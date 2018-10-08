package ch03;


class Tank{
    int level;
}

class Letter{
    char c;
}

public class Assignment {
    public static void main(String[] args){
        Tank t1 = new Tank();
        Tank t2 = new Tank();
        t1.level = 9;
        t2.level = 40;
        prt("1: t1_level:" + t1.level + ", t2_level" + t2.level);
//      java 赋值非核心对象时是传递引用
        t1 = t2;
        prt("2: t1_level:" + t1.level + ", t2_level" + t2.level);
        t1.level = 100;
        prt("3: t1_level:" + t1.level + ", t2_level" + t2.level);

        Integer c1 = 1;
        Integer c2 = 2;
        prt("1: c1:" + c1 + ", c2:" + c2);
        c1 = c2;
        prt("2: c1:" + c1 + ", c2:" + c2);
        c1 = 99;
        prt("3: c1:" + c1 + ", c2:" + c2);

        Letter x = new Letter();
        x.c = 'a';
        prt("1: x_c:" + x.c);
//      对象传入方法时传递的是对象本身而非副本
        f(x);
        prt("2: x_c:" + x.c);

    }

    private static void f(Letter y){
        y.c = 'z';
    }

    private static void prt(String s){
        System.out.println(s);
    }
}
