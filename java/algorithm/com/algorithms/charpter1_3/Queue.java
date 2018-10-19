package com.algorithms.charpter1_3;

import com.princeton.StdOut;

import java.util.Iterator;

public class Queue<Item> implements Iterable<Item> {
    private Node first;
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
        private Node current = first;

        public boolean hasNext() {
            return current != null;
        }

        public Item next() {
            Item item = current.item;
            current = current.next;
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
        Node old_last = last;
        last = new Node();
        last.item = item;
        if (isEmpty()) {
            first = last;
        } else {
            old_last.next = last;
        }
        N++;
    }

    public Item dequeue() {
        Item item = first.item;
        first = first.next;
        if (isEmpty()) {
            last = null;
        }
        N--;
        return item;
    }


    public static void main(String[] args) {
        Queue<String> s = new Queue<>();
        s.enqueue("as");
        s.enqueue("bp");
        s.enqueue("99");
        StdOut.println("(" + s.size() + " left on queue)");
        for (String t : s) {
            StdOut.println(t);
        }
    }
}
