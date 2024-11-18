from flask import Flask, render_template, request, jsonify
import textwrap
import google.generativeai as genai
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

def configure_generative_ai(api_key):
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Error configuring generative AI: {e}")

def generate_content(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

# Replace 'YOUR_API_KEY' with your actual API key
api_key = "AIzaSyDRYQyH8iYoYKmW8H585mMvx5Mw_BM3Dnw"
# Configuration
configure_generative_ai(api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json
    user_input = data['input']
    conversation_history = data['history']

    if user_input.lower() == 'exit':
        return jsonify({"response": "Goodbye!"})

    elif user_input.lower() == 'clear':
        return jsonify({"response": "Conversation cleared.", "history": ""})

    else:
        conversation_history += "\n" + user_input
        bot_response = generate_content(conversation_history)
        return jsonify({"response": bot_response, "history": conversation_history})

if __name__ == '__main__':
    app.run(debug=True)

