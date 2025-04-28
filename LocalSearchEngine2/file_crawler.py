import os

class FileCrawler:
    def crawl(self, root):
        for dirpath, dirnames, filenames in os.walk(root):
            for fn in filenames:
                yield os.path.join(dirpath, fn)