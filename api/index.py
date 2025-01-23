import os
from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# Configure the Gemini API key
genai.configure(api_key='AIzaSyBp4LThvyi-BrhnXPFIgBnpwunh9BT8E_M')  # Ensure GEMINI_API_KEY is set in your environment

@app.route('/', methods=['GET', 'POST'])
def home():
    response = None
    if request.method == 'POST':
        user_query = request.form['query']
        
        # Send the user's query to the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')  # Replace with your specific model name if needed
        chat = model.start_chat(history=[])
        response = chat.send_message(user_query).text  # Get the response from Gemini
        
    return render_template('query_form.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)


