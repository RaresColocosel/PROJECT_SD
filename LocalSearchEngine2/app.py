import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import threading
from config import Config
from database_handler import DatabaseHandler
from file_indexer import FileIndexer
from query_parser import QueryParser
from ranking_service import RankingService

# Load .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

db = DatabaseHandler()
cfg=Config()
indexer = FileIndexer(db, cfg)
parser = QueryParser()
ranker = RankingService()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def do_index():
    directory = request.form.get('directory')
    if not directory or not os.path.isdir(directory):
        flash('Invalid directory', 'error')
        return redirect(url_for('index'))
    threading.Thread(target=indexer.index_directory, args=directory, daemon=True).start()
    flash(f'Started indexing {directory}', 'info')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query','')
    paths, contents = parser.parse(query)
    rows = db.list_all()

    def norm(fp):
        return fp.replace('\\', '/').lower()

    for p in paths:
        q = p.replace('\\', '/').lower()
        rows = [r for r in rows if q in norm(r['file_path'])]

    for c in contents:
        cc = c.lower()
        rows = [r for r in rows if cc in (r['file_content'] or '').lower()]

    results = ranker.rank(rows, contents)

    for r in results:
        lines = (r.get('file_content') or '').splitlines()
        r['preview'] = lines[:3]

    db.record_query(query)

    return render_template('results.html', results=results, query=query)
@app.route('/suggest', methods=['GET'])
def suggest():
    prefix = request.args.get('prefix','')
    return jsonify(db.suggest(prefix))

if __name__ == '__main__':
    FLASK_HOST = os.getenv('FLASK_HOST')
    FLASK_PORT = os.getenv('FLASK_PORT')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
