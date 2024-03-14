from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse, urljoin
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup

app = Flask("noval")

session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def print_paragraphs(paragraphs):
    extracted_text = ""
    for paragraph in paragraphs:
        extracted_text += paragraph.text.strip() + '\n\n'
    return extracted_text

def extract_text(url, current_page=1, max_pages=5):
    extracted_text = ""
    
    try:
        with session.get(url) as response:
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            content_div = soup.find('div', class_=['text-left', 'text-right', 'chapter-content'])

            if content_div:
                unwanted_elements = soup.select('p.d-none, div[class^="riwya-"]')
                for element in unwanted_elements:
                    element.decompose()

                all_paragraphs = content_div.find_all('p')
                extracted_text += print_paragraphs(all_paragraphs)

                if current_page < max_pages:
                    next_links = soup.select('a.next_page, a.nextchap')
                    for link in next_links:
                        href = link.get('href')
                        if href and is_valid_url(href):
                            full_url = urljoin(url, href)
                            print(f'الانتقال إلى الصفحة التالية: {full_url}')
                            extracted_text += extract_text(full_url, current_page + 1, max_pages)
                            return extracted_text  

                if current_page >= max_pages:
                    print(f'تم استخراج النص من {max_pages} صفحات.')
            else:
                print('لم يتم العثور على <div class="text-left">.')

            return extracted_text

    except requests.exceptions.RequestException as e:
        print(f'حدث خطأ أثناء الاتصال: {e}')
        return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    url = request.form.get('url')
    max_pages = request.form.get('max_pages', 5)
    if max_pages.isdigit():
        max_pages = int(max_pages)

    extracted_text = extract_text(url, max_pages=max_pages)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'extracted_text': extracted_text})
    else:
        return render_template('result.html', extracted_text=extracted_text)
      