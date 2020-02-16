#include <stdio.h>
#include "extend_c.h"

void hello()
{
    printf("hello world ! \n");
}

/* 计算最大公约数 */
int gcd(int x, int y)
{
    int g = y;
    while (x > 0)
    {
        g = x;
        x = y % x;
        y = g;
    }
    return g;
}

void each(int nums[], int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("%d\n", nums[i]);
    }
}

void test(data_t *d)
{
    d->x = 100;
    d->y = 200;
}