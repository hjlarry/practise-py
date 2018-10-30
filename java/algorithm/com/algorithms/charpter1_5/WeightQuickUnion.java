package com.algorithms.charpter1_5;

import com.princeton.StdIn;
import com.princeton.StdOut;
import com.princeton.Stopwatch;

public class WeightQuickUnion {
    private int[] id; // 分量ID
    private int[] sz;  // 各个根节点对应的分量大小
    private int count; // 分量数量

    public WeightQuickUnion(int N) {
        count = N;
        id = new int[N];
        sz = new int[N];
        for (int i = 0; i < N; i++) {
            id[i] = i;
            sz[i] = 1;
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
        if(sz[pRoot] < sz[qRoot]){
            id[pRoot] = qRoot;
            sz[qRoot] += sz[pRoot];
        }else {
            id[qRoot] = pRoot;
            sz[pRoot] += sz[qRoot];
        }
        count -- ;
    }

    public static void main(String[] args) {
        Stopwatch timer = new Stopwatch();
        int N = StdIn.readInt();
        WeightQuickUnion uf = new WeightQuickUnion(N);
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
        StdOut.println(time1);
    }
}
