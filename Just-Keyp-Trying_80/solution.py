mappings = { 0x04:"a", 0x05:"b", 0x06:"c", 0x07:"d", 0x08:"e", 0x09:"f", 0x0A:"g", 0x0B:"h", 0x0C:"i", 0x0D:"j", 0x0E:"k", 0x0F:"l", 0x10:"m", 0x11:"n", 0x12:"o", 0x13:"p", 0x14:"q", 0x15:"r", 0x16:"s", 0x17:"t", 0x18:"u", 0x19:"v", 0x1A:"w", 0x1B:"x", 0x1C:"y", 0x1D:"z", 0x1E:"1", 0x1F:"2", 0x20:"3", 0x21:"4", 0x22:"5", 0x23:"6", 0x24:"7", 0x25:"8", 0x26:"9", 0x27:"0", 0x28:"\n", 0x2C:" ", 0x2D:"-", 0x2E:"=", 0x2F:"[", 0x30:"]", 0x31:"\\", 0x33:";", 0x34:"'", 0x36:",", 0x37:".", 0x38:"/", 0x55:"*", 0x56:"-", 0x57:"+", 0xCC:"#"
            }

shifted_mappings = { 0x04:"A", 0x05:"B", 0X06:"C", 0X07:"D", 0X08:"E", 0X09:"F", 0X0A:"G", 0X0B:"H", 0X0C:"I", 0X0D:"J", 0X0E:"K", 0X0F:"L", 0X10:"M", 0X11:"N", 0X12:"O", 0X13:"P", 0X14:"Q", 0X15:"R", 0X16:"S", 0X17:"T", 0X18:"U", 0X19:"V", 0X1A:"W", 0X1B:"X", 0X1C:"Y", 0X1D:"Z", 0x1E:"!", 0x1F:"@", 0x20:"#", 0x21:"$", 0x22:"%", 0x23:"^", 0x24:"&", 0x25:"*", 0x26:"(", 0x27:")", 0x2C: " ", 0x2D:"_", 0x2E:"+", 0x2F:"{", 0x30:"}", 0x31:"|", 0x33:":", 0x34:"\"", 0x36:"<", 0x37:">", 0x38:"?", 0x55:"*", 0x56:"_", 0x57:"+", 0xCC:"#"
                    }

nums = []
keys = open('data.txt').readlines()
for x in range(len(keys)):
    split = keys[x].strip().split(":")
    # Only keep the packets that are valid
    if len(split) != 8:
        continue

    if split[2] != "00" and split[3] == "00":
        control = False
        shifted = False
        if split[0] == "02":
            # Shift was held
            shifted = True
        if split[0] == "01":
            # Control was held
            control = True

        nums.append((int(split[2], 16), shifted, control))

caps = False

output = ""
for x in range(len(nums)):
    n = nums[x]
    num = n[0]
    shifted = n[1]
    control = n[2]
    if num in mappings:
        if shifted:
            output += shifted_mappings[num]
        elif control:
            output += "CONTROL-%s" % mappings[num]
        else:
            if caps:
                output += mappings[num].upper()
            else:
                output += mappings[num]
    elif num == 0x2A:
        # Backspace
        output = output[:-1]
    elif num == 0x39:
        # Caps lock
        caps = not caps

print output

"""
Looking at the packets, we see some usb data that represent keys on a keyboard.
We can extract the data with the following:
$ tshark -r data.pcap -T fields -e usb.capdata > data.txt

Using the keyboard mappings found at http://www.freebsddiary.org/APC/usb_hid_usages.php, we can decode the data.
$ python solution.py
flag[pr355-0nwards-00784a00]

The flag is:
flag{pr355_0nwards_00784a00}
"""
