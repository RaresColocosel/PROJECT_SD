package com.example.LocalSearchEngine.Domain.Database;

import com.example.LocalSearchEngine.Domain.Model.IndexOfFile;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.lang.NonNull;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.time.LocalDateTime;

public class  Mapper implements RowMapper<IndexOfFile> {

    @Override
    public @NonNull IndexOfFile mapRow(@NonNull ResultSet rs, int rowNum) throws SQLException {
        IndexOfFile ioFile = new IndexOfFile();
        ioFile.setId(rs.getLong("id"));
        ioFile.setFileName(rs.getString("file_name"));
        ioFile.setFilePath(rs.getString("file_path"));
        ioFile.setFileType(rs.getString("file_type"));
        ioFile.setFileContent(rs.getString("file_content"));
        Timestamp ts = rs.getTimestamp("indexed_at");
        LocalDateTime indexedAt = (ts != null) ? ts.toLocalDateTime() : null;
        ioFile.setIndexedAt(indexedAt);
        return ioFile;
    }
}
