package ch07;

import static utils.Print.*;

// 基类初始化
class Art{
    Art(){
        print("this is art()");
    }
}

class  Drawing extends Art{
    Drawing(){
        print("this is drawing");
    }
}

public class Cartoon extends Drawing{
    Cartoon(){
        print("this is cartoon");
    }
    public static void main(String[] args){
        Cartoon x = new Cartoon();
    }
}
