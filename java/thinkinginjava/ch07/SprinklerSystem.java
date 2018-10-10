package ch07;

class WaterSource {
    private String s;

    WaterSource() {
        s = "constructed";
    }

    public String toString() {
        return s;
    }
}

// combination example
public class SprinklerSystem {
    private String v1, v2, v3, v4;
    private WaterSource ws = new WaterSource();
    private int i;
    private float f;
    public String toString(){
        return "value1="+v1+",v2="+v2+"\n i="+i+", f="+f+",source="+ws;
    }
    public static void main(String[] args){
        SprinklerSystem ss = new SprinklerSystem();
        System.out.println(ss);
    }
}
