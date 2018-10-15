package ch11;

import java.util.*;
import ch14.pets.*;

public class SimpleIteration {
    public static void main(String[] args){
        List<Pet> pets = Pets.arrayList(12);
        Iterator<Pet> it = pets.iterator();
        while(it.hasNext()){
            Pet p = it.next();
            System.out.println(p.id() + ":" + p + " ");
        }
        System.out.println();
        for (Pet pet:pets)
            System.out.println(pet.id() + ":" + pet + " ");

        it = pets.iterator();
        for(int i=0;i<5;i++){
            it.next();
            it.remove();
        }
        System.out.println(pets);
    }
}
