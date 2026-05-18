from flask import Flask, render_template, request, jsonify
from faq_data import faqs

import nltk
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from waitress import serve

nltk.download('punkt')
nltk.download('punkt_tab') 
nltk.download('stopwords')

app = Flask(__name__)

# Text preprocessing
def preprocess(text):
    text = text.lower()

    tokens = word_tokenize(text)

    tokens = [
        word for word in tokens
        if word not in stopwords.words('english')
        and word not in string.punctuation
    ]

    return " ".join(tokens)

# Preprocess FAQ questions
questions = [preprocess(faq['question']) for faq in faqs]

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

question_vectors = vectorizer.fit_transform(questions)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Chat endpoint
@app.route('/chat', methods=['POST'])
def chat():

    user_message = request.json['message']

    processed_message = preprocess(user_message)

    user_vector = vectorizer.transform([processed_message])

    similarities = cosine_similarity(
        user_vector,
        question_vectors
    )

    best_match_index = similarities.argmax()

    best_score = similarities[0][best_match_index]

    if best_score > 0.2:
        response = faqs[best_match_index]['answer']
    else:
        response = "Sorry, I couldn't understand your question."

    return jsonify({
        'response': response
    })

if __name__ == '__main__':
    print("Server running at http://127.0.0.1:5000")
    serve(app, host='0.0.0.0', port=5000)