# worker.py
import os
from flask import Flask, request, jsonify


def run_worker(worker_id, search_dir, port):
    app = Flask(__name__)

    @app.route("/api/search", methods=["POST"])
    def search_endpoint():
        data = request.get_json(force=True)
        query = data.get("query", "").strip()
        directory = data.get("directory", "").strip() or search_dir

        if not os.path.exists(directory):
            return jsonify({
                "worker_id": worker_id,
                "query": query,
                "results": [],
                "error": f"Directory not found: {directory}"
            }), 400

        results = []
        query_lower = query.lower()
        for root, dirs, files in os.walk(directory):
            for file in files:
                if query_lower in file.lower():
                    results.append(os.path.join(root, file))

        return jsonify({
            "worker_id": worker_id,
            "query": query,
            "results": results
        })

    print(f"Starting worker '{worker_id}' on port {port} searching in '{search_dir}'")
    app.run(host="0.0.0.0", port=port, debug=False)
