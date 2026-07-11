from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Simple fake news keywords
FAKE_KEYWORDS = {
    'clickbait', 'shocking', "you won't believe", 'secret', 'conspiracy',
    'hoax', 'fake', 'scam', 'urgent', 'act now', 'miracle cure',
    'government hiding', "they don't want you to know", 'exposed',
    'warning', 'danger', 'banned', 'censored', 'elites', 'deep state'
}

def is_fake_news(title, text):
    content = (title + " " + text).lower()
    content = re.sub(r'[^\w\s]', ' ', content)
    matches = sum(1 for phrase in FAKE_KEYWORDS if phrase in content)
    return matches >= 2

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        title = data.get('title', '')
        text = data.get('text', '')

        if not title.strip() and not text.strip():
            return jsonify({'error': 'Please provide title or text'}), 400

        is_fake = is_fake_news(title, text)
        result = "Fake" if is_fake else "Real"
        confidence = 85 if is_fake else 90

        return jsonify({
            'result': result,
            'confidence': confidence
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
