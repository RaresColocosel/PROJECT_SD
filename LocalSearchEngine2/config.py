import os

class Config:
    def __init__(self):
        self.report_format = os.getenv('INDEX_REPORT_FORMAT', 'text')
        self.report_path   = os.getenv('INDEX_REPORT_PATH', 'index_report.txt')
        self.prioritized_extensions = os.getenv('PRIORITIZED_EXT', '.py,.md').split(',')