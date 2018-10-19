package com.algorithms.charpter1_3;

import com.princeton.StdIn;
import com.princeton.StdOut;

public class FixedCapacityStack<Item> {
    private Item[] a; // stack entries
    private int N;  // size
    FixedCapacityStack(int cap){
        a = (Item[]) new Object[cap];
    }
    public boolean isEmpty(){
        return N == 0;
    }
    private void resize(int max){
        Item[] temp = (Item[]) new Object[max];
        for (int i=0;i<N;i++){
            temp[i] = a[i];
        }
        a = temp;
    }
    public int size(){
        return N;
    }
    public void push(Item item){
        if (N == a.length){
            resize(N*2);
        }
        a[N++] = item;
    }
    public Item pop(){
        Item item = a[--N];
        a[N] = null; // 对象游离
        if (N>0 && N==a.length/4){
            resize(N/2);
        }
        return item;
    }
    public static void main(String[] args){
        FixedCapacityStack<String> s = new FixedCapacityStack<>(10);
        while (!StdIn.isEmpty()){
            String item = StdIn.readString();
            if (!item.equals("-")){
                s.push(item);
            }else if(!s.isEmpty()){
                StdOut.print(s.pop() + " ");
            }
        }
        StdOut.println("("+s.size()+" left on stack");
    }
}
