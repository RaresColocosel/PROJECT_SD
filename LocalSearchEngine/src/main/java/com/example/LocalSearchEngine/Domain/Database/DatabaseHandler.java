package com.example.LocalSearchEngine.Domain.Database;

import com.example.LocalSearchEngine.Domain.Model.IndexOfFile;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Repository
public class DatabaseHandler {

    private final JdbcTemplate jdbcTemplate;

    @Autowired
    public DatabaseHandler(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public void insertAll(List<IndexOfFile> files) {
        String sql = """
            INSERT INTO file_index 
                (file_name, file_path, file_type, file_content, indexed_at)
            VALUES 
                (?, ?, ?, ?, ?)
        """;
        List<Object[]> batchArgs = new ArrayList<>();
        for (IndexOfFile f : files) {
            batchArgs.add(new Object[]{
                    f.getFileName(),
                    f.getFilePath(),
                    f.getFileType(),
                    f.getFileContent(),
                    f.getIndexedAt()
            });
        }
        jdbcTemplate.batchUpdate(sql, batchArgs);
    }

    public void updateAll(List<IndexOfFile> files) {
        String sql = """
            UPDATE file_index
            SET file_name = ?, file_type = ?, file_content = ?, indexed_at = ?
            WHERE file_path = ?
        """;
        List<Object[]> batchArgs = new ArrayList<>();
        for (IndexOfFile f : files) {
            batchArgs.add(new Object[]{
                    f.getFileName(),
                    f.getFileType(),
                    f.getFileContent(),
                    f.getIndexedAt(),
                    f.getFilePath()
            });
        }
        jdbcTemplate.batchUpdate(sql, batchArgs);
    }

    public IndexOfFile findByPath(String filePath) {
        String sql = "SELECT * FROM file_index WHERE file_path = ?";
        List<IndexOfFile> results = jdbcTemplate.query(sql, new Mapper(), filePath);
        return results.isEmpty() ? null : results.get(0);
    }

    public List<IndexOfFile> searchFiles(String userInput) {
        String tsQuery = buildTsQuery(userInput);
        String sql = """
            SELECT *
            FROM file_index
            WHERE to_tsvector('english', coalesce(file_name,'') || ' ' || coalesce(file_content,'')) 
                  @@ to_tsquery('english', ?)
        """;
        return jdbcTemplate.query(sql, new Mapper(), tsQuery);
    }

    public List<IndexOfFile> searchAll() {
        String sql = "SELECT * FROM file_index";
        return jdbcTemplate.query(sql, new Mapper());
    }

    public void clearDatabase() {
        writeInFile("Resetting file_index table...");
        jdbcTemplate.update("DELETE FROM file_index");
        try {
            jdbcTemplate.execute("ALTER SEQUENCE file_index_id_seq RESTART WITH 1");
            writeInFile("Sequence file_index_id_seq reset to 1.");
        } catch (Exception e) {
            System.err.println("Error resetting sequence: " + e.getMessage());
        }
    }

    public static void writeInFile(String message) {
        String filename = "Process.txt";
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename, true))) {
            writer.write(message);
            writer.newLine();
            System.out.println("Wrote to " + filename + ": " + message);
        } catch (IOException e) {
            System.err.println("Error writing to file: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private String buildTsQuery(String userInput) {
        if (userInput == null || userInput.isBlank()) {
            return "";
        }
        String[] tokens = userInput.trim().split("\\s+");
        return String.join(" & ", tokens);
    }
}
