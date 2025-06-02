# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] – 2025-04-28
- Added:  
  - Image gallery widget to display all image‐type search results.  
  - Log viewer widget to preview up to 50 lines from any `.log` files in the result set.  
  - Word count widget showing total words across text files in results.  
  - Directory stats widget showing number of distinct directories in results.   
  - Implement spell corrector based on Norvig’s `big.txt` approach.  
  - Enhanced `search_service.py` so that `cache_info()` returns a simple dictionary (`hits`, `misses`, `currsize`, `maxsize`).  


## [0.1.0] – 2025-03-15
- Initial skeleton:  
  - `app.py` with basic Flask routes: “/” and “/search”.  
  - `DatabaseHandler` storing `file_index` and `search_history` tables in PostgreSQL.  
  - `FileCrawler` and `FileIndexer` storing file content, file type, last modified, etc.  
  - `QueryParser` that splits “path:…” and “content:…” qualifiers.  
  - `RankingService` doing a simple term‐count ranking.  
  - Basic “search” HTML template showing results with file name and preview.  