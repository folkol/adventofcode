import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashSet;

public class a {
    public static void main(String[] args) throws IOException {
        char[][] seafloor = parseInput();

        var step = 0;
        var willMove = new HashSet<Integer>();
        while (true) {
            step++;
            willMove.clear();
            int height = seafloor.length;
            var numMoved = 0;
            for (var row = 0; row < height; row++) {
                int width = seafloor[row].length;
                for (var col = 0; col < width; col++) {
                    if (seafloor[row][col] == '>' && seafloor[row][(col + 1) % width] == '.') {
                        willMove.add(row * width + col);
                        numMoved++;
                    }
                }
            }
            for (var row = 0; row < height; row++) {
                int width = seafloor[row].length;
                for (var col = 0; col < width; col++) {
                    if (willMove.contains(row * width + col)) {
                        seafloor[row][col] = '.';
                        seafloor[row][(col + 1) % width] = '>';
                    }
                }
            }
            willMove.clear();
            for (var row = 0; row < height; row++) {
                int width = seafloor[row].length;
                for (var col = 0; col < width; col++) {
                    if (seafloor[row][col] == 'v' && seafloor[(row + 1) % height][col] == '.') {
                        willMove.add(row * width + col);
                        numMoved++;
                    }
                }
            }
            for (var row = 0; row < height; row++) {
                int width = seafloor[row].length;
                for (var col = 0; col < width; col++) {
                    if (willMove.contains(row * width + col)) {
                        seafloor[row][col] = '.';
                        seafloor[(row + 1) % height][col] = 'v';
                    }
                }
            }
            if (numMoved == 0) {
                System.out.println(step);
                break;
            }
        }
    }

    private static char[][] parseInput() throws IOException {
        var lines = Files.readAllLines(Paths.get("input.dat"));
        var seafloor = new char[lines.size()][lines.get(0).length()];
        for (int row = 0; row < lines.size(); row++) {
            var line = lines.get(row);
            for (var col = 0; col < line.length(); col++) {
                seafloor[row][col] = line.charAt(col);
            }
        }
        return seafloor;
    }
}
