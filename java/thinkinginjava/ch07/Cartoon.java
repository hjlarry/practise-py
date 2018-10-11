package ch07;

import static utils.Print.*;

// 基类初始化
class Art{
    Art(int i){
        print("this is art()");
    }
}

class  Drawing extends Art{
    Drawing(){
        super(5);  // 必须在首行初始化父类
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
