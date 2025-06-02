import os
import threading
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from dotenv import load_dotenv

from database_handler import DatabaseHandler
from file_crawler import FileCrawler
from file_indexer import FileIndexer
from query_parser import QueryParser
from ranking_service import RankingService
from widgets import WidgetFactory
from spelling_corrector import NorvigCorrector, correct_query   # ← new import
from search_service import DatabaseSearchService, CachingSearchService
from facets import summarize_by_file_type, summarize_by_year, summarize_by_language

load_dotenv()

DICT_PATH = os.getenv("DICT_PATH", "big.txt")

corrector = NorvigCorrector(DICT_PATH)

db_handler    = DatabaseHandler()
parser        = QueryParser()
ranker        = RankingService()
widget_factory= WidgetFactory()

underlying_search = DatabaseSearchService(
    db_handler=db_handler,
    parser=parser,
    ranker=ranker,
    widget_factory=widget_factory
)
search_service = CachingSearchService(underlying_search, max_cache_size=256)

crawler       = FileCrawler()
indexer       = FileIndexer(db_handler)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "devkey")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def do_index():
    directory = request.form.get('directory', '').strip()
    if not directory or not os.path.isdir(directory):
        flash('Invalid directory path', 'error')
        return redirect(url_for('index'))

    threading.Thread(target=indexer.index_directory, args=(directory,), daemon=True).start()
    flash(f'Started indexing {directory}', 'info')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    raw_query = request.args.get('query', '').strip()

    corrected_query, corrections = correct_query(raw_query, corrector)

    if corrections:
        pairs = ", ".join(f"'{orig}'→'{new}'" for (orig, new) in corrections)
        flash(f"Spell‐check suggestions: {pairs}", 'warning')

    payload = search_service.search(corrected_query)
    results = payload['results']

    facet_by_type     = summarize_by_file_type(results)
    facet_by_year     = summarize_by_year(results)
    facet_by_language = summarize_by_language(results)

    return render_template(
        'results.html',
        results=results,
        query=corrected_query,
        original_query=raw_query,
        widgets=payload['widgets'],
        facets_type=facet_by_type,
        facets_year=facet_by_year,
        facets_lang=facet_by_language
    )

@app.route('/suggest', methods=['GET'])
def suggest():
    prefix = request.args.get('prefix', '')
    suggestions = db_handler.suggest(prefix)
    return jsonify(suggestions)

@app.route('/cache_info', methods=['GET'])
def cache_info():
    info = search_service.cache_info()
    return jsonify(info)

if __name__ == '__main__':
    host  = os.getenv('FLASK_HOST', '127.0.0.1')
    port  = int(os.getenv('FLASK_PORT', 5000))
    debug = (os.getenv('FLASK_DEBUG', 'false').lower() == 'true')
    app.run(host=host, port=port, debug=debug)
