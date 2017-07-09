# Contact Helper

###### Description:

In order to keep track of the contact information in our ever-growing organization, I made a simple helper tool. You can find it running at ```shell2017.picoctf.com:29018```

#### Hints:

 * Is there a function pointer somewhere that you could change?

 * Learning about ptmalloc2 might help. glibc uses a modified version of it.


#### Solution

Ok, so we're given a source and an executable, that's always nice to work with. The hints make it fairly clear that whatever vulnerability we have to work with is going to be a heap-based vulnerability, and the goal is to overwrite some sort of function pointer. The first thing that grabs my attention from the source is this global function pointer in the program data struct:
```C
struct program_data {
    contact_t contacts[MAX_CONTACTS];
    uint64_t num_contacts;

    exit_function_t exit_function; // Hey wow this looks like a convenient victim pointer from the hint!!!
    char company_name[COMPANY_LENGTH];
};
```

Now just from the fact that Contact Helper was the highest point value binary, I had a Meta-Game intuition that the vulnerability was going to be a double free. A quick search for calls to free in the source code further assured me this was the case.

```C
bool add_contact(uint64_t id, char *username, char *phone) {
    contact_t new_employee = xmalloc(sizeof(struct contact_data));

    contact_t old_employee = get_contact(id);
    if (old_employee != NULL) {
        free(old_employee);
        data.num_contacts--;
    }

    new_employee->id = id;
    bool success = copy_username(new_employee->username, username) &&
        copy_phone(new_employee->phone, phone);

    if (data.num_contacts >= MAX_CONTACTS || !success || !insert_contact(new_employee)) {
        free(new_employee);
        return false;
    }

    return true;
}
```

The first thing I immediately noticed was the two calls to ```free()```, with one being conditional. This is generally a big no-no, but I realized that they were different structs. I wasn't sure my initial assumption was right, so I went back to the source. I saw this:

```C
if (add_contact(id, username, phone)) {
    printf("Successfully added.\n");
} else {
    printf("Failed to add.\n");
}
```
And then I realized that the pointer to the old contact is *never* reassigned despite having been freed in `add_contact` This means that two consecutive calls to ```add_contact``` with the right parameters could cause a double free! Some quick trolling around in ltrace confirmed this:

```bash
python -c 'print "add 0 bret 1234567890\n" + "add 0 bret 12345678\n" + "add 0 bret 1234567\n"' |
ltrace ./contacts |& egrep "alloc|free"
```
```
malloc(56)                                       = 0x1c2e010    <- Initial Allocation
malloc(56)                                       = 0x1c2e050    <- New Contact struct alloc'd
free(0x1c2e010)                                  = <void>       <-Old Struct is free'd
free(0x1c2e050)                                  = <void>       <- Failure to match data frees new struct
malloc(56)                                       = 0x1c2e050    <- New Contact struct alloc'd
*** Error in `./contacts': double free or corruption (fasttop): 0x0000000001c2e010 ***
free(0x1c2e010 <no return ...>                                  <- Old Struct (not reassigned) free'd twice
```

Alright! From here, the goal was to get another fastbin on the free list, so I did a bit of reasoning on what the program functions did. I came up with these rules:

  1) Add new that matches none => immediate malloc then free
    2) Add new that matches but fails => malloc(new) free(old) free(new)
    3) Add new that matches perfectly =>malloc(new) free(old)

After this, I sat open with ltrace in one terminal and vim in another, and I pretended to be malloc, maintaining a free list and tracking which contacts pointed where. I sort of got the order right by trial and error, but the order is shown in my pwntools script. After that, the third allocation is treated as a free chunk, meaning I could write (almost) arbitrarily. (The costraints made it that I had to overwrite ```stdin``` in the GOT ( I don't exactly remember why ) but since used a magic shell gadget, the lack of arguments didn't really matter.) At this point, I had to simply put in the address I wanted to leak and then subsequently write over in the third allocation, which was treated as being free. This meant that my input was treated as a pointer, and the next allocation would overwrite the GOT! After that it was fairly standard pwnable procedure: leak,calculate, and overwrite.
