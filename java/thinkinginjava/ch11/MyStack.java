package ch11;

import java.util.LinkedList;

public class MyStack<T> {
    private LinkedList<T> storage = new LinkedList<T>();
    public void push(T v){
        storage.addFirst(v);
    }
    public T peek(){
        return storage.getFirst();
    }
    public T pop(){
        return storage.removeFirst();
    }
    public boolean empty(){
        return storage.isEmpty();
    }
    public String toString(){
        return storage.toString();
    }
    public static void main(String[] args){
        MyStack<String> myStack = new MyStack<String>();
        for (String s:"my dog is sls".split(" "))
            myStack.push(s);
        while (!myStack.empty())
            System.out.println(myStack.pop());
    }
}
