package com.example.LocalSearchEngine.Filesystem.Indexer;

import com.example.LocalSearchEngine.Domain.Database.DatabaseHandler;
import com.example.LocalSearchEngine.Domain.Model.IndexOfFile;
import com.example.LocalSearchEngine.Filesystem.FileDataExtractor;
import com.example.LocalSearchEngine.Filesystem.FileCrawler.FileCrawler;
import org.springframework.stereotype.Component;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.attribute.BasicFileAttributes;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.List;

@Component
public class FileIndexer {

    private final FileCrawler fileCrawler;
    private final DatabaseHandler databaseHandler;

    public FileIndexer(FileCrawler fileCrawler, DatabaseHandler databaseHandler) {
        this.fileCrawler = fileCrawler;
        this.databaseHandler = databaseHandler;
    }

    public void indexFilesIncrementally(String rootDirectory) {
        DatabaseHandler.writeInFile("Starting incremental indexing for: " + rootDirectory);

        List<File> files;
        try {
            files = fileCrawler.crawlDirectory(rootDirectory);
        } catch (Exception e) {
            DatabaseHandler.writeInFile("Error crawling directory: " + e.getMessage());
            return;
        }

        DatabaseHandler.writeInFile("FileCrawler found " + files.size() + " files.");

        List<IndexOfFile> newFiles = new ArrayList<>();
        List<IndexOfFile> updatedFiles = new ArrayList<>();

        for (File file : files) {
            try {
                BasicFileAttributes attrs = Files.readAttributes(file.toPath(), BasicFileAttributes.class);
                LocalDateTime lastModified = Instant.ofEpochMilli(attrs.lastModifiedTime().toMillis())
                        .atZone(ZoneId.systemDefault()).toLocalDateTime();
                IndexOfFile existing = databaseHandler.findByPath(file.getAbsolutePath());
                if (existing != null) {
                    // If lastModified is same, skip
                    if (existing.getIndexedAt() != null && existing.getIndexedAt().equals(lastModified)) {
                        continue;
                    }
                    existing.setFileName(file.getName());
                    existing.setFilePath(file.getAbsolutePath());
                    existing.setFileType(FileDataExtractor.extractTxtType(file));
                    existing.setIndexedAt(lastModified);
                    updatedFiles.add(existing);
                } else {
                    IndexOfFile newFile = new IndexOfFile();
                    newFile.setFileName(file.getName());
                    newFile.setFilePath(file.getAbsolutePath());
                    newFile.setFileContent(FileDataExtractor.extractText(file));
                    newFile.setFileType(FileDataExtractor.extractTxtType(file));
                    newFile.setIndexedAt(lastModified);
                    newFiles.add(newFile);
                }
            } catch (Exception e) {
                DatabaseHandler.writeInFile("Error indexing file " + file.getAbsolutePath() + " => " + e.getMessage());
            }
        }

        if (!newFiles.isEmpty()) {
            databaseHandler.insertAll(newFiles);
            DatabaseHandler.writeInFile("Inserted " + newFiles.size() + " new file(s).");
        }
        if (!updatedFiles.isEmpty()) {
            databaseHandler.updateAll(updatedFiles);
            DatabaseHandler.writeInFile("Updated " + updatedFiles.size() + " existing file(s).");
        }

        DatabaseHandler.writeInFile("Finished incremental indexing for: " + rootDirectory);
    }
}
