package com.algorithms.charpter2_1;

public class Selecttion extends BaseSort {
    public static void sort(Comparable[] a) {

        int len = a.length;
        for (int i = 0; i < a.length; i++) {
            int min = i;
            for (int j = i; j < len; j++) {
                if (less(a[j], a[min])) {
                    min = j;
                }
            }
            exch(a, min, i);
        }
    }

    public static void main(String[] args) {
        String[] a = {"s", "o", "r", "t", "e", "x", "a", "m", "p", "l", "e"};
        sort(a);
        assert isSorted(a);
        show(a);
    }
}
