package com.algorithms.charpter1_3;

import com.princeton.StdOut;

import java.util.Iterator;

public class ResizingArrayStack<Item> implements Iterable<Item> {

    private Item[] a = (Item[]) new Object[1]; // stack entries
    private int N = 0;  // size

    public boolean isEmpty() {
        return N == 0;
    }

    private void resize(int max) {
        Item[] temp = (Item[]) new Object[max];
        for (int i = 0; i < N; i++) {
            temp[i] = a[i];
        }
        a = temp;
    }

    public int size() {
        return N;
    }

    public void push(Item item) {
        if (N == a.length) {
            resize(N * 2);
        }
        a[N++] = item;
    }

    public Item pop() {
        Item item = a[--N];
        a[N] = null; // 对象游离
        if (N > 0 && N == a.length / 4) {
            resize(N / 2);
        }
        return item;
    }

    public Iterator<Item> iterator() {
        return new ReverseArrayIterator();
    }

    private class ReverseArrayIterator implements Iterator<Item> {
        private int i = N;

        public boolean hasNext() {
            return i > 0;
        }

        public Item next() {
            return a[--i];
        }

        public void remove() {
        }
    }

    public static void main(String[] args) {
        ResizingArrayStack<String> s = new ResizingArrayStack<>();
        s.push("as");
        s.push("bp");
        StdOut.println("(" + s.size() + " left on stack)");
        for (String t : s) {
            StdOut.println(t);
        }
    }
}
