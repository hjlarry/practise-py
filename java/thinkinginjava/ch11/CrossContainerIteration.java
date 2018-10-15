package ch11;

import java.util.*;
import ch14.pets.*;

public class CrossContainerIteration {
    public static void display(Iterator<Pet> it){
        while(it.hasNext()){
            Pet p = it.next();
            System.out.println(p.id() + ":" + p + " ");
        }
        System.out.println();
    }
    public static void main(String[] args){
        ArrayList<Pet> pets = Pets.arrayList(8);
        LinkedList<Pet> petll = new LinkedList<Pet>(pets);
        HashSet<Pet> peths = new HashSet<Pet>(pets);
        TreeSet<Pet> petts = new TreeSet<Pet>(pets);
        // display void not care about the type of container
        display(pets.iterator());
        display(petll.iterator());
        display(peths.iterator());
        display(petts.iterator());
    }
}
