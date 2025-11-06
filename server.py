from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate_itinerary():
    data = request.json
    prompt = f"""
    Create a day-by-day travel itinerary for a trip from {data['origin']} to {data['destination']}
    from {data['start_date']} to {data['end_date']}.
    Traveler interests: {', '.join(data['interests'])}.
    Preferred pace: {data['pace']}.
    Return each day's plan divided into Morning, Afternoon, and Evening.
    """

    # Gọi mô hình Ollama (ví dụ llama3)
    result = subprocess.run(["ollama", "run", "llama3", prompt], capture_output=True, text=True)
    itinerary = result.stdout.strip()
    return jsonify({"itinerary": itinerary})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
