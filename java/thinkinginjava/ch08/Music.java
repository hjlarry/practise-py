package ch08;

import static utils.Print.*;

class Instrument {
    void play(Note n) {
        print("Instrument.play()" + n);
    }

    String what() {
        return "Instrument";
    }

    void adjust() {
        print("adjust Instrument");
    }

    public String toString(){
        return what();
    }
}

class Wind extends Instrument {
    void play(Note n) {
        print("Wind.play()" + n);
    }

    String what() {
        return "Wind";
    }

    void adjust() {
        print("adjust Wind");
    }
}

class Percission extends Instrument {
    void play(Note n) {
        print("Percission.play()" + n);
    }

    String what() {
        return "Percission";
    }

    void adjust() {
        print("adjust Percission");
    }
}

class Stringed extends Instrument {
    void play(Note n) {
        print("Stringed.play()" + n);
    }

    String what() {
        return "Stringed";
    }

    void adjust() {
        print("adjust Stringed");
    }
}

class Brass extends Wind {
    @Override
    void play(Note n) {
        print("Brass.play()" + n);
    }

    void adjust() {
        print("adjust Brass");
    }
}

class Woodwind extends Wind {
    void play(Note n) {
        print("Woodwind.play()" + n);
    }

    String what() {
        return "Woodwind";
    }
}

// 多态
public class Music {
    public static void tune(Instrument instrument) {
        instrument.play(Note.MIDDLE_C);
        System.out.println(instrument);
    }

    public static void tune_all(Instrument[] instruments) {
        for (Instrument instrument : instruments) {
            tune(instrument);
        }
    }

    public static void main(String[] args) {
        Instrument[] instruments = {
                new Wind(), new Percission(), new Stringed(), new Brass(), new Woodwind()
        };
        tune_all(instruments);
    }
}
