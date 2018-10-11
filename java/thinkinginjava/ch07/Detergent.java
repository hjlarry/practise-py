package ch07;
import static utils.Print.*;

// 继承示例
public class Detergent extends Cleanser{
    public void apple(){
        append("Detergent.apple()");
        super.apple();
    }
    public void form(){
        append("form()");
    }
    public static void main(String[] args){
        Detergent x = new Detergent();
        x.dillute();
        x.apple();
        x.form();
        print(x);

        print("Test base class:");
        Cleanser.main(args);
    }
}
class Cleanser{
    private String s = "Cleanser";
    public void append(String a){
        s += a;
    }
    protected void dillute(){
        append(" dillute()");
    }
    public void apple(){
        append(" apple()");
    }
    public String toString(){
        return s;
    }
    public static void main(String[] args){
        Cleanser x = new Cleanser();
        x.dillute();x.apple();
        print(x);
    }
}