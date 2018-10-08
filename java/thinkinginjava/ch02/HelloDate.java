package ch02;

import java.util.Date;

public class HelloDate {
    public static void main(String[] args) {
        System.out.println("Hello. It`s");
        System.out.println(new Date());
        System.getProperties().list(System.out);
        System.out.println(System.getProperty("user.name"));
        System.out.println(System.getProperty("java.library.path"));
    }
}