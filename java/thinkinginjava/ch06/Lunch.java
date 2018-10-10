package ch06;


class Soup1 {
    // private构造方法将不允许别人创建该类的对象
    private Soup1() {
    }

    static Soup1 makeSoup() {
        return new Soup1();
    }
}

class Soup2 {
    private Soup2() {
    }

    private static Soup2 sp2 = new Soup2();

    // 单例实现
    static Soup2 access() {
        return sp2;
    }

    void f() {

    }
}

public class Lunch {
    void testPrivate() {
//        can`t do this: Soup1 sp1 = new Soup1();
    }

    public int testStatic() {
        Soup1 sp1 = Soup1.makeSoup();
        System.out.println(sp1);
        return 999;
    }

    void testSingle() {
        Soup2.access().f();
    }
}
