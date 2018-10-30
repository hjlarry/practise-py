package com.algorithms.charpter1_5;

import com.princeton.StdIn;
import com.princeton.StdOut;
import com.princeton.Stopwatch;
public class QuickUnion {
    private int[] id; // 分量ID
    private int count; // 分量数量

    public QuickUnion(int N) {
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
        while(p!= id[p]){
            p = id[p];
        }
        return p;
    }

    public void union(int p, int q) {
        int pRoot = find(p);
        int qRoot = find(q);
        if(pRoot == qRoot){
            return;
        }
        id[pRoot] = qRoot;
        count -- ;
    }

    public static void main(String[] args) {
        Stopwatch timer = new Stopwatch();
        int N = StdIn.readInt();
        QuickUnion uf = new QuickUnion(N);
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
        double time1 = timer.elapsedTime();
        StdOut.println(time1); // 0.91 of 10w data
    }
}
