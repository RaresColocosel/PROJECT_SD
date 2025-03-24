package com.example.LocalSearchEngine.Backend;

import com.example.LocalSearchEngine.Filesystem.Indexer.FileIndexer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ServiceClass {

    private final FileIndexer fileIndexer;

    @Autowired
    public ServiceClass(FileIndexer fileIndexer) {
        this.fileIndexer = fileIndexer;
    }

    public void indexDirectory(String directory) {
        fileIndexer.indexFilesIncrementally(directory);
    }
}