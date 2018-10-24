package com.algorithms.charpter1_3;

import com.princeton.StdOut;

import java.util.Iterator;

public class CircleQueue<Item> implements Iterable<Item> {
    private Node last;
    private int N;

    private class Node {
        Item item;
        Node next;
    }

    public Iterator<Item> iterator() {
        return new ListIterator();
    }

    private class ListIterator implements Iterator<Item> {
        private Node current = last;
        private int n = size();

        public boolean hasNext() {
            return n > 0;
        }

        public Item next() {
            Item item = current.item;
            current = current.next;
            n--;
            return item;
        }
    }

    public boolean isEmpty() {
        return N == 0; // first==null也可以
    }

    public int size() {
        return N;
    }

    public void enqueue(Item item) {
        Node x = new Node();
        x.item = item;
        if (isEmpty()) {
            x.next = x;
        } else {
            x.next = last.next;
            last.next = x;
        }
        last = x;
        N++;
    }

    public Item dequeue() {
        if (isEmpty()) {
            throw new RuntimeException("queue under flow");
        }
        Item item = last.next.item;
        if (last.next == last) {
            last = null;
        } else {
            last.next = last.next.next;
        }
        N--;
        return item;
    }


    public static void main(String[] args) {
        CircleQueue<String> s = new CircleQueue<>();
        s.enqueue("as");
        s.enqueue("bp");
        s.enqueue("99");
        StdOut.println("(" + s.size() + " left on CircleQueue)");
        for (String t : s) {
            StdOut.println(t);
        }
    }
}
