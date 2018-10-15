package ch11;

import java.util.*;
import ch14.pets.*;
import static utils.Print.*;

public class LinkedListFeatures {
    public static void main(String[] args){
        LinkedList<Pet> pets = new LinkedList<Pet>(Pets.arrayList(5));
        LinkedList<Pet> pet_null = new LinkedList<Pet>();
        print(pets);
        print("pets.getFirst():"+pets.getFirst());
        print("pets.element():"+pets.element());
        print("pets.peek():"+pets.peek());
        print("pets.remove():"+pets.remove());
        print("pets.removeFirst():"+pets.removeFirst());
        print("pets.poll():"+pets.poll());
        //when empty return null
        print("pet_null.peek():"+pet_null.peek());
        print("pet_null.poll():"+pet_null.poll());
        //when empty raise exception
//        print("pet_null.remove():"+pet_null.getFirst());
        print(pets);

        pets.addFirst(new Rat());
        print("after add_first:"+pets);
        pets.offer(Pets.randomPet());
        print("after offer:"+pets);
        pets.add(Pets.randomPet());
        print("after add:"+pets);
        pets.addLast(new Hamster());
        print("after addLast:"+pets);
        print("remove Last:"+pets.removeLast());

    }
}
