package com.algorithms.charpter2_1;

public class Insertion extends BaseSort {
    public static void sort(Comparable[] a) {
        int len = a.length;
        for (int i = 1; i < len; i++) {
            for (int j = i; j > 0 && less(a[j], a[j - 1]); j--) {
                exch(a, j, j - 1);
            }
        }
    }
    public static void main(String[] args){
        String[] a = {"s", "o", "r", "t", "e", "x", "a", "m", "p", "l", "e"};
        sort(a);
        assert isSorted(a);
        show(a);
    }
}
