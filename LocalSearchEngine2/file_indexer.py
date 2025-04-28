import os
from datetime import datetime
from file_crawler import FileCrawler
from database_handler import DatabaseHandler
from config import Config

class FileIndexer:

    def __init__(self, db: DatabaseHandler, cfg: Config, crawler: FileCrawler = None):
        self.db = db
        self.cfg = cfg
        self.crawler = crawler or FileCrawler()
        self.report = []

    def compute_index_score(self, path, content, depth):
        score = 1.0 / (depth + 1)
        score += 1.0 / (len(content) + 1)
        ext = os.path.splitext(path)[1]
        if ext in self.cfg.prioritized_extensions:
            score *= 2
        return score

    def index_directory(self, root):
        self.report.clear()
        count = 0
        for fp in self.crawler.crawl(root):
            stat = os.stat(fp)
            depth = fp.replace(root, '').count(os.sep)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().replace('\x00', '')
            except Exception:
                content = ''
            fi = {
                'name': os.path.basename(fp),
                'path': fp,
                'type': os.path.splitext(fp)[1].lstrip('.') or None,
                'content': content,
                'indexed_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'size': stat.st_size,
                'accessed': datetime.fromtimestamp(stat.st_atime).isoformat(),
                'depth': depth,
                'index_score': self.compute_index_score(fp, content, depth)
            }
            self.db.insert_file(fi)
            self.report.append((fp, fi['index_score']))
            count += 1

        if self.cfg.report_format == 'json':
            import json
            with open(self.cfg.report_path, 'w') as f:
                json.dump({'count': count, 'files': [ {'path':p,'score':s} for p,s in self.report ]}, f)
        else:
            with open(self.cfg.report_path, 'w') as f:
                f.write(f"Indexed {count} files\n")
                for p,s in self.report:
                    f.write(f"{p}: {s}\n")
