import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Kasiski {

    private static final int MIN_FACTOR = 2;
    private static final int MAX_FACTOR = 10;

    public static int test(String cipher) {
        Map<String, Integer> repeatingWords = getRepeatingWords(cipher);
        Map<String, Integer> distances = getDistances(cipher, repeatingWords);
        int[] factorCounter = factorizeDistances(distances);
        return findKeyLength(factorCounter);
    }

    private static Map<String, Integer> getRepeatingWords(String cipher) {
        Map<String, Integer> repeatingWords = new LinkedHashMap<>();
        String regex = String.format("(\\S{%d,%d})(?=.*?\\1)", MIN_FACTOR, MAX_FACTOR);
        Matcher m = Pattern.compile(regex).matcher(cipher);
        while (m.find()) {
            if (!repeatingWords.containsKey(m.group())) {
                repeatingWords.put(m.group(), m.start());
            }
        }
        return repeatingWords;
    }

    private static Map<String, Integer> getDistances(String cipher, Map<String, Integer> repeatingWords) {
        Map<String, Integer> distances = new LinkedHashMap<>();
        for (Map.Entry<String, Integer> entry : repeatingWords.entrySet()) {
            int distance = cipher.indexOf(entry.getKey(), entry.getValue() + entry.getKey().length()) - entry.getValue();
            distances.put(entry.getKey(), distance);
        }
        return distances;
    }

    private static int[] factorizeDistances(Map<String, Integer> distances) {
        int[] factorCounter = new int[MAX_FACTOR + 1];
        for (Map.Entry<String, Integer> entry : distances.entrySet()) {
            for (int i = MAX_FACTOR; i >= MIN_FACTOR; i--) {
                if (entry.getValue() % i == 0) {
                    factorCounter[i]++;
                }
            }
        }
        return factorCounter;
    }

    private static int findKeyLength(int[] factorCounter) {
        Map<Integer, Integer> factorMap = new LinkedHashMap<>();

        for (int i = MAX_FACTOR; i >= MIN_FACTOR; i--) {
            factorMap.put(i, factorCounter[i]);
        }
        factorMap = Util.sortMap(factorMap, false);
        return (Integer) factorMap.keySet().toArray()[ 0 ];
    }
}
