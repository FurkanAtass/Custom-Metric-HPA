from flask import Flask, jsonify, Response
import time
from concurrent.futures import ThreadPoolExecutor
from prometheus_client import start_http_server, Counter, Histogram
from prometheus_client import generate_latest, REGISTRY

PORT = 3000
app = Flask(__name__)

executor = ThreadPoolExecutor(max_workers=1)

graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.')

def long_running_task():
    time.sleep(10) 
    return "AI Model Inference Result"

@app.route("/")
def hello():
    future = executor.submit(long_running_task)
    start = time.time()
    result = future.result() 
    end = time.time()
    graphs['c'].inc()
    graphs['h'].observe(end - start)
    return jsonify(result=result)

@app.route('/metrics')
def metrics():
    res = []
    for k,v in graphs.items():
        res.append(generate_latest(v))
    return Response(res, mimetype="text/plain")

if __name__ == "__main__":
    # start_http_server(8000)  
    app.run(host='0.0.0.0', port=PORT) 