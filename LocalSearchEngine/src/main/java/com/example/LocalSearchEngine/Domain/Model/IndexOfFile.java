package com.example.LocalSearchEngine.Domain.Model;

import java.time.LocalDateTime;


public class IndexOfFile {

    private Long id;
    private String fileName;
    private String filePath;
    private String fileType;
    private String fileContent;
    private LocalDateTime indexedAt;

    public IndexOfFile() {}

    public IndexOfFile(Long id, String fileName, String filePath,
                       String fileType, String fileContent,
                       LocalDateTime indexedAt) {
        this.id = id;
        this.fileName = fileName;
        this.filePath = filePath;
        this.fileType = fileType;
        this.fileContent = fileContent;
        this.indexedAt = indexedAt;
    }

    // Getters / Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getFileName() { return fileName; }
    public void setFileName(String fileName) { this.fileName = fileName; }

    public String getFilePath() { return filePath; }
    public void setFilePath(String filePath) { this.filePath = filePath; }

    public String getFileType() { return fileType; }
    public void setFileType(String fileType) { this.fileType = fileType; }

    public String getFileContent() { return fileContent; }
    public void setFileContent(String fileContent) { this.fileContent = fileContent; }

    public LocalDateTime getIndexedAt() { return indexedAt; }
    public void setIndexedAt(LocalDateTime indexedAt) { this.indexedAt = indexedAt; }
}
