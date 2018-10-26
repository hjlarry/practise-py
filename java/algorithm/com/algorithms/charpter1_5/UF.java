package com.algorithms.charpter1_5;

import com.princeton.StdIn;
import com.princeton.StdOut;

public class UF {
    private int[] id; // 分量ID
    private int count; // 分量数量

    public UF(int N) {
        count = N;
        id = new int[N];
        for (int i = 0; i < N; i++) {
            id[i] = i;
        }
    }

    public int count() {
        return count;
    }

    public boolean connected(int p, int q) {
        return find(p) == find(q);
    }

    public int find(int p) {
        return id[p];
    }

    public void union(int p, int q) {
        int idP = id[p];
        int idQ = id[q];
        if (idP == idQ) {
            return;
        }
        id[q] = idP;
        for (int i : id) {
            if (i == idQ) {
                i = idP;
            }
        }
        count -- ;
    }

    public static void main(String[] args) {
        int N = StdIn.readInt();
        UF uf = new UF(N);
        while (!StdIn.isEmpty()) {
            int p = StdIn.readInt();
            int q = StdIn.readInt();
            if (uf.connected(p, q)) {
                continue;
            }
            uf.union(p, q);
            StdOut.println(p + "  " + q);
        }
        StdOut.println(uf.count() + "compoents");
    }


}
