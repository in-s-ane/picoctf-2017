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

"""
After spending much time trying to get the spl to compile the given program, we can finally examine its
behavior. The behavior is deterministic, meaning the same input will produce the same output. Because of this, we
can brute force the correct input we need to generate the desired output.

Alternatively, its possible to decode the program by reading the documentation of the language.

Its@MidSuMm3rNights3xpl0!t
"""
