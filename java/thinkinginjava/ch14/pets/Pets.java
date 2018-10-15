package ch14.pets;

import java.util.*;
public class Pets {
    public static final PetCreator creator = new LiteralPetCreator();
    public static ArrayList<Pet> arrayList(int size){
        return creator.arrayList(size);
    }
}