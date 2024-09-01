from textblob import TextBlob
import string
from extraction import extract_date, extract_place, extract_vehicle_type, extract_sentiment
import re
from langdetect import detect
from spellchecker import SpellChecker

# Dictionnaire des fautes de frappe courantes
common_typos = {
    "adn": "and",
    "teh": "the",
    "recieve": "receive",
    "definately": "definitely",
    # Ajouter d'autres fautes courantes et leurs corrections ici
}

def correct_typos(text):
    words = text.split()
    corrected_words = [common_typos.get(word.lower(), word) for word in words]
    return ' '.join(corrected_words)

def correct_spelling(text, lang='en'):
    if lang == 'fr':
        spell = SpellChecker(language='fr')
        words = text.split()
        corrected_words = [spell.candidates(word).pop() if word in spell else word for word in words]
        return ' '.join(corrected_words)
    else:
        blob = TextBlob(text)
        return str(blob.correct())

def expand_contractions(text):
    contractions = {
        "n't": "not",
        "'m": "am",
        "'s": "is",
        "'re": "are",
        "'ve": "have",
        "'d": "would",
        "'ll": "will",
        "'t": "not",
        "'cause": "because",
        "'y": "you",
    }
    for contraction, expansion in contractions.items():
        text = re.sub(r"\b" + re.escape(contraction) + r"\b", expansion, text)
    return text

def process_text_correction(text):
    text = correct_typos(text)
    text = expand_contractions(text)
    
    # Détection de la langue et correction
    words = text.split()
    corrected_words = []
    for word in words:
        try:
            lang = detect(word)
        except:
            lang = 'unknown'
        corrected_word = correct_spelling(word, lang)
        corrected_words.append(corrected_word)
    
    return ' '.join(corrected_words)

def normalize_text(text):
    def has_valid_date(text):
        date = extract_date(text)
        return date != "Date not found"
    
    text = expand_contractions(text)
    text = text.lower()
    # Remove long numeric sequences
    text = re.sub(r'\b\d{10,}\b', '', text)  # Remove numbers with 10 or more digits
    text = re.sub(r'\b[a-zA-Z]{9,}\b', '', text)
    # Remove emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    if not has_valid_date(text):
        text = re.sub(r'(?<=\w)\d+(?=\w)', '', text)
    
        text = re.sub(r'\s+', ' ', text)
        text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = text.strip()
    
    return text

