import java.util.Scanner;

public class Checksum {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int sum = 0;
        while(sc.hasNextLine()) {
            String line = sc.nextLine();
            Scanner numbers = new Scanner(line);
            int min = Integer.MAX_VALUE;
            int max = Integer.MIN_VALUE;
            while(numbers.hasNextInt()) {
                int i = numbers.nextInt();
                if(i < min) {
                    min = i;
                }
                if(i > max) {
                    max = i;
                }
                //System.out.printf("%d\t%d\t%d\t%d\t%d%n", i, min, max, max - min, sum);
            }
            int diff = max - min;
            sum += diff;
        }
        System.out.println(sum);
    }
}

