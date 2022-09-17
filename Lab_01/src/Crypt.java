import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.AbstractMap;
import java.util.LinkedHashMap;
import java.util.Map;

public class Crypt {
    static final int ALPHABET_SIZE = 26;

    private static final Map<Integer, Double> ENGLISH_LETTERS_FREQUENCY = Map.ofEntries(
            new AbstractMap.SimpleEntry<>(0, 0.08167),
            new AbstractMap.SimpleEntry<>(1, 0.01492),
            new AbstractMap.SimpleEntry<>(2, 0.02782),
            new AbstractMap.SimpleEntry<>(3, 0.04253),
            new AbstractMap.SimpleEntry<>(4, 0.12702),
            new AbstractMap.SimpleEntry<>(5, 0.0228),
            new AbstractMap.SimpleEntry<>(6, 0.02015),
            new AbstractMap.SimpleEntry<>(7, 0.06094),
            new AbstractMap.SimpleEntry<>(8, 0.06966),
            new AbstractMap.SimpleEntry<>(9, 0.00153),
            new AbstractMap.SimpleEntry<>(10, 0.00772),
            new AbstractMap.SimpleEntry<>(11, 0.04025),
            new AbstractMap.SimpleEntry<>(12, 0.02406),
            new AbstractMap.SimpleEntry<>(13, 0.06749),
            new AbstractMap.SimpleEntry<>(14, 0.07507),
            new AbstractMap.SimpleEntry<>(15, 0.01929),
            new AbstractMap.SimpleEntry<>(16, 0.00095),
            new AbstractMap.SimpleEntry<>(17, 0.05987),
            new AbstractMap.SimpleEntry<>(18, 0.06327),
            new AbstractMap.SimpleEntry<>(19, 0.09056),
            new AbstractMap.SimpleEntry<>(20, 0.02758),
            new AbstractMap.SimpleEntry<>(21, 0.00978),
            new AbstractMap.SimpleEntry<>(22, 0.0236),
            new AbstractMap.SimpleEntry<>(23, 0.0015),
            new AbstractMap.SimpleEntry<>(24, 0.01974),
            new AbstractMap.SimpleEntry<>(25, 0.00074)
    );

    static String vigenereCryptAnalyse(String[] streams)
    {
        Text[] cosets = new Text[streams.length];
        int[] keys = new int[streams.length];
        int[] letters = new int[streams.length];

        for (int i = 0; i < streams.length; i++)
        {
            cosets[i] = new Text(streams[i]);
            keys[i] = caesarCryptAnalyse(cosets[i]);

            letters[i] = 'a' + keys[i];
            letters[i] = normalizeLetter( letters[i] );
        }

        StringBuilder key = new StringBuilder();

        for (int letter : letters)
        {
            key.append((char) letter);
        }
        return key.toString();
    }

    static int caesarCryptAnalyse(Text cipherText)
    {
        float[] deviation = new float[ALPHABET_SIZE];
        Map<Integer, Float> deviationMap = new LinkedHashMap<>();
        for (int s = 0; s < ALPHABET_SIZE; s++)
        {
            for (int l = 0; l < ALPHABET_SIZE; l++)
            {
                deviation[s] += Math.abs(
                        ENGLISH_LETTERS_FREQUENCY.get(l)
                                - Util.getFrequency(cipherText.getLetterCount((l + s) % ALPHABET_SIZE),
                                cipherText.getTotalLetters()));
            }
            deviationMap.put(s, deviation[s]);
        }
        deviationMap = Util.sortMap(deviationMap, true);
        return (Integer) deviationMap.keySet().toArray()[0];
    }


    public static void encrypt(File fileToEncrypt, File encryptedFile, String key)
    {
        try
        {
            FileReader reader = new FileReader(fileToEncrypt);
            FileWriter writer = new FileWriter(encryptedFile);
            int ch;
            int chNum = 0;
            int[] shifts = breakDownKey(key);

            while ((ch = reader.read()) != -1)
            {
                ch = Character.toLowerCase(ch);
                if (ch < 'a' || ch > 'z')
                {
                    writer.write(ch);
                    continue;
                }

                int encryptedCh = ch + shifts[chNum % key.length()];
                encryptedCh = normalizeLetter(encryptedCh);

                writer.write(encryptedCh);
                chNum++;
            }

            reader.close();
            writer.flush();
            writer.close();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    static String[] breakDownCipher(String cipher, int keyLength)
    {
        String[] streams = new String[keyLength];
        int numOfCh = 0;

        for (char ch : cipher.toCharArray())
        {
            streams[numOfCh % keyLength] += Character.toString(ch);
            numOfCh++;
        }
        return streams;
    }

    private static int normalizeLetter(int letter)
    {
        while (letter < 'a')
        {
            letter += ALPHABET_SIZE;
        }
        while (letter > 'z')
        {
            letter -= ALPHABET_SIZE;
        }
        return letter;
    }

    private static int[] breakDownKey(String key)
    {
        int[] shifts = new int[key.length()];

        for (int i = 0; i < key.length(); i++)
        {
            shifts[i] = key.charAt(i) - 'a';
        }

        return shifts;
    }
}
