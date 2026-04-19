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