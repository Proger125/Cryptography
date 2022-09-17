import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class Text {
    private final int[] letterCounters;
    private int totalLetters;

    private final String text;

    public Text(File file) {
        this.letterCounters = new int[Crypt.ALPHABET_SIZE];
        this.totalLetters = 0;
        try(FileReader reader = new FileReader(file)) {
            int ch;
            StringBuilder result = new StringBuilder();
            while ((ch = reader.read()) != -1)
            {
                ch = Character.toLowerCase(ch);
                if (ch < 'a' || ch > 'z')
                {
                    continue;
                }
                this.letterCounters[ch - 'a']++;
                this.totalLetters++;
                result.append((char) ch);
            }
            this.text = result.toString();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public Text(String text) {
        this.letterCounters = new int[Crypt.ALPHABET_SIZE];
        this.totalLetters = 0;
        StringBuilder result = new StringBuilder();
        for (char ch : text.toCharArray()) {
            ch = Character.toLowerCase(ch);
            if (ch < 'a' || ch > 'z')
            {
                continue;
            }
            this.letterCounters[ch - 'a']++;
            this.totalLetters++;
            result.append((char) ch);
        }
        this.text = result.toString();
    }

    public String getText() {
        return this.text;
    }

    public int getLetterCount(int letter) {
        return this.letterCounters[letter];
    }
    public int getTotalLetters() {
        return this.totalLetters;
    }
}
