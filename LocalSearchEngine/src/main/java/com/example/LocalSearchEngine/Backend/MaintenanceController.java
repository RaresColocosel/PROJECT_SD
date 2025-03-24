package com.example.LocalSearchEngine.Backend;

import com.example.LocalSearchEngine.Backend.ServiceClass;
import com.example.LocalSearchEngine.Domain.Database.DatabaseHandler;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/maintenance")
public class MaintenanceController {

    private final DatabaseHandler dbHandler;

    @Autowired
    public MaintenanceController(DatabaseHandler dbHandler) {
        this.dbHandler = dbHandler;
    }

    @GetMapping("/clear")
    public String clearTable() {
        dbHandler.clearDatabase();
        return "file_index table cleared.";
    }
}
