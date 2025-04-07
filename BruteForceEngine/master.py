import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates")

config = {
    "workers": []
}

result_cache = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/config", methods=["POST"])
def update_config():
    data = request.get_json(force=True)
    new_workers = data.get("workers", [])
    config["workers"] = new_workers
    result_cache.clear()
    return jsonify({"message": "Configuration updated", "config": config})


@app.route("/api/search", methods=["POST"])
def search_api():
    data = request.get_json(force=True)
    query = data.get("query", "").strip()
    chosen_indices = data.get("workers", [])

    if not query:
        return jsonify({"query": "", "results": []})

    cache_key = query
    if cache_key in result_cache:
        return jsonify({"query": query, "results": result_cache[cache_key]})

    results = []
    for idx in chosen_indices:
        try:
            idx = int(idx)
        except ValueError:
            continue
        if idx < 0 or idx >= len(config["workers"]):
            continue
        worker_info = config["workers"][idx]
        worker_url = worker_info["url"]
        directory = worker_info["directory"]
        try:
            response = requests.post(worker_url, json={"query": query, "directory": directory}, timeout=100)
            if response.status_code == 200:
                data = response.json()
                results.extend(data.get("results", []))
            else:
                print(f"Worker error: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Error contacting worker at {worker_url}: {e}")

    unique_results = sorted(set(results))
    result_cache[cache_key] = unique_results
    return jsonify({"query": query, "results": unique_results})


def run_master(port=3000):
    print(f"Starting master on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
