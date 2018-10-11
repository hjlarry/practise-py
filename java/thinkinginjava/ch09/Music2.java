package ch09;

import static utils.Print.*;

import ch08.Note;

interface Instrument_in {
    int VALUE = 5; // static & final, compile time constants
    void play(Note n); // automatically public
    void adjust();
}

class Wind_in implements Instrument_in {
    public void play(Note n) {
        print("Wind.play()" + n + this);
    }

    public void adjust() {
        print("adjust Wind");
    }

    public String toString(){
        return "<Wind haha>";
    }
}

class Percission_in implements Instrument_in {
    public void play(Note n) {
        print("Percission.play()" + n);
    }

    public void adjust() {
        print("adjust Percission");
    }
}


class Brass2 extends Wind_in {
    @Override
    public void play(Note n) {
        print("Brass.play()" + n);
    }

    public void adjust() {
        print("adjust Brass");
    }

    public String toString(){
        return "<Brass2>";
    }
}

class Woodwind2 extends Wind_in {
    public String toString(){
        return "<Woodwind2>";
    }
}

public class Music2 {
    public static void tune(Instrument_in instrument) {
        instrument.play(Note.MIDDLE_C);
        System.out.println(instrument);
    }

    public static void tune_all(Instrument_in[] instruments) {
        for (Instrument_in instrument : instruments) {
            tune(instrument);
        }
    }

    public static void main(String[] args) {
        Instrument_in[] instruments = {
                new Wind_in(), new Percission_in(), new Brass2(), new Woodwind2()
        };
        tune_all(instruments);
    }
}
