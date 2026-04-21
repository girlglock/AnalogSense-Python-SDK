from __future__ import annotations
import sys
import warnings

from .providers import ALL_PROVIDERS, AsProvider
from .keymaps import wooting_to_name, razer_to_wooting, nuphy_to_wooting, bytech_to_wooting
from .layouts import drunkdeer_index_to_hid_scancode

try:
    import hid as _hid
    _HID_AVAILABLE = True
except ImportError:
    _HID_AVAILABLE = False
    if sys.platform == "linux":
        warnings.warn("'hid' is not installed. you can install it with: pip install hid")
    else:
        warnings.warn("'hidapi' is not installed. you can install it with: pip install hidapi")


class DeviceHandle:
    def __init__(self, hid_dev, info: dict):
        self._dev           = hid_dev
        self.vendor_id      = info["vendor_id"]
        self.product_id     = info["product_id"]
        self.product_string = info.get("product_string") or f"{info['vendor_id']:#06x}:{info['product_id']:#06x}"

    def __getattr__(self, name):
        return getattr(self._dev, name)

    def read(self, size, timeout_ms=100):
        return self._dev.read(size, timeout_ms)

    def write(self, data):
        return self._dev.write(data)

    def close(self):
        return self._dev.close()


class AnalogSense:
    def __init__(self, extra_providers=None):
        self.providers = list(ALL_PROVIDERS)
        if extra_providers:
            self.providers.extend(extra_providers)

    def _collect_candidates(self):
        candidates = []
        seen = set()
        for provider_cls in self.providers:
            for f in provider_cls.FILTERS:
                try:
                    vendor_id  = f.get("vendor_id", 0)
                    product_id = f.get("product_id", 0)
                    for info in _hid.enumerate(vendor_id, product_id):
                        dedup_key = (info["vendor_id"], info["product_id"], info.get("usage_page", 0), info.get("usage", 0))
                        if dedup_key in seen: continue
                        if "usage_page" in f and info.get("usage_page") != f["usage_page"]: continue
                        seen.add(dedup_key)
                        candidates.append((info, provider_cls))
                except Exception as e:
                    warnings.warn(f"Error enumerating HID devices: {e}")
        return candidates

    def _open(self, info, provider_cls):
        try:
            if sys.platform == "linux":
                dev = _hid.Device(path=info["path"])
            else:
                dev = _hid.device()
                dev.open_path(info["path"])
            return provider_cls(DeviceHandle(dev, info))
        except Exception as e:
            if "Permission denied" in str(e):
                warnings.warn(
                    f"Permission denied opening {info.get('product_string', info['path'])}. "
                    "On Linux, udev rules are required. See: https://github.com/girlglock/AnalogSense-Python-SDK#installation"
                )
            else:
                warnings.warn(f"Failed to open device: {e}")
            return None

    def get_devices(self):
        if not _HID_AVAILABLE: return []
        return [dev for dev in (self._open(info, cls) for info, cls in self._collect_candidates()) if dev is not None]

    def open_device(self, vendor_id, product_id):
        if not _HID_AVAILABLE: return None
        for info, provider_cls in self._collect_candidates():
            if info["vendor_id"] == vendor_id and info["product_id"] == product_id:
                return self._open(info, provider_cls)
        return None

    def scancode_to_string(self, scancode):
        return wooting_to_name.get(scancode, str(scancode))

    @staticmethod
    def razer_scancode_to_hid(scancode):
        result = razer_to_wooting.get(scancode, 0)
        if result == 0: warnings.warn(f"Failed to map Razer scancode to HID: {scancode:#x}")
        return result

    @staticmethod
    def nuphy_scancode_to_hid(scancode):
        result = nuphy_to_wooting.get(scancode, 0)
        if result == 0: warnings.warn(f"Failed to map NuPhy scancode to HID: {scancode:#x}")
        return result

    @staticmethod
    def bytech_scancode_to_hid(scancode):
        result = bytech_to_wooting.get(scancode, 0)
        if result == 0: warnings.warn(f"Failed to map Bytech scancode to HID: {scancode:#x}")
        return result

    @staticmethod
    def drunkdeer_index_to_hid(index):
        return drunkdeer_index_to_hid_scancode(index)