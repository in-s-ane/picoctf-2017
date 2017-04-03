#include <iostream>
#include <fstream>

void printL(int x, int L[17])
{
    std::cout << x << " [";
    for (int i = 0; i < 17; ++i)
    {
        std::cout << L[i] << ",";
    }
    std::cout << "]\n";
}

int mips(unsigned int x)
{
    int L[17] = {0};
    L[6] = x & -16777216;
    L[16] = x & 16711680;
    L[7] = x & 65280;
    L[4] = x & 255;
    L[3] = L[6] >> 24;

    while (1)
    {
        L[5] = L[2] < 13 ? 1 : 0;
        L[2]++;
        if (!L[5]) break;
        L[3] -= 13;
    }

    L[3] -= 6;
    printL(1, L);
    L[5] = L[3] << 24;
    printL(2, L);
    L[16] = L[16] >> 16;
    printL(3, L);
    L[2] = L[16] - 81;
    printL(4, L);
    L[8] = L[2] << 6;
    printL(5, L);
    L[3] = L[2] << 8;
    printL(6, L);
    L[3] = L[3] - L[8];
    printL(7, L);
    L[3] = L[2] - L[3];
    printL(8, L);
    L[7] = L[7] >> 8;
    printL(9, L);
    L[2] = L[4] << 1;
    printL(10, L);
    L[2] += 3;
    printL(11, L);
    L[3] = L[3] << 16;
    printL(12, L);
    if (L[7] != L[2])
        L[2] = 165;
    else
        L[2] = 94;

    L[2] = L[2] - 94;
    printL(13, L);
    L[2] = L[2] << 8;
    printL(14, L);
    L[6] = L[6] >> 24;
    printL(15, L);
    L[16] = L[6] - L[16];
    printL(16, L);
    L[4] = L[4] - L[16];
    printL(17, L);
    L[3] = L[5] + L[3];
    printL(18, L);
    L[3] = L[2] + L[3];
    printL(19, L);
    L[16] = L[4] + L[3];
    printL(20, L);
    if (L[16] == 0)
        return 1;
    return 0;
}

int main()
{
    mips(-10);

    /* mips(-10); */
    /* mips(-1000000); */
    /* mips(-1000000000); */

    /* while (1) */
    /* { */
    /*     int x = 0; */
    /*     std::cin >> x; */
    /*     mips(x); */
    /* } */

    return 0;
}
