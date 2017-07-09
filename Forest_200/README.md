# Forest

##### Description:
I was wandering the [forest](forest) and found a file. It came with some [string](string.txt)

#### Hints:
A number of disassemblers have tools to help view structs

#### Solution:

We are given a binary and a string.txt containing a string consisting of "D", "L", and "R".

Running `./forest` tells us what it expects as arguments:

```
$ ./forest
You have the wrong number of arguments for this forest.
./forest [password] [string]
```

Opening `forest` in your favorite disassembler shows us that before argc and argv are examined, a function is called with a string. This must be some sort of initialization.

The string, at 0x8049C0C, is "yuoteavpxqgrlsdhwfjkzi_cmbn".
The function is at 0x80486F0 and seems too complicated to be worth attempting to understand at the moment.

Examining `main` again, we see that another function is called, taking the initialization function's return value as well as the arguments we provided the program. The return value of this function is then checked: 1 is success and 0 is failure.

We can reverse the two functions, and the functions called by them. The result is in `rev.py` (with some additions).

There are a few things to note. The program generates a tree based on a constant (the string at 0x8049C0C), and walks through the tree using inputs we give it. "L" and "R" continue recursion while "D" stops it. I couldn't understand how the program worked, though, so I took to testing.

In line 59 of `rev.py`, the program checks if both strings have been traversed (null terminated strings in C, we make do with `len` in python) and whether some validation condition has been met (line 53). If we get rid of the length restriction, perhaps we can learn something about the validation.

Trying "y" as the password, due to the intialization string in the binary starting with "y", printed "Success". I tried with more characters, but they failed. I tried shortening the "DLLD..." string argument, and it still worked all the way down to a single "D".
I assume from this that each letter in the password corresponds to some number letters in the string, but this number could be variable because of the recursive nature of the validation function. My speculation is that the number of letters in the password is equal to the number of times "D" appears in the string, which is 51 (which holds true for the flag we later find).

Trying a few more letters manually along with the entire string (from string.txt), "yo" prints "Success" as well. We can definitely bruteforce this. A simplified version of the reversed code and the bruteforce is in `solve.py`.

Running `solve.py` gives us this:
you_could_see_the_forest_for_the_trees_ckyljfxyfmswaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

There are extra a's at the end, because I fetched 100 letters instead of 51.
