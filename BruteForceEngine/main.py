# main.py
import multiprocessing
import time
import os
from worker import run_worker
from master import run_master, config


def start_worker_process(worker_id, search_dir, port):
    p = multiprocessing.Process(target=run_worker, args=(worker_id, search_dir, port))
    p.start()
    return p


if __name__ == "__main__":
    num_workers = 2
    worker_processes = []
    base_port = 3001
    default_workers_config = []

    default_search_dir = os.path.expanduser("~")

    for i in range(num_workers):
        worker_id = f"worker-{i + 1}"
        port = base_port + i
        default_url = f"http://localhost:{port}/api/search"
        default_workers_config.append({"url": default_url, "directory": default_search_dir})
        p = start_worker_process(worker_id, default_search_dir, port)
        worker_processes.append(p)

    config["workers"] = default_workers_config

    time.sleep(2)

    try:
        run_master(3000)
    except KeyboardInterrupt:
        print("Shutting down master and workers...")
    finally:
        for p in worker_processes:
            p.terminate()
            p.join()
