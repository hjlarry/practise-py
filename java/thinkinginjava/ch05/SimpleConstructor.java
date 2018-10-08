package ch05;

import com.sun.tools.javac.comp.Flow;

class Rock {
    Rock(int i) {
        System.out.println(i);
    }
}

class Rock2 {
    String s1;
    String s2 = "dsa";
    String s3;

    Rock2() {
        s3 = "jje";
    }
}

class Rock3 {
    Rock3() {
        System.out.println("no params");
    }

    Rock3(String s) {
        System.out.println("have params" + s);
    }
}

class Rock4 {
    Rock4 eat() {
        System.out.println("jaj");
        return this;
    }

    void test() {
        eat();
        this.eat();
    }
}

class Leaf {
    private int i = 0;

    Leaf increment() {
        i++;
        return this;
    }

    void print() {
        System.out.println("i=" + i);
    }
}

class Person {
    public void eat(Apple apple) {
        Apple peeled = apple.getPeeled();
        System.out.println("yummy");
    }
}

class Apple {
    Apple getPeeled() {
        return Peeler.peel(this);
    }
}

class Peeler {
    static Apple peel(Apple apple) {
        return apple;
    }
}

class Flower {
    int petalCount = 0;
    String s = "init value";

    Flower(int pentals) {
        petalCount = pentals;
        System.out.println("constuctor with int only , petalcount=" + petalCount);
    }

    Flower(String ss) {
        s = ss;
        System.out.println("constuctor with string only , s=" + s);
    }

    Flower(String s, int pentals) {
        this(pentals);
//        this(s); can`t call two
        this.s = s;
        System.out.println("String and int");
    }

    Flower() {
        this("hi", 47);
        System.out.println("default no args constructor");
    }

    void printPetalCount() {
//        this(11); can`t call not in constructor
        System.out.println("petalCount=" + petalCount + " s=" + s);
    }
}

class Window {
    Window(int marker) {
        System.out.println("window " + marker);
    }
}

// 对象初始化顺序
class House{
    Window w1 = new Window(1);
    House(){
        System.out.println("house ");
        Window w2 = new Window(2);
    }
    Window w3 = new Window(3);
    void f(){
        System.out.println("ff ");
    }
    Window w4 = new Window(4);
}

public class SimpleConstructor {
    public static void main(String[] args) {
        new Rock(10);
        Rock2 r = new Rock2();
        System.out.println(r.s1);
        System.out.println(r.s2);
        System.out.println(r.s3);
        new Rock3();
        new Rock3("haha");
        Leaf leaf = new Leaf();
        leaf.increment().increment().increment().print();
        new Person().eat(new Apple());
        new Rock4().test();

        Flower x = new Flower();
        x.printPetalCount();

        House h = new House();
        h.f();
    }
}
