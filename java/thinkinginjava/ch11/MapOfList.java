package ch11;

import java.util.*;

import ch14.pets.*;

import static utils.Print.*;

public class MapOfList {
    public static Map<Person, List<? extends Pet>> petPeople = new HashMap<Person, List<? extends Pet>>();

    static {
        petPeople.put(new Person("Dawn"), Arrays.asList(new Cymric("Molly"), new Mutt("Spot")));
        petPeople.put(new Person("Kate"), Arrays.asList(new Cat("Shelly"), new Cat("Spot1"), new Dog("hehe")));
        petPeople.put(new Person("Marrin"), Arrays.asList(new Pug("Molly is a big shit"), new Cat("Pinkist"), new Cat("Standrad for the reat")));
        petPeople.put(new Person("Luke"), Arrays.asList(new Cymric("Molly"), new Mutt("Spot")));
    }
    public static void main(String[] args){
        print("People: "+petPeople.keySet());
        print("Pets: "+petPeople.values());
        for (Person person: petPeople.keySet()){
            print(person + "has: ");
            for (Pet pet :petPeople.get(person)){
                print("  "+pet);
            }
        }
    }
}
