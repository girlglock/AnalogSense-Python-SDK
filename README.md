# AnalogSense Python SDK
Python port of [AnalogSense.js](https://github.com/AnalogSense/JavaScript-SDK/) for analog keyboard input.
## Supported Keyboards/Devices
- Everything by Wooting
- Everything by NuPhy
- Everything by DrunkDeer
- Razer Huntsman V2 Analog<sup>R</sup>
- Razer Huntsman Mini Analog<sup>R</sup>
- Razer Huntsman V3 Pro<sup>R</sup>
- Razer Huntsman V3 Pro Mini<sup>R</sup>
- Razer Huntsman V3 Pro Tenkeyless<sup>R</sup>
- Keychron Q1 HE<sup>P, F</sup>
- Keychron Q3 HE<sup>P, F</sup>
- Keychron Q5 HE<sup>P, F</sup>
- Keychron K2 HE<sup>P, F</sup>
- Lemokey P1 HE<sup>P, F</sup>
- Madlions MAD60HE<sup>P</sup>
- Madlions MAD68HE<sup>P</sup>
- Madlions MAD68R<sup>P</sup>
- Redragon K709HE<sup>P</sup>

<sup>R</sup> Razer Synapse needs to be installed and running for analogue inputs to be received from this keyboard.  
<sup>P</sup> The official firmware only supports polling, which can lead to lag and missed inputs.  
<sup>F</sup> [Custom firmware with full analog report functionality is available](https://analogsense.org/firmware/).

## Installation
```bash
pip install AnalogSensePy
```

On Linux you may need udev rules or `sudo` for hid
```bash
printf '%s\n' \
  'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0660", GROUP="input"' \
  'SUBSYSTEM=="usb", ATTRS{idVendor}=="31e3", MODE="0660", GROUP="input"' \
  'SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", MODE="0660", GROUP="input"' \
  'SUBSYSTEM=="usb", ATTRS{idVendor}=="1532", MODE="0660", GROUP="input"' \
  'SUBSYSTEM=="usb", ATTRS{idVendor}=="19f5", MODE="0660", GROUP="input"' \
  'SUBSYSTEM=="usb", ATTRS{idVendor}=="352d", MODE="0660", GROUP="input"' \
  'SUBSYSTEM=="usb", ATTRS{idVendor}=="3434", MODE="0660", GROUP="input"' \
  'SUBSYSTEM=="usb", ATTRS{idVendor}=="362d", MODE="0660", GROUP="input"' \
  'SUBSYSTEM=="usb", ATTRS{idVendor}=="373b", MODE="0660", GROUP="input"' \
  'SUBSYSTEM=="usb", ATTRS{idVendor}=="372e", MODE="0660", GROUP="input"' \
  | sudo tee /etc/udev/rules.d/99-analogsense.rules

sudo udevadm control --reload-rules && sudo udevadm trigger
```
## Usage
```python
from analogsense import AnalogSense

as_ = AnalogSense()
devices = as_.get_devices()

if not devices:
    print("no supported analog keyboards found.")
    exit()

if len(devices) == 1:
    dev = devices[0]
else:
    for i, d in enumerate(devices):
        print(f"  [{i}] {d.product_name}")
    dev = devices[int(input("select device index: "))]

def on_keys(active_keys):
    for k in active_keys:
        # converting the scancode to a nice readable string
        name = as_.scancode_to_string(k["scancode"])
        
        # some providers can return the digital state of the key
        # (what the system perceives the key as pressed or not)
        # other providers that do not support this will return None
        if k["digital"] is not None:
            digital = " [down]" if k["digital"] else " [up]"
        else:
            digital = ""

        print(f"{name:20s} {k['value']:.4f}{digital}")

dev.start_listening(on_keys)
input("press keys... enter to stop.\n")
dev.stop_listening()
```

The following functions are available on `AnalogSense`:
- `get_devices() -> list[Device]`
- `open_device(vendor_id, product_id) -> Device | None`
- `scancode_to_string(scancode: int) -> str`

A device instance has the following members:
- `start_listening(handler: Callable[[list[{"scancode": int, "value": float}]], None])`
- `stop_listening()`
- `product_name: str`
- `forget()`
- `dev: DeviceHandle`

### Scancodes
The scancodes provided by this library are primarily HID scancodes; most keys are mapped as seen on usage page 0x07 (A = 0x04, B = 0x05, ...).

Control keys (usage page 0x0C) are mapped in the `0x3__` range, modulo 0x100:
- `0x3B5` = Next Track
- `0x3B6` = Previous Track
- `0x3B7` = Stop Media
- `0x3CD` = Play/Pause
- `0x394` = Open File Explorer
- `0x323` = Open Browser Home Page

OEM-specific keys are mapped in the `0x4__` range:
- `0x401` = Brightness Up
- `0x402` = Brightness Down
- `0x403` = Profile 1
- `0x404` = Profile 2
- `0x405` = Profile 3
- `0x408` = Profile Switch
- `0x409` = Function Key (Fn)