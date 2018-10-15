package ch11;

import java.util.*;

class Snow{}
class Power extends Snow{}
class Light extends Power{}
class Heavy extends Power{}
class Crusty extends Snow{}
class Slush extends Snow{}

public class AddingGroups {
    public static void main(String[] args){
        Collection<Integer> collection = new ArrayList<Integer>(Arrays.asList(1,2,3,4,5));
        Integer[] moreInts = {6,7,8,9};
        System.out.println(collection);
        collection.addAll(Arrays.asList(moreInts));
        System.out.println(collection);
        Collections.addAll(collection, moreInts);
        System.out.println(collection);
        Collections.addAll(collection, 16,17,18,19);
        System.out.println(collection);

        List<Integer> list = Arrays.asList(20,21,22);
        list.set(1, 99);
        System.out.println(list);
//        list.add(60);  // runtime error, because the underlying array cannot be resized
        System.out.println(list);

        List<Snow> list2 = Arrays.asList(new Power(), new Crusty(), new Slush());
        List<Snow> list3 = Arrays.asList(new Light(), new Heavy());  // 在书中这样是创建不了的，但试验这个版本的jdk是可以的
        System.out.println(list2);
        System.out.println(list3);

    }
}
