from transformers import pipeline
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path to save/load the model
model_path = "./models"  # Local folder for the model

# Initialize the pipeline, with cache_dir only used during model loading
qa_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",  # Model name
    cache_dir=model_path          # Cache directory for loading/saving the model
)

# Function to generate a response
def generate_response(user_query, context=""):
    if not context:
        return "I'm sorry, I couldn't find a relevant answer in the knowledge base."
    # Generate a response using the pipeline
    response = qa_pipeline(
        f"{context} {user_query}",  # Input prompt
        max_length=50,             # Limit the length of the generated text
        num_return_sequences=1     # Return one response
    )
    return response[0]["generated_text"]

# Route to handle POST requests
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_query = data.get("query", "")
        context_answer = "Your context here"  # Replace with dynamic context
        response = generate_response(user_query, context=context_answer)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False)
