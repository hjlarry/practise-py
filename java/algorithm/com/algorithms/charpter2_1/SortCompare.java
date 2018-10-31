package com.algorithms.charpter2_1;

import com.princeton.StdOut;
import com.princeton.StdRandom;
import com.princeton.Stopwatch;

public class SortCompare {
    public static double time(String alg, Double[] a) {
        Stopwatch timer = new Stopwatch();
        if (alg.equals("Selection")) {
            Selection.sort(a);
        }
        if (alg.equals("Insertion")) {
            Insertion.sort(a);
        }
        return timer.elapsedTime();
    }

    public static double timeRandomInput(String alg, int N, int T) {
        double total = 0.0;
        Double[] a = new Double[N];
        for (int t = 0; t < T; t++) {
            for (int i = 0; i < N; i++) {
                a[i] = StdRandom.uniform();
            }
            total += time(alg, a);
        }
        return total;
    }

    public static void main(String[] args) {
        String alg1 = "Selection";
        String alg2 = "Insertion";
        int N = 1000;
        int T = 100;
        double t1 = timeRandomInput(alg1, N, T);
        double t2 = timeRandomInput(alg2, N, T);
        StdOut.println(alg1 + " use " + t1);
        StdOut.println(alg2 + " use " + t2);
        StdOut.println(alg2 + "/" + alg1 + "=" + t2 / t1);
    }
}
