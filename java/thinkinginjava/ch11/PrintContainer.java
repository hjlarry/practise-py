package ch11;

import java.util.*;
import static utils.Print.*;

public class PrintContainer {
    static Collection fill(Collection<String> collection){
        collection.add("jat");
        collection.add("cat");
        collection.add("dog");
        collection.add("dog");
        return collection;
    }

    static Map fill(Map<String, String> map){
        map.put("jat", "Fuzzy");
        map.put("cat", "Rags");
        map.put("dog", "Bosco");
        map.put("dog", "Spot");
        return map;
    }

    public static void main(String[] args){
        print(fill(new ArrayList<String>()));
        print(fill(new LinkedList<String>()));
        print(fill(new HashSet<String>())); // 快速查找
        print(fill(new TreeSet<String>())); // 按比较结果的升序排列元素
        print(fill(new LinkedHashSet<String>())); // 按插入的顺序排列元素
        print(fill(new HashMap<String, String>()));
        print(fill(new TreeMap<String, String>()));
        print(fill(new LinkedHashMap<String, String>()));
    }
}
