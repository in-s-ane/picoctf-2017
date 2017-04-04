import subprocess
import string

def run(command, _input):
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output = process.communicate(input=_input)
    return output[0]

desired = "tu1|\h+&g\OP7@% :BH7M6m3g="
correct = ""

while len(correct) < len(desired):
    found = False
    for char in string.printable:
        candidate = char + correct
        output = run("./MuchAdoAboutHacking", candidate + " ")
        if desired.startswith(output):
            correct = char + correct
            print correct
            found = True
            break

    if not found:
        print "Failed"
        break

print correct
