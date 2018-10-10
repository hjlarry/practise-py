package ch07;

import static utils.Print.*;

class Soap {
    private String s;

    Soap() {
        print("Soap()");
        s = "constructed";
    }

    public String toString() {
        return s;
    }
}

// init example
public class Bath {
    // initializing at point of defination;
    private String s1="happy", s2="happ2", s3, s4;
    private Soap sp;
    private int i;
    private float toy;
    public Bath(){
        print("Inside bath()");
        s3 = "joy";
        toy = 3.14f;
        sp = new Soap();
    }
    //instance initialization
    {i = 47;}
    public String toString(){
        if (s4==null){  // lazy initialization
            s4 = "Jou";
        }
        return s1+s2+s3+s4+i+toy+sp;
    }
    public static void main(String[] args){
        Bath b = new Bath();
        print(b);
    }
}
