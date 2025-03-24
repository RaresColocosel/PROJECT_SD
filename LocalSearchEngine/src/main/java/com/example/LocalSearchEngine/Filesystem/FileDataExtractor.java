package com.example.LocalSearchEngine.Filesystem;

import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.sax.BodyContentHandler;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
public class FileDataExtractor {

    public static String extractText(File file) {
        String extension = extractTxtType(file);
        if ("plain".equalsIgnoreCase(extension)) {
            try {
                return Files.readString(Paths.get(file.getAbsolutePath()), StandardCharsets.UTF_8);
            } catch (IOException e) {
                System.err.println("Error reading plain text file: " + file.getAbsolutePath() + " => " + e.getMessage());
                return "";
            }
        }
        try (InputStream stream = new FileInputStream(file)) {
            BodyContentHandler handler = new BodyContentHandler(-1);
            Metadata metadata = new Metadata();
            AutoDetectParser parser = new AutoDetectParser();
            ParseContext context = new ParseContext();
            parser.parse(stream, handler, metadata, context);
        } catch (Exception e) {
            System.err.println("Error processing " + file.getAbsolutePath() + " => " + e.getMessage());
            return "";
        }
        return "";
    }

    public static String extractTxtType(File file) {
        String name = file.getName().toLowerCase();
        if (name.endsWith(".txt")) {
            return "plain";
        }
        return "";
    }

}