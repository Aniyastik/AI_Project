from flask import Flask, jsonify, request
from rag.database import find_relevant_topic, retrieve_chunk
from simulator import simulate_response
from evaluation.evaluator import run_evaluation

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({
        "name": "Walled Garden AI",
        "status": "ok",
        "routes": {
            "health": "/health",
            "chat": "/chat (POST)",
            "evaluate": "/evaluate (POST)"
        }
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    age = int(data.get("age", 12))
    system = data.get("system", "Proposed")

    if not prompt:
        return jsonify({"error": "Missing 'prompt'"}), 400

    topic = find_relevant_topic(prompt)
    context = retrieve_chunk(topic, age) if topic else ""

    response = simulate_response(
        system=system,
        prompt=prompt,
        user_age=age,
        context=context,
    )

    return jsonify({
        "system": system,
        "age": age,
        "prompt": prompt,
        "retrieved_topic": topic,
        "response": response,
    })


@app.post("/evaluate")
def evaluate():
    data = request.get_json(silent=True) or {}
    limit = data.get("limit")

    if limit is not None:
        try:
            limit = int(limit)
        except ValueError:
            return jsonify({"error": "'limit' must be an integer"}), 400

    df = run_evaluation(limit=limit, output_path="evaluation/results.csv")

    summary = (
        df.groupby("System")[["Safety_Score", "Accuracy_Score", "Hallucination_Score", "Age_Align_Score"]]
        .mean()
        .round(3)
        .to_dict(orient="index")
    )

    return jsonify({
        "rows": len(df),
        "summary": summary,
        "results_file": "evaluation/results.csv"
    })