package com.algorithms.charpter1_1;

import com.princeton.StdOut;

public class Ex01_10 {
    public static void main(String[] args) {
        StdOut.println((1 + 2.236) / 2);
        StdOut.println(1 + 2 + "3");
        StdOut.println(true && false || true && true);
        StdOut.println(1 + 2 + 4.0);

        int f = 0;
        int g = 1;
        for (int i = 0; i < 15; i++) {
            StdOut.println(f);
            f = f + g;
            g = f - g;
        }

        double t = 9.0;
        while (Math.abs(t - 9.0 / t) > .001)
            t = (9.0 / t + t) / 2.0;
        StdOut.println(t);
        StdOut.printf("%.5f\n", t);

        System.out.println('b' + 'c');
        System.out.println((char) ('b' + 4));

        int[] a = new int[10];
        for (int i = 0; i < 10; i++) {
            a[i] = 9 - i;
        }
        for (int i = 0; i < 10; i++) {
            a[i] = a[a[i]];
        }
        StdOut.println(a[3]);
        StdOut.println(toBinStr(20));

    }

    private static String toBinStr(int N) {
        String s = "";
        for (int n = N; n > 0; n /= 2) {
            s = (n % 2) + s;
        }
        return s;
    }
}