from flask import Flask, request, redirect, jsonify
import string
import random
from middleware.logs import send_log 


app = Flask(__name__)

url_map = {}

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/')
def index():
    return "URL shortener service"

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    if not original_url or not isinstance(original_url, str):
        send_log("backend", "error", "handler", "Invalid URL received")
        return jsonify({'error': 'Invalid URL'}), 400

    if not (original_url.startswith('http://') or original_url.startswith('https://')):
        send_log("backend", "error", "handler", "URL must start with http:// or https://")
        return jsonify({'error': 'URL must start with http:// or https://'}), 400


    short_code = generate_short_code()
    url_map[short_code] = original_url
    send_log("backend", "info", "handler", f"Shortened URL {original_url} to {short_code}")
    return jsonify({'short_url': request.host_url + short_code})


@app.route('/<short_code>')
def redirect_url(short_code):
    original_url = url_map.get(short_code)
    if original_url:
        send_log("backend", "info", "handler", f"Redirecting short code {short_code}")
        return redirect(original_url)
    send_log("backend", "warning", "handler", f"Short code {short_code} not found")
    return jsonify({'error': 'URL not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)