package com.example.LocalSearchEngine.Backend;

import com.example.LocalSearchEngine.Backend.ServiceClass;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/indexer")
public class IndexController {

    private final ServiceClass serviceClass;

    @Autowired
    public IndexController(ServiceClass serviceClass) {
        this.serviceClass = serviceClass;
    }

    // Using a GET request with a path variable "/indexer/initialize/{directory}"
    // e.g. GET http://localhost:8080/indexer/initialize?directory=E:/LocalSearchEngine
    @GetMapping("/initialize")
    public ResponseEntity<String> reindex(@RequestParam String directory) {
        serviceClass.indexDirectory(directory);
        String msg = "Incremental indexing started for directory: " + directory;
        return ResponseEntity.ok(msg);
    }
}
