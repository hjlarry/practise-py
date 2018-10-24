package com.algorithms.charpter1_3;

import com.princeton.StdOut;
import java.util.Iterator;

// ex 1.3.33
public class Deque<Item> implements Iterable<Item> {
    private Node left;
    private Node right;
    private int N;

    private class Node {
        Item item;
        Node next;
        Node prev;

        public Node(Item item) {
            this.item = item;
            this.next = null;
            this.prev = null;
        }
    }

    public Iterator<Item> iterator() {
        return new ListIterator();
    }

    private class ListIterator implements Iterator<Item> {
        private Node current = left;

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
        return N == 0;
    }

    public int size() {
        return N;
    }

    public void pushLeft(Item item) {
        Node old_left = left;
        left = new Node(item);
        if (isEmpty()) {
            right = left;
        } else {
            left.next = old_left;
            left.prev = right;
        }
        N++;
    }

    public void pushRight(Item item) {
        Node old_right = right;
        right = new Node(item);
        if (isEmpty()) {
            left = right;
        } else {
            old_right.next = right;
            right.prev = old_right;
        }
        N++;
    }

    public Item popLeft() {
        Node old_left = left;
        Item item = old_left.item;
        left = old_left.next;
        left.prev = old_left.prev;
        N--;
        return item;
    }

    public Item popRight() {
        Node old_right = right;
        Item item = old_right.item;
        right = old_right.prev;
        right.next = null;
        N--;
        return item;
    }


    public static void main(String[] args) {
        Deque<String> dq = new Deque<>();
        dq.pushLeft("1");
        dq.pushLeft("2");
        dq.pushLeft("3");
        dq.pushRight("4");
        for (String s : dq) {
            StdOut.println(s);
        }
        StdOut.println();
        dq.popLeft();
        dq.popRight();
        for (String s : dq) {
            StdOut.println(s);
        }
    }
}
