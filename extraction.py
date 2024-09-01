import spacy
import re
from transformers import pipeline
from datetime import datetime

# Load spaCy model
nlp = spacy.load('en_core_web_md')

# Initialize the sentiment analysis pipeline
sentiment_analyzer = pipeline('sentiment-analysis')
def extract_date(text):
    # Define date patterns
    date_patterns = [
        r'\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b',  # dd/mm/yyyy, dd-mm-yyyy, dd/mm/yy
        r'\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}\b',    # dd/mm/yyyy or dd-mm-yyyy
        r'\b\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2}\b',    # yyyy/mm/dd or yyyy-mm-dd
        r'\b\d{1,2} [A-Za-z]+ \d{4}\b',             # dd Month yyyy
        r'\b[A-Za-z]+ \d{1,2}, \d{4}\b',            # Month dd, yyyy
        r'\b\d{4} [A-Za-z]+ \d{1,2}\b',             # yyyy Month dd
        r'\b[A-Za-z]+, [A-Za-z]+ \d{1,2}, \d{4}\b', # Month, Day, yyyy
        r'\b\d{1,2}[\/\-]\d{4}\b',                  # dd/yyyy (less common)
        r'\b\d{1,2}[\/\-]\d{2}[\/\-]\d{2}\b',       # dd/mm/yy or dd-mm-yy
        r'\b\d{2}[\/\-]\d{2}[\/\-]\d{2}\b',         # yy/mm/dd or yy-mm-dd
        r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[\+\-]\d{2}:\d{2})\b'  # ISO 8601 format yyyy-mm-ddTHH:MM:SSZ or yyyy-mm-ddTHH:MM:SS+hh:mm
    ]
    
    # Extract dates using the patterns
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # Validate and parse the extracted dates
            try:
                # Handle common formats
                if re.match(r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}', match):
                    date_obj = datetime.strptime(match, '%d-%m-%Y')  # Handle dd-mm-yyyy format
                elif re.match(r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}', match):
                    date_obj = datetime.strptime(match, '%d-%m-%Y')  # Handle dd/mm/yyyy or dd-mm-yyyy
                elif re.match(r'\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2}', match):
                    date_obj = datetime.strptime(match, '%Y-%m-%d')  # Handle yyyy-mm-dd
                else:
                    date_obj = datetime.strptime(match, '%d %b %Y')  # Handle dd Month yyyy

                # Check if year is 2024
                if date_obj.year == 2024:
                    return match
            except ValueError:
                continue
    
    return "Date not found"

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# List of known cities (expand this list as needed)
known_cities = ["Tunis", "Sousse", "Monastir","Ben Arous"]

def extract_place(text):
    doc = nlp(text)
    
    # Check what entities are being recognized
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")
    
    places = set()  # Use set to avoid duplicates
    
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC", "FAC"]:  # Default NER labels
            places.add(ent.text.strip())
    
    # Add known cities to the results if not already included
    for city in known_cities:
        if city in text:
            places.add(city)
    
    if places:
        return ', '.join(places)
    
    return "Place not found"
 
    


def extract_vehicle_type(text):
    vehicle_types = ["car", "truck", "bus", "motorcycle", "bicycle","motor"]
    for vehicle in vehicle_types:
        if vehicle in text.lower():
            return vehicle.capitalize()
    return "Vehicle type not found"

def extract_sentiment(text):
    result = sentiment_analyzer(text)
    return result[0]
