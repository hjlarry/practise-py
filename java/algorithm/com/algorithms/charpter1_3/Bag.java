package com.algorithms.charpter1_3;
import com.princeton.StdOut;
import java.util.Iterator;

public class Bag<Item> implements Iterable<Item> {
    private Node first;
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
            return current!=null;
        }

        public Item next() {
            Item item = current.item;
            current = current.next;
            return item;
        }
    }

    public boolean isEmpty() {
        return N == 0;
    }

    public int size() {
        return N;
    }

    public void add(Item item) {
        Node oldfirst = first;
        first = new Node();
        first.item = item;
        first.next = oldfirst;
        N++;
    }


    public static void main(String[] args) {
        Bag<String> s = new Bag<>();
        s.add("as");
        s.add("bp");
        s.add("99");
        StdOut.println("(" + s.size() + " left on bag)");
        for (String t : s) {
            StdOut.println(t);
        }
    }
}
