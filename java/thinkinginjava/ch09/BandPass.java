package ch09;

public class BandPass extends Filter {
    double lowoff, highoff;
    public BandPass(double lowoff, double highoff){
        this.lowoff = lowoff;
        this.highoff = highoff;
    }
    public Waveform process(Waveform input){
        return input;
    }
}
