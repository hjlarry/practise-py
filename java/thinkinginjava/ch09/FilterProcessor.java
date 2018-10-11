package ch09;

class FilterAdapter implements Processor{
    Filter filter;
    public FilterAdapter(Filter filter){
        this.filter = filter;
    }
    public String name(){
        return filter.name();
    }
    public Waveform process(Object input){
        return filter.process((Waveform) input);
    }
}

public class FilterProcessor {
    public static void main(String[] args){
        Waveform w = new Waveform();
        Apply.process(new FilterAdapter(new LowPass(1.5)), w);
        Apply.process(new FilterAdapter(new HighPass(4.5)), w);
        Apply.process(new FilterAdapter(new BandPass(2.0,3.1)), w);
    }
}
