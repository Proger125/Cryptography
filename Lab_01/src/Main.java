import org.knowm.xchart.QuickChart;
import org.knowm.xchart.SwingWrapper;
import org.knowm.xchart.XYChart;

import java.io.*;
import java.util.List;
import java.util.Scanner;

public class Main {

    private static final List<String> PASSWORDS = List.of("clients", "beautys", "efforts", "bridges", "domains", "assists", "casuals", "courses", "actuals", "costlys");

    private static final List< List<String> > DIFFERENT_SIZE_PASSWORDS = List.of(
            List.of("cat", "dog", "ham", "cow", "dad", "far", "eve", "lam", "pip", "tax"),
            List.of("earth", "final", "hotel", "japan", "jones", "chair", "abuse", "ratio", "stone", "union"),
            List.of("balance", "anxious", "analyst", "compare", "exactly", "include", "loyalty", "massive", "natural", "predict"),
            List.of("abandoned", "babelized", "cabaletta", "dacoities", "ealdorman", "fabulated", "gablelike", "iarovised", "jabberers", "kabbalism"),
            List.of("abandonable", "babiroussas", "cabbagehead", "dactylology", "eagernesses", "gabbinesses", "haberdasher", "iceboatings", "jackerooing", "kabbalistic")
    );
    private static final String FILE_PATH = "file%s.txt";
    private static final String FILE_ENCRYPTED_PATH = "file%s_en.txt";

    public static void main(String[] args) {
        double[] probabilities = new double[PASSWORDS.size()];
        double[] filesSizes = new double[PASSWORDS.size()];
        int allAttacks = PASSWORDS.size();
        for (int i = 1; i < PASSWORDS.size() + 1; i++) {
            int successAttacks = 0;
            File sourceFile = new File(String.format(FILE_PATH, i));
            File destFile = new File(String.format(FILE_ENCRYPTED_PATH, i));
            filesSizes[i - 1] = sourceFile.length();
            for (var password : PASSWORDS) {
                if (isKasiskiAttackSuccess(sourceFile, destFile, password)) {
                    successAttacks++;
                }
            }
            probabilities[i - 1] = calcProbability(successAttacks, allAttacks);
        }
        XYChart chart1 = QuickChart.getChart("First chart", "File size", "Probability","series", filesSizes, probabilities);
        new SwingWrapper(chart1).displayChart();
        probabilities = new double[DIFFERENT_SIZE_PASSWORDS.size()];
        double[] passwordsLength = new double[DIFFERENT_SIZE_PASSWORDS.size()];
        File sourceFile = new File(String.format(FILE_PATH, 5));
        File destFile = new File(String.format(FILE_ENCRYPTED_PATH, 5));
        int i = 0;
        for (var passwordList : DIFFERENT_SIZE_PASSWORDS) {
            allAttacks = passwordList.size();
            passwordsLength[i] = passwordList.get(0).length();
            int successAttacks = 0;
            for (var password : passwordList) {
                if (isKasiskiAttackSuccess(sourceFile, destFile, password)) {
                    successAttacks++;
                }
            }
            probabilities[i] = calcProbability(successAttacks, allAttacks);
            i++;
        }
        XYChart chart2 = QuickChart.getChart("Second chart", "Word length", "Probability", "series", passwordsLength, probabilities);
        new SwingWrapper(chart2).displayChart();
    }

    private static double calcProbability(double successAttacks, double allAttacks) {
        return successAttacks / allAttacks;
    }

    private static boolean isKasiskiAttackSuccess(File sourceFile, File destFile, String password){
        Crypt.encrypt(sourceFile, destFile, password);
        Text text = new Text(destFile);
        String cipher = text.getText();
        int keyLength = Kasiski.test(cipher);
        String[] streams = Crypt.breakDownCipher(cipher, keyLength);
        String keyword = Crypt.vigenereCryptAnalyse(streams);
        return keyword.equals(password);
    }

    private static String getPassword() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter password to encrypt Vigenere cipher with: ");

        String password = scanner.nextLine();
        while (!password.matches("[a-zA-Z]+")) {
            System.out.println("Please enter a valid password! (Only letters allowed) : ");
            password = scanner.nextLine();
        }
        password = password.trim();
        password = password.toLowerCase();
        password = password.replaceAll("\\s+", "");
        scanner.close();
        return password;
    }
}