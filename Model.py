from joblib import load
from urllib.parse import urlparse, unquote
import pandas as pd
import re

def countUrlLength(url):
    return len(url)

def countDomainLength(url):
    return len(urlparse(url).netloc)

def countSpecialCharacters(url):
    feature = ['@', '?', '-', '=', '.', '#', '+', '$', '!', '*', ',']
    result = {}
    for a in feature:
        result[a] = url.count(a)

    return result

def checkEncodedSymbols(url):
    decoded_url = unquote(url)
    if url != decoded_url:
        return 1

    return 0

def checkHttps(url):
    protocol = urlparse(url).scheme
    if protocol == 'https':
        return 1

    return 0

def countDigits(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1

    return digits

def countLetters(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters

def checkShortiningService(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 1

    return 0

def checkIP(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4 with port
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
        '([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
        '((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)  # Ipv6
    if match:
        return 1

    return 0

model = load('trained_model.joblib')

def prepareAndPredict(url):
    predict_data = dict()

    predict_data["length"] = [countUrlLength(url)]
    predict_data["domainLength"] = [countDomainLength(url)]
    special_characters = countSpecialCharacters(url)
    for i in special_characters:
        predict_data[i] = [special_characters[i]]
    predict_data["isEncodedSymbols"] = [checkEncodedSymbols(url)]
    predict_data["isHttps"] = [checkHttps(url)]
    predict_data["digitsCount"] = [countDigits(url)]
    predict_data["lettersCount"] = [countLetters(url)]
    predict_data["isShortiningService"] = [checkShortiningService(url)]
    predict_data["isIp"] = [checkIP(url)]

    predict_data = pd.DataFrame(predict_data)

    return model.predict(predict_data)[0]