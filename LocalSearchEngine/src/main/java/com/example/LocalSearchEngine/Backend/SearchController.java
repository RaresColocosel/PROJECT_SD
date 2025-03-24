package com.example.LocalSearchEngine.Backend;

import com.example.LocalSearchEngine.Domain.Model.IndexOfFile;
import com.example.LocalSearchEngine.Domain.Database.DatabaseHandler;
import com.example.LocalSearchEngine.Backend.ServiceClass;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@RestController
@RequestMapping("/api")
public class SearchController {

    private final ServiceClass serviceClass;
    private final DatabaseHandler databaseHandler;

    @Autowired
    public SearchController(ServiceClass serviceClass, DatabaseHandler databaseHandler) {
        this.serviceClass = serviceClass;
        this.databaseHandler = databaseHandler;
    }

    @PostMapping("/index")
    public String indexDirectory(@RequestParam String path) {
        serviceClass.indexDirectory(path);
        return "Indexing complete for directory: " + path;
    }

    @GetMapping("/search")
    public List<FileSearchResult> searchFiles(@RequestParam String query) {
        List<IndexOfFile> results = databaseHandler.searchFiles(query);
        List<FileSearchResult> response = new ArrayList<>();

        for (IndexOfFile file : results) {
            String[] lines = file.getFileContent().split("\r?\n");
            List<String> preview = Arrays.asList(lines).subList(0, Math.min(3, lines.length));

            response.add(new FileSearchResult(
                    file.getFileName(),
                    file.getFilePath(),
                    preview
            ));
        }

        return response;
    }

    public static class FileSearchResult {
        private String fileName;
        private String filePath;
        private List<String> preview;

        public FileSearchResult(String fileName, String filePath, List<String> preview) {
            this.fileName = fileName;
            this.filePath = filePath;
            this.preview = preview;
        }

        public String getFileName() {
            return fileName;
        }

        public String getFilePath() {
            return filePath;
        }

        public List<String> getPreview() {
            return preview;
        }
    }
}