package utils;

public class Range {
    public static int[] range(int n) {
        int[] result = new int[n];
        for (int i = 0; i < n; i++) {
            result[i] = i;
        }
        return result;
    }

    public static int[] range(int start, int end) {
        int len = end - start;
        int[] result = new int[len];
        for (int i = 0; i < len; i++) {
            result[i] = start + i;
        }
        return result;
    }

    public static int[] range(int start, int end, int step) {
        int len = (end - start)/step;
        int[] result = new int[len];
        for (int i = 0; i < len; i++) {
            result[i] = start + step * i;
        }
        return result;
    }
}
