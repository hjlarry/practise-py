package com.algorithms.charpter1_1;

import com.princeton.StdOut;

public class Ex11_13 {
    private static void printMatrix(boolean[][] matrix) {
        StdOut.println();
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                StdOut.print(i);
                StdOut.print("--");
                StdOut.print(j);
                StdOut.print("-->");
                if (matrix[i][j]) {
                    StdOut.print("*");
                } else {
                    StdOut.print(" ");
                }
                StdOut.println();
            }
        }
    }

    private static void printTransposedMatrix(int[][] matrix) {
        for (int i = 0; i < matrix[0].length; i++) {
            for (int j = 0; j < matrix.length; j++) {
                StdOut.println(matrix[j][i]);
            }
        }
    }

    public static void main(String[] args) {
        boolean[][] a = {{true, false, true}, {false, true, false}};
        printMatrix(a);

        int[][] b = {{100, 300, 500}, {10, 50, 90},};
        printTransposedMatrix(b);
    }
}
