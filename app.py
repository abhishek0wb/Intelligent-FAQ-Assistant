from flask import Flask, request, jsonify, render_template
import sqlite3
from transformers import pipeline

app = Flask(__name__)

# Load Flan-T5
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")

def generate_response(user_query, context=""):
    if not context:
        return "I'm sorry, I couldn't find a relevant answer in the knowledge base."
    
    # Generative prompt
    prompt = f"Context: {context}\nQuestion: {user_query}\nAnswer:"
    response = qa_pipeline(prompt, max_length=50, num_return_sequences=1)
    return response[0]['generated_text'].strip()


def fetch_faq_from_db(query):
    conn = sqlite3.connect('faq.db')
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM knowledge_base")
    rows = cursor.fetchall()
    conn.close()
    
    for question, answer in rows:
        if query.lower() in question.lower():
            return question, answer
    return None, None

# Homepage with a form for user input
@app.route('/')
def home():
    return '''
    <h1>Intelligent FAQ Assistant</h1>
    <form action="/ask" method="post">
        <label for="query">Ask a Question:</label><br>
        <input type="text" id="query" name="query" required><br><br>
        <button type="submit">Submit</button>
    </form>
    '''

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form.get('query')
    
    # Fetch FAQ from database
    context_question, context_answer = fetch_faq_from_db(user_query)
    if context_answer:
        response = generate_response(user_query, context=f"{context_answer}")
    else:
        response = "I'm sorry, I couldn't find a relevant answer in the knowledge base. Please contact support for further assistance."
    
    return f'''
    <h1>Intelligent FAQ Assistant</h1>
    <p><strong>Your Question:</strong> {user_query}</p>
    <p><strong>Answer:</strong> {response}</p>
    <a href="/">Ask another question</a>
    '''


if __name__ == '__main__':
    app.run(debug=True)
