import java.io.*;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;

class FruitFallAnalyzer {

    public static void analyzeFall(int houseStart, int houseEnd, int appleTreePos, int orangeTreePos,
                                   List<Integer> appleDistances, List<Integer> orangeDistances) {
        long applesOnHouse = appleDistances.stream()
                .map(d -> d + appleTreePos)
                .filter(pos -> pos >= houseStart && pos <= houseEnd)
                .count();

        long orangesOnHouse = orangeDistances.stream()
                .map(d -> d + orangeTreePos)
                .filter(pos -> pos >= houseStart && pos <= houseEnd)
                .count();

        System.out.println(applesOnHouse);
        System.out.println(orangesOnHouse);
    }
}

public class code1 {
    public static void main(String[] args) throws IOException {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in))) {

            List<Integer> houseRange = Arrays.stream(reader.readLine().split(" "))
                    .map(Integer::parseInt).collect(Collectors.toList());

            List<Integer> treePositions = Arrays.stream(reader.readLine().split(" "))
                    .map(Integer::parseInt).collect(Collectors.toList());

            reader.readLine(); // skip the count line as it's not needed

            List<Integer> apples = Arrays.stream(reader.readLine().split(" "))
                    .map(Integer::parseInt).collect(Collectors.toList());

            List<Integer> oranges = Arrays.stream(reader.readLine().split(" "))
                    .map(Integer::parseInt).collect(Collectors.toList());

            FruitFallAnalyzer.analyzeFall(
                    houseRange.get(0),
                    houseRange.get(1),
                    treePositions.get(0),
                    treePositions.get(1),
                    apples,
                    oranges
            );
        }
    }
}
