package com.example.LocalSearchEngine.Filesystem.FileCrawler;

import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
@Component
public class FileCrawler {

    public List<File> crawlDirectory(String rootDir) throws IOException {
        List<File> txtFiles = new ArrayList<>();
        walkDirectory(new File(rootDir), txtFiles);
        return txtFiles;
    }

    private void walkDirectory(File dir, List<File> collector) {
        if (!dir.isDirectory()) {
            return;
        }
        File[] files = dir.listFiles();
        if (files == null) {
            return;
        }
        for (File f : files) {
            if (f.isDirectory()) {
                walkDirectory(f, collector);
            } else if (f.getName().toLowerCase().endsWith(".txt")) {
                collector.add(f);
            }
        }
    }
}
