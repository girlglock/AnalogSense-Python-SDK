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
    dev = devices[int(input("Select device index: "))]

def on_keys(active_keys):
    for k in active_keys:
        print(as_.scancode_to_string(k["scancode"]), f"{k['value']:.2f}")

dev.start_listening(on_keys)
input("enter to stop...\n")
dev.stop_listening()