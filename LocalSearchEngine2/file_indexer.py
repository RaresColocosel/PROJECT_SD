import os
from datetime import datetime
from file_crawler import FileCrawler
from file_data_extractor import FileDataExtractor

class FileIndexer:
    def __init__(self, db_handler):
        self.db = db_handler
        self.crawler = FileCrawler()

    def index_directory(self, root_directory):
        files = self.crawler.crawl_directory(root_directory)
        for fp in files:
            try:
                st = os.stat(fp)
                indexed_at = datetime.fromtimestamp(st.st_mtime).isoformat()
                accessed   = datetime.fromtimestamp(st.st_atime).isoformat()
                size       = st.st_size
                depth      = fp.count(os.sep)
                content    = FileDataExtractor.extract_text(fp)
                file_type  = FileDataExtractor.extract_type(fp)
                fi = {
                    "name": os.path.basename(fp),
                    "path": fp,
                    "type": file_type,
                    "content": content,
                    "indexed_at": indexed_at,
                    "size": size,
                    "accessed": accessed,
                    "depth": depth,
                    "index_score": None
                }
                self.db.insert_file(fi)
            except Exception:
                continue
