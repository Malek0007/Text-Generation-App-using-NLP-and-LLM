from googletrans import Translator
from transformers import MarianMTModel, MarianTokenizer
import nltk
from extraction import extract_date, extract_place, extract_vehicle_type, extract_sentiment
from textblob import TextBlob

# Initialize translator
translator = Translator()

# Load MarianMT model and tokenizer for English-French translation
model_name = 'Helsinki-NLP/opus-mt-fr-en'  # For French to English
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def detect_language(word):
    try:
        detected = translator.detect(word)
        return detected.lang
    except Exception as e:
        print(f"Language detection error: {e}")
        return 'unknown'

def is_unique_synonym(word):
    pos = nltk.pos_tag([word])[0][1]
    return pos in ['NN', 'NNS']

# Define the translation dictionary
predefined_translations = {
    'voiture': 'car',
    'accident': 'accident',
    'camion': 'truck',
    'moto': 'motorcycle',
    'bus': 'bus',
    'panne': 'breakdown',
    'collision': 'collision',
    'route': 'road',
    'blessure': 'injury',
    'ambulance': 'ambulance',
    'police': 'police',
    'chauffeur': 'driver',
    'feu': 'fire',
    'urgence': 'emergency'
}

def translate_non_english_words(text):
    words = text.split()
    translated_words = []
    current_chunk = []
    translated_set = set()  # To track already translated words

    for word in words:
        current_chunk.append(word)
        chunk_text = ' '.join(current_chunk)

        # Check if the chunk is a date or place
        if extract_date(chunk_text) != "Date not found" or extract_place(chunk_text) != "Place not found":
            translated_words.append(chunk_text)
            current_chunk = []
        else:
            lang = detect_language(word)
            if lang != 'en':
                if word in predefined_translations:
                    translated_word = predefined_translations[word]
                    translated_words.append(translated_word)
                    translated_set.add(word)  # Add the word to the set of translated words
                elif word in translated_set:
                    translated_words.append(predefined_translations[word])
                else:
                    try:
                        # Use is_unique_synonym or fallback to translator/model
                        if is_unique_synonym(word):
                            translated_word = translator.translate(word, dest='en').text
                        else:
                            inputs = tokenizer(word, return_tensors="pt", truncation=True)
                            translated = model.generate(**inputs)
                            translated_word = tokenizer.decode(translated[0], skip_special_tokens=True)
                        translated_words.append(translated_word)
                        translated_set.add(word)  # Add the word to the set of translated words
                    except Exception as e:
                        print(f"Translation error for word '{word}': {e}")
                        translated_words.append(word)
            else:
                translated_words.append(word)
            current_chunk = []

    if current_chunk:
        translated_words.append(' '.join(current_chunk))

    # Normalize text (e.g., correct spelling errors)
    processed_text = ' '.join(translated_words)
    processed_text = correct_spelling_errors(processed_text)

    return processed_text

def correct_spelling_errors(text):
    # Placeholder function for correcting spelling errors
    # You can use TextBlob, SpellChecker, or any other spelling correction method
    # For example, using TextBlob:
    blob = TextBlob(text)
    return str(blob.correct())
