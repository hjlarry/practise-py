package ch07;

import java.util.*;

import static utils.Print.*;

class Value {
    int i;

    public Value(int i) {
        this.i = i;
    }
}

final class CannotExtend{

}


public class FinalData {
    private static Random rand = new Random(47);
    private String id;
    private final int x; // blank final, 必须在域定义处或构造器中用表达式赋值。
    public FinalData(String id) {
        this.id = id;
        this.x = 1;
    }
    public FinalData(int id) {
        x = id;
    }

    // can be compile-time constants:
    // 定义为public，则可以被用于包外；定义为static，则强调只有一份；定义为final，则说明它是一个常量
    private final int valueOne = 9;
    private static final int VALUE_TWO = 99;
    public static final int VALUE_THREE = 39;
    private static int VALUE_FOUR = 44;
    // can not be compile-time constants:
    private final int i4 = rand.nextInt(20);
    static final int INT_5 = rand.nextInt(20);
    private Value v1 = new Value(10);
    private final Value v2 = new Value(22);
    private static final Value VALUE_3 = new Value(33);
    private final int[] a = {3, 4, 5, 6};

    public String toString() {
        return id + ": i4=" + i4 + ". INT_5=" + INT_5;
    }
    public static void main(String[] args){
        FinalData fd1 = new FinalData("fd1");
        // fd1.valueOne++;   can`t change value
        fd1.v2.i++;
        fd1.v1 = new Value(9);
        for (int i=0; i< fd1.a.length; i++){
            fd1.a[i]++;
            // !fd1.VALUE_3 = new Value(1);
        }
        print(fd1);
        print("create new finaldata:");
        FinalData fd2 = new FinalData("fd2");
        print(fd1);
        print(fd2);
        fd2.VALUE_FOUR = 55;
        print(fd1.VALUE_FOUR);
        print(fd1.x);
        FinalData fd3 = new FinalData(99);
        print(fd3.x);
    }
}
