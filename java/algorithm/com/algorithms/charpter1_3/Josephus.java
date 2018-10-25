package com.algorithms.charpter1_3;

import com.princeton.StdOut;

// ex 1.3.37
public class Josephus {
    private int N;
    private int M;

    public Josephus(int N, int M) {
        this.N = N;
        this.M = M;
    }

    public void kill() {
        Queue<Integer> q = new Queue<Integer>();
        for (int i = 0; i < N; i++) {
            q.enqueue(i);
        }
        int k = 0;
        while (!q.isEmpty()){
            int x = q.dequeue();
            if (++k % M == 0){
                StdOut.println(x);
            }else{
                q.enqueue(x);
            }
        }

    }

    public static void main(String[] args) {
        Josephus j = new Josephus(7, 2);
        j.kill();
    }
}
