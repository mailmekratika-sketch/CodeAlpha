from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
from waitress import serve

app = Flask(__name__)

LANGUAGES = {
    'en': 'English',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ""

    if request.method == 'POST':
        text = request.form['text']
        source_lang = request.form['source_lang']
        target_lang = request.form['target_lang']

        translated_text = GoogleTranslator(
            source=source_lang,
            target=target_lang
        ).translate(text)

    return render_template(
        'index.html',
        languages=LANGUAGES,
        translated_text=translated_text
    )

if __name__ == '__main__':
    print("Server running at http://127.0.0.1:5000")
    serve(app, host='0.0.0.0', port=5000)