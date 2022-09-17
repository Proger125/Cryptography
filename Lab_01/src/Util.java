import java.util.*;

public class Util {

    static double getFrequency(int amount, int total) {
        return (double) amount / (double) total;
    }
    static <K extends Comparable<K>, V extends Comparable<V>>
    Map<K, V> sortMap(Map<K, V> unsortedMap, final boolean asc)
    {
        List<Map.Entry<K, V>> list = new LinkedList<>(unsortedMap.entrySet());

        list.sort((o1, o2) -> {
            if (asc) {
                return o1.getValue().compareTo(o2.getValue());
            } else {
                return o2.getValue().compareTo(o1.getValue());
            }
        });

        Map<K, V> sortedMap = new LinkedHashMap<>();
        for (Map.Entry<K, V> entry : list)
        {
            sortedMap.put(entry.getKey(), entry.getValue());
        }
        return sortedMap;
    }
}
