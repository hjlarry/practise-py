package com.algorithms.charpter1_1;

import com.algorithms.StdOut;

public class Ex19 {
    private static long[] F(int N) {
        long[] fab = new long[N + 1];
        if (N == 0) {
            return fab;
        }
        fab[1] = 1;
        if (N == 1) {
            return fab;
        }
        for (int i = 2; i <= N; i++) {
            fab[i] = fab[i - 1] + fab[i - 2];
        }
        return fab;
    }

    public static void main(String[] args) {
        long[] fab = F(99);
        for (int i = 0; i < fab.length; i++) {
            StdOut.println(i + " " + fab[i]);
        }
    }
}
