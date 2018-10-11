package ch07;

// 代理模式
public class SpaceShipDelegation {
    private String name;
    private SpaceControls controls = new SpaceControls();
    public SpaceShipDelegation(String name){
        this.name = name;
    }
    public void up(int vel){
        controls.up(vel);
    }
    public void down(int vel){
        controls.down(vel);
    }
    public void left(int vel){
        controls.left(vel);
    }
    public void right(int vel){
        controls.right(vel);
    }
    public static void main(String[] args){
        SpaceShipDelegation ssd = new SpaceShipDelegation("haha");
        ssd.up(100);
    }
}
