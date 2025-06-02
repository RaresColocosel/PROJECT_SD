import os

class FileCrawler:
    def crawl_directory(self, root_dir):
        all_files = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for fname in filenames:
                fullpath = os.path.join(dirpath, fname)
                all_files.append(fullpath)
        return all_files
