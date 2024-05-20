from flask import Flask, request, Response
from goose3 import Goose
from goose3.text import StopWordsChinese
import requests
import jieba
from janome.tokenizer import Tokenizer as JanomeTokenizer
from langdetect import detect as langdetect_detect, DetectorFactory
import langid
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Ensure consistent language detection results for langdetect
DetectorFactory.seed = 0

app = Flask(__name__)

def extract_first_image(html, base_url=None):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Define potential content areas
    content_selectors = [
        'article',  # Common HTML5 tag for article content
        'div[class*="content"]',  # Divs with class names containing "content"
        'div[class*="article"]',  # Divs with class names containing "article"
        'section',  # Common HTML5 tag for sections
        'main'  # Common HTML5 tag for main content
    ]
    
    for selector in content_selectors:
        main_content = soup.select_one(selector)
        if main_content:
            img = main_content.find('img')
            if img:
                img_url = img.get('src')
                if img_url:
                    if img_url.startswith('//'):
                        if base_url:
                            parsed_url = urlparse(base_url)
                            img_url = f'{parsed_url.scheme}:{img_url}'
                        else:
                            img_url = f'https:{img_url}'
                    elif img_url.startswith('/'):
                        if base_url:
                            parsed_url = urlparse(base_url)
                            img_url = f'{parsed_url.scheme}://{parsed_url.netloc}{img_url}'
                    return img_url
    return None

def detect_language(text):
    # Use langdetect
    try:
        lang_langdetect = langdetect_detect(text)
    except:
        lang_langdetect = None

    # Use langid
    lang_langid, _ = langid.classify(text)

    # If both detectors agree, return the detected language
    if lang_langdetect == lang_langid:
        return lang_langdetect
    else:
        # If not, return the result from langid
        return lang_langid

@app.route('/health', methods=['GET'])
def health_check():
    return Response(json.dumps({"status": "healthy"}), mimetype='application/json; charset=utf-8')

@app.route('/', methods=['POST'])
def extract_content():
    data = request.json
    url = data.get('url')
    html = data.get('html')
    language = data.get('language')

    if not url and not html:
        return Response(json.dumps({"error": "URL or HTML content must be provided"}, ensure_ascii=False), mimetype='application/json; charset=utf-8')

    if url:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'}
        response = requests.get(url, headers=headers)
        html = response.text

    if not language:
        language = detect_language(html)
    
    if language == 'zh':
        g = Goose({'stopwords_class': StopWordsChinese})
    else:
        g = Goose()

    article = g.extract(raw_html=html)
    content = article.cleaned_text
    # Fallback if Goose3 fails to extract content
    if not content:
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.get_text()

    image_url = article.top_image.src if article.top_image else extract_first_image(html, url)

    if language == 'zh':
        content = ''.join(jieba.cut(content))
    elif language == 'ja':
        tokenizer = JanomeTokenizer()
        content = ' '.join(token.surface for token in tokenizer.tokenize(content))
    else:
        content = content  # For other languages, no special tokenization

    response_data = {
        "content": content,
        "image_url": image_url,
        "language": language
    }

    response_json = json.dumps(response_data, ensure_ascii=False)
    return Response(response_json, mimetype='application/json; charset=utf-8')

if __name__ == '__main__':
    app.run(debug=False, port=5001)