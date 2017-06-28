#include <iostream>
#include <fstream>

int mips(unsigned int x) {
    unsigned int L[17] = {0};
    L[6] = x & -16777216;
    L[16] = x & 16711680;
    L[7] = x & 65280;
    L[4] = x & 255;
    L[3] = L[6] >> 24;

    while (1) {
        L[5] = L[2] < 13 ? 1 : 0;
        L[2]++;
        if (!L[5]) break;
        L[3] -= 13;
    }

    L[3] -= 6;
    L[5] = L[3] << 24;
    L[16] = L[16] >> 16;
    L[2] = L[16] - 81;
    L[8] = L[2] << 6;
    L[3] = L[2] << 8;
    L[3] = L[3] - L[8];
    L[3] = L[2] - L[3];
    L[7] = L[7] >> 8;
    L[2] = L[4] << 1;
    L[2] += 3;
    L[3] = L[3] << 16;
    if (L[7] != L[2])
        L[2] = 165;
    else
        L[2] = 94;

    L[2] = L[2] - 94;
    L[2] = L[2] << 8;
    L[6] = L[6] >> 24;
    L[16] = L[6] - L[16];
    L[4] = L[4] - L[16];
    L[3] = L[5] + L[3];
    L[3] = L[2] + L[3];
    L[16] = L[4] + L[3];
    if (L[16] == 0)
        return 1;
    return 0;
}

int main()
{
    unsigned int x = 0;
    while (x < 4294967295)
    {
        int r = mips(x);
        if (r == 1) {
            std::cout << "X found: " << x << "\n";
            std::cout << "Answer: " << "0x" << std::hex << x << "\n";
            break;
        }
        x++;
        if (x % 100000000 == 0) {
            std::cout << "x: " << x << "\n";
        }
    }

    return 0;
}

/*
The first thing that comes to mind is to reduce the mips instructions down to a simple expression and
use a constraint solver to solve for x
However, we could not completely simplify the instructions, so we chose to use brute-force.
$ g++ -O3 solution.cpp && ./a.out
...
x found: 2941370206
Answer: 0xaf51bf5e
*/
