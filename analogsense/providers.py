from __future__ import annotations
import threading
import time
import warnings
from typing import Callable

from .keymaps import razer_to_wooting, nuphy_to_wooting, bytech_to_wooting, KEY_NONE
from .layouts import (
    LAYOUT_KEYCHRON_Q1_HE, LAYOUT_KEYCHRON_Q3_HE, LAYOUT_KEYCHRON_Q5_HE,
    LAYOUT_KEYCHRON_K2_HE, LAYOUT_LEMOKEY_P1_HE,
    LAYOUT_MADLIONS_MAD60HE, LAYOUT_MADLIONS_MAD68HE,
    layout_key, layout_size, layout_index_to_row, layout_index_to_col,
    drunkdeer_index_to_hid_scancode,
)

ActiveKey = dict
Handler   = Callable[[list[ActiveKey]], None]


class AsProvider:
    FILTERS = []

    def __init__(self, dev):
        self.dev = dev
        self._buffer: dict[int, float] = {}
        self._thread: threading.Thread | None = None
        self._running = False

    @property
    def product_name(self):
        return getattr(self.dev, "product_string", "Unknown")

    def forget(self):
        self.stop_listening()
        try:
            self.dev.close()
        except Exception:
            pass

    def _buffer_to_active_keys(self):
        return [{"scancode": sc, "value": v, "digital": None} for sc, v in self._buffer.items()]

    def start_listening(self, handler: Handler):
        raise NotImplementedError

    def stop_listening(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None

    def _read_loop(self, handler: Handler):
        while self._running:
            try:
                data = self.dev.read(64, timeout_ms=100)
                if data:
                    self._handle_report(bytes(data), handler)
            except Exception as e:
                warnings.warn(f"HID read error: {e}")
                break

    def _handle_report(self, data: bytes, handler: Handler):
        raise NotImplementedError


class AsProviderWootingV1(AsProvider):
    FILTERS = [
        {"usage_page": 0xFF54, "vendor_id": 0x31E3},
        {"usage_page": 0xFF54, "vendor_id": 0x03EB, "product_id": 0xFF01},
        {"usage_page": 0xFF54, "vendor_id": 0x03EB, "product_id": 0xFF02},
    ]

    def start_listening(self, handler: Handler):
        self._running = True
        self._prev_scancodes: set[int] = set()
        self._thread = threading.Thread(target=self._read_loop, args=(handler,), daemon=True)
        self._thread.start()

    def _handle_report(self, data: bytes, handler: Handler):
        active_keys = []
        current_scancodes = set()
        i = 0
        while i < len(data):
            if i + 2 > len(data): break
            scancode = (data[i] << 8) | data[i + 1]
            i += 2
            if scancode == 0: break
            if i >= len(data): break
            value = data[i]
            i += 1
            active_keys.append({"scancode": scancode, "value": value / 255, "digital": None})
            current_scancodes.add(scancode)
        for released in self._prev_scancodes - current_scancodes:
            active_keys.append({"scancode": released, "value": 0.0, "digital": None})
        self._prev_scancodes = current_scancodes
        handler(active_keys)


class AsProviderWootingV2(AsProvider):
    FILTERS = [
        {"usage_page": 0xFF53, "vendor_id": 0x31E3},
    ]

    def start_listening(self, handler: Handler):
        self._running = True
        self._prev_scancodes: set[int] = set()
        self._thread = threading.Thread(target=self._read_loop, args=(handler,), daemon=True)
        self._thread.start()

    def _handle_report(self, data: bytes, handler: Handler):
        active_keys = []
        current_scancodes = set()
        i = 0
        while i + 4 <= len(data):
            keycode  = data[i + 1]
            packed   = data[i + 2]
            value_hi = data[i + 3]
            digital  = packed & 0x1
            key_ns   = (packed >> 2) & 0xF
            value_lo = (packed >> 6) & 0x3
            scancode = (key_ns << 8) | keycode
            value    = (value_hi << 2) | value_lo
            i += 4
            if scancode == 0: break
            if value == 0: continue
            active_keys.append({"scancode": scancode, "value": value / 1023, "digital": digital})
            current_scancodes.add(scancode)
        for released in self._prev_scancodes - current_scancodes:
            active_keys.append({"scancode": released, "value": 0.0, "digital": 0})
        self._prev_scancodes = current_scancodes
        handler(active_keys)


class AsProviderRazerHuntsman(AsProvider):
    FILTERS = [
        {"vendor_id": 0x1532, "product_id": 0x0266, "usage_page": 0x0001},  #Razer Huntsman V2
        {"vendor_id": 0x1532, "product_id": 0x0282, "usage_page": 0x0001},  #Razer Huntsman Mini
    ]

    _REPORT_ID = 7

    def start_listening(self, handler: Handler):
        self._running = True
        self._prev_scancodes: set[int] = set()
        self._thread = threading.Thread(target=self._read_loop, args=(handler,), daemon=True)
        self._thread.start()

    def _handle_report(self, data: bytes, handler: Handler):
        if data[0] == self._REPORT_ID:
            data = data[1:]
        elif len(data) > 1 and data[0] != 0:
            return
        active_keys = []
        current_scancodes = set()
        i = 1
        while i < len(data):
            scancode = data[i]; i += 1
            if scancode == 0: break
            value = data[i]; i += 1
            hid_sc = _razer_to_hid(scancode)
            if hid_sc:
                active_keys.append({"scancode": hid_sc, "value": value / 255, "digital": None})
                current_scancodes.add(hid_sc)
        for released in self._prev_scancodes - current_scancodes:
            active_keys.append({"scancode": released, "value": 0.0, "digital": None})
        self._prev_scancodes = current_scancodes
        handler(active_keys)


class AsProviderRazerHuntsmanV3(AsProvider):
    FILTERS = [
        {"vendor_id": 0x1532, "product_id": 0x02A6, "usage_page": 0x0001},  #Razer Huntsman V3 Pro
        {"vendor_id": 0x1532, "product_id": 0x02A7, "usage_page": 0x0001},  #Razer Huntsman V3 Pro Tenkeyless
        {"vendor_id": 0x1532, "product_id": 0x02B0, "usage_page": 0x0001},  #Razer Huntsman V3 Pro Mini
    ]
    _REPORT_ID = 11

    def start_listening(self, handler: Handler):
        self._running = True
        self._prev_scancodes: set[int] = set()
        self._thread = threading.Thread(target=self._read_loop, args=(handler,), daemon=True)
        self._thread.start()

    def _handle_report(self, data: bytes, handler: Handler):
        if data[0] == self._REPORT_ID:
            data = data[1:]
        elif len(data) > 1 and data[0] != 0:
            return
        active_keys = []
        current_scancodes = set()
        i = 1
        while i + 2 < len(data):
            scancode = data[i]; i += 1
            if scancode == 0: break
            value   = data[i]; i += 1
            _unused = data[i]; i += 1
            hid_sc = _razer_to_hid(scancode)
            if hid_sc:
                active_keys.append({"scancode": hid_sc, "value": value / 255, "digital": None})
                current_scancodes.add(hid_sc)
        for released in self._prev_scancodes - current_scancodes:
            active_keys.append({"scancode": released, "value": 0.0, "digital": None})
        self._prev_scancodes = current_scancodes
        handler(active_keys)

#this one needs testing
class AsProviderNuphy(AsProvider):
    FILTERS = [
        {"vendor_id": 0x19F5, "usage_page": 0x0001, "usage": 0x0000},
    ]

    def start_listening(self, handler: Handler):
        self._running = True
        self._thread = threading.Thread(target=self._read_loop, args=(handler,), daemon=True)
        self._thread.start()

    def _handle_report(self, data: bytes, handler: Handler):
        if data[0] != 0xA0: return
        raw_sc = (data[2] << 8) | data[3]
        hid_sc = _nuphy_to_hid(raw_sc)
        if hid_sc == 0: return
        if data[7] == 0:
            self._buffer.pop(hid_sc, None)
        else:
            self._buffer[hid_sc] = data[7] / 200
        handler(self._buffer_to_active_keys())


class AsProviderDrunkdeer(AsProvider):
    FILTERS = [
        {"usage_page": 0xFF00, "vendor_id": 0x352D},
    ]

    _POLL_PAYLOAD = bytes([
        0xB6, 0x03, 0x01, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ])

    def start_listening(self, handler: Handler):
        self._running = True
        self._active_keys = []
        self._thread = threading.Thread(target=self._poll_loop, args=(handler,), daemon=True)
        self._thread.start()

    def _poll_loop(self, handler: Handler):
        self.dev.write(b"\x04" + self._POLL_PAYLOAD)
        while self._running:
            try:
                data = self.dev.read(64, timeout_ms=100)
                if not data: continue
                data = bytes(data)
                n = data[3]
                if n == 0:
                    self._active_keys = []
                for i in range(4, len(data)):
                    value = data[i]
                    if value != 0:
                        sc = drunkdeer_index_to_hid_scancode(n * (64 - 5) + (i - 4))
                        self._active_keys.append({"scancode": sc, "value": value / 40, "digital": None})
                if n == 2:
                    handler(list(self._active_keys))
                    self._active_keys = []
            except Exception as e:
                warnings.warn(f"DrunkDeer read error: {e}")
                break


class AsProviderKeychron(AsProvider):
    FILTERS = [
        {"vendor_id": 0x3434, "product_id": 0x0B10, "usage_page": 0xFF60, "usage": 0x61},  #Q1 HE ANSI
        {"vendor_id": 0x3434, "product_id": 0x0B11, "usage_page": 0xFF60, "usage": 0x61},  #Q1 HE ISO
        {"vendor_id": 0x3434, "product_id": 0x0B12, "usage_page": 0xFF60, "usage": 0x61},  #Q1 HE JIS
        {"vendor_id": 0x3434, "product_id": 0x0B30, "usage_page": 0xFF60, "usage": 0x61},  #Q3 HE ANSI
        {"vendor_id": 0x3434, "product_id": 0x0B50, "usage_page": 0xFF60, "usage": 0x61},  #Q5 HE ANSI
        {"vendor_id": 0x3434, "product_id": 0x0E20, "usage_page": 0xFF60, "usage": 0x61},  #K2 HE ANSI
        {"vendor_id": 0x3434, "product_id": 0x0E21, "usage_page": 0xFF60, "usage": 0x61},  #K2 HE ISO
        {"vendor_id": 0x3434, "product_id": 0x0E22, "usage_page": 0xFF60, "usage": 0x61},  #K2 HE JIS
        {"vendor_id": 0x362D, "product_id": 0x0610, "usage_page": 0xFF60, "usage": 0x61},  #Lemokey P1 HE ANSI
    ]

    _INIT_PAYLOAD = bytes([
        0xA9, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ])

    def _pick_layout(self):
        pid = self.dev.product_id
        if pid in (0x0B10, 0x0B11, 0x0B12): return LAYOUT_KEYCHRON_Q1_HE
        if pid == 0x0B30: return LAYOUT_KEYCHRON_Q3_HE
        if pid == 0x0B50: return LAYOUT_KEYCHRON_Q5_HE
        if pid == 0x0610: return LAYOUT_LEMOKEY_P1_HE
        return LAYOUT_KEYCHRON_K2_HE

    def start_listening(self, handler: Handler):
        self._running = True
        self.layout = self._pick_layout()
        self._thread = threading.Thread(target=self._keychron_loop, args=(handler,), daemon=True)
        self._thread.start()

    def _build_single_key_request(self, index):
        key = layout_key(self.layout, index)
        if key == KEY_NONE: return None
        row = layout_index_to_row(self.layout, index)
        col = layout_index_to_col(self.layout, index)
        buf = bytearray(32)
        buf[0] = 0xA9; buf[1] = 0x30; buf[2] = row; buf[3] = col
        return bytes(buf)

    def _build_all_keys_request(self):
        buf = bytearray(32)
        buf[0] = 0xA9; buf[1] = 0x31
        return bytes(buf)

    def _keychron_loop(self, handler: Handler):
        self.dev.write(b"\x00" + self._INIT_PAYLOAD)
        data = bytes(self.dev.read(64, timeout_ms=500) or [])
        if not data: return
        am_version = data[2] if len(data) > 2 else 0
        has_full_report = len(data) > 31 and data[31] == 0x45
        self._buffer = {}
        if has_full_report:
            self._run_full_mode(handler)
        else:
            self._run_single_mode(handler, am_version)

    def _run_full_mode(self, handler: Handler):
        chunk_index = 0
        self.dev.write(b"\x00" + self._build_all_keys_request())
        while self._running:
            data = bytes(self.dev.read(64, timeout_ms=200) or [])
            if not data: continue
            for i in range(30):
                li = chunk_index * 30 + i
                if li < layout_size(self.layout):
                    key = layout_key(self.layout, li)
                    if key != KEY_NONE:
                        travel = data[2 + i] if 2 + i < len(data) else 0
                        if travel >= 5:
                            self._buffer[key] = min(travel / 235, 1.0)
                        else:
                            self._buffer.pop(key, None)
            chunk_index += 1
            if chunk_index == 4:
                handler(self._buffer_to_active_keys())
                chunk_index = 0
                self.dev.write(b"\x00" + self._build_all_keys_request())

    def _run_single_mode(self, handler: Handler, am_version: int):
        value_offset = 6 if am_version >= 4 else 3
        index = 0
        while True:
            req = self._build_single_key_request(index)
            if req:
                self.dev.write(b"\x00" + req)
                break
            index = (index + 1) % layout_size(self.layout)
        while self._running:
            data = bytes(self.dev.read(64, timeout_ms=200) or [])
            if not data: continue
            key = layout_key(self.layout, index)
            travel = data[value_offset] if value_offset < len(data) else 0
            if travel >= 5:
                self._buffer[key] = min(travel / 235, 1.0)
            else:
                self._buffer.pop(key, None)
            handler(self._buffer_to_active_keys())
            while True:
                index = (index + 1) % layout_size(self.layout)
                req = self._build_single_key_request(index)
                if req:
                    self.dev.write(b"\x00" + req)
                    break


class AsProviderMadlions(AsProvider):
    FILTERS = [
        #MAD60HE
        {"vendor_id": 0x373B, "product_id": 0x1053, "usage_page": 0xFF60, "usage": 0x61},
        {"vendor_id": 0x373B, "product_id": 0x1054, "usage_page": 0xFF60, "usage": 0x61},
        {"vendor_id": 0x373B, "product_id": 0x1055, "usage_page": 0xFF60, "usage": 0x61},
        {"vendor_id": 0x373B, "product_id": 0x1056, "usage_page": 0xFF60, "usage": 0x61},
        {"vendor_id": 0x373B, "product_id": 0x105D, "usage_page": 0xFF60, "usage": 0x61},
        #MAD68HE
        {"vendor_id": 0x373B, "product_id": 0x1058, "usage_page": 0xFF60, "usage": 0x61},
        {"vendor_id": 0x373B, "product_id": 0x1059, "usage_page": 0xFF60, "usage": 0x61},
        {"vendor_id": 0x373B, "product_id": 0x105A, "usage_page": 0xFF60, "usage": 0x61},
        {"vendor_id": 0x373B, "product_id": 0x105C, "usage_page": 0xFF60, "usage": 0x61},
        #MAD68R
        {"vendor_id": 0x373B, "product_id": 0x10A7, "usage_page": 0xFF60, "usage": 0x61},
    ]

    _INIT_PAYLOAD = bytes([
        0x02, 0x96, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x04,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ])

    _MAD60HE_PIDS = {0x1053, 0x1054, 0x1055, 0x1056, 0x105D}

    def start_listening(self, handler: Handler):
        pid = self.dev.product_id
        self.layout = LAYOUT_MADLIONS_MAD60HE if pid in self._MAD60HE_PIDS else LAYOUT_MADLIONS_MAD68HE
        self._running = True
        self._thread = threading.Thread(target=self._madlions_loop, args=(handler,), daemon=True)
        self._thread.start()

    def _madlions_loop(self, handler: Handler):
        payload = bytearray(self._INIT_PAYLOAD)
        self.dev.write(b"\x00" + bytes(payload))
        offset = 0
        self._buffer = {}
        while self._running:
            data = bytes(self.dev.read(64, timeout_ms=200) or [])
            if not data: continue
            for i in range(4):
                idx = offset + i
                if idx < len(self.layout):
                    key = self.layout[idx]
                    pos = 7 + i * 5 + 3
                    travel = (data[pos] << 8) | data[pos + 1] if pos + 1 < len(data) else 0
                    if travel == 0:
                        self._buffer.pop(key, None)
                    else:
                        self._buffer[key] = travel / 350
            handler(self._buffer_to_active_keys())
            offset = (offset + 4) % len(self.layout)
            payload[6] = offset
            self.dev.write(b"\x00" + bytes(payload))


class AsProviderBytech(AsProvider):
    FILTERS = [
        {"vendor_id": 0x372E, "product_id": 0x105B, "usage_page": 0xFF00},  #Redragon K709 HE
    ]

    def _build_payload(self, cmd, sub):
        buf = bytearray(63)
        buf[0] = cmd
        buf[1] = sub
        total = 9 + sum(buf[:-1])
        buf[-1] = 255 - (total % 256)
        return bytes(buf)

    def start_listening(self, handler: Handler):
        self._running = True
        self._thread = threading.Thread(target=self._bytech_loop, args=(handler,), daemon=True)
        self._thread.start()

    def _bytech_loop(self, handler: Handler):
        payload = self._build_payload(0x97, 0x00)
        self._buffer = {}
        self.dev.write(b"\x09" + payload)
        last_poll = time.monotonic()
        while self._running:
            now = time.monotonic()
            if now - last_poll >= 1.0:
                self.dev.write(b"\x09" + payload)
                last_poll = now
            data = bytes(self.dev.read(64, timeout_ms=100) or [])
            if not data: continue
            if data[0] == 0x97 and data[1] == 0x01:
                self.dev.write(b"\x09" + payload)
                last_poll = time.monotonic()
                self._buffer = {}
                count = data[5]
                for i in range(0, count, 4):
                    base = 6 + i
                    if base + 3 >= len(data): break
                    pos      = (data[base] << 8) | data[base + 1]
                    distance = (data[base + 2] << 8) | data[base + 3]
                    sc = _bytech_to_hid(pos)
                    if sc and distance > 10:
                        self._buffer[sc] = min(distance / 355, 1.0)
                handler(self._buffer_to_active_keys())


def _razer_to_hid(sc):
    result = razer_to_wooting.get(sc, 0)
    if result == 0:
        warnings.warn(f"Failed to map Razer scancode to HID scancode: {sc:#x}")
    return result

def _nuphy_to_hid(sc):
    result = nuphy_to_wooting.get(sc, 0)
    if result == 0:
        warnings.warn(f"Failed to map NuPhy scancode to HID scancode: {sc:#x}")
    return result

def _bytech_to_hid(sc):
    result = bytech_to_wooting.get(sc, 0)
    if result == 0:
        warnings.warn(f"Failed to map Bytech scancode to HID scancode: {sc:#x}")
    return result


ALL_PROVIDERS = [
    AsProviderWootingV1,
    AsProviderWootingV2,
    AsProviderRazerHuntsman,
    AsProviderRazerHuntsmanV3,
    AsProviderNuphy,
    AsProviderDrunkdeer,
    AsProviderKeychron,
    AsProviderMadlions,
    AsProviderBytech,
]