# Deeper Into The Matrix
###### Description:
Flaws in the matrix have been corrected, and now you must dive deeper to discover its secrets. Jack in at ```shell2017.picoctf.com:16845```

#### Hints:
 * Sometimes a NULL pointer can be useful.
 * The GOT is protected now - you'll have to find something else to attack.

#### Solution

For starts, we only have the executable. Quickly opening it in IDA, I began the usual reversing process, comparing it to the source of the first matrix problem. Luckily, most of it seemed similar, with the originial indexing scheme having been fixed. With the second program being nearly identical to the first, my gut instinct was that the vulnerability was related to the indexing scheme, not to some overflow. In order to confirm this, I looked at how the program handled input, using only ```sscanf()```, with no actual string arrays or buffers to be overflowed. With that in mind, I sought out to find the NULL pointer referenced in the hint.

I looked at the functions in the order I would use them, starting with ```handle_create()``` 

```C
 if ( (unsigned int)(a2 - 1) > 0x270F
    || (v4 = malloc(0xCu),
        v4[1] = a2,
        *v4 = format,
        v5 = v4,
        v3 = (_DWORD)format * a2,
        v4[2] = calloc((_DWORD)format * a2, 4u),
        *(&matrices + v2) = v5,
        *MK_FP(__GS__, 20) != v7) )
  {

````
Given that the only pointers we really have influence on are the pointers to the matrices, I looked up the references to ```*alloc()```. Sure enough, the *alloc family returns null when allocation requests fail due to a lack of memory. The global array only contains pointers to the structs, so it's unlikely that a ```malloc(12)``` would fail. ```calloc()``` however, is called based on the size of the array of floats, so potentially up to ```10,000^2 * sizeof(float)``` (big number) bytes. Surely, that could make it fail! After that, exploitation takes advantage of the fact that in C, there are no arrays, just offsets from the base. This means that my "array" (lets call it ```data```) that the program thinks is stored at 0 can be indexed safely. ```data[12]``` is actually just ```&data + 12*4```. Although that would cause a segfault, we have access to large enough indices that we can address some valid parts of memory. From here, exploitation was going to be super easy, just a typical overwrite...

Except that it wasn't. Full RelRo makes most of the writable sections of the binary useless for overwrites, and I was also going to have to deal with limits on index sizes and exponent-mantissa form instead of easy integer form. The first order of business was to increase the range of memory. With full indices of 10,000, I could only access up to ```0x2faf0800```, which isn't quite good enough. I leaked the address of my crafted matrix, which was conveniently stored in a global array. After that, I set the columns field of the struct equal to 1 million, using python's ```struct``` class. After that, I had access to all of addressable memory, and I leaked a GOT pointer, calculated libc, and... googled for hours. I didn't know what to overwrite, but after quite a bit of digging I found that glibc conveniently has writable pointers for programmers to hook into ```free()```. After finding that, I overwrote the hook pointer with the computed address of system, then packed "/bin/sh" as 2 32-bit ~~floats~~ ints, and stored them as the row and column of another victim struct that I freed to get shell.

One issue I ran into was that when I tried my exploit remotely, it didn't work at all. My script was awfully written at this point, and then it hit me: Calloc wasn't failing remotely. I was running on a VM, so the first struct failed, but the servers had more resources at their disposal. I deleted my whole script, and rewrote it in a way that could be iterated over. After that, I got a shell!!!
