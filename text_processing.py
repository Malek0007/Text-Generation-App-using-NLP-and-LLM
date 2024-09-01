from translation import translate_non_english_words
from correction import correct_typos, normalize_text,process_text_correction
from extraction import extract_date, extract_place, extract_vehicle_type, extract_sentiment
from transformers import pipeline
from text_filtration import filter_text
from text_generation import generate_text

def process_text(text):
    # Extract date, place, and vehicle type (optional fields)
    date = extract_date(text)  # This may return None
    place = extract_place(text)  # This may return None
    
    # Normalize and correct the text as before
    normalized_text = normalize_text(text)
    corrected_typos_text = correct_typos(normalized_text)
    processed_text = process_text_correction(corrected_typos_text)
    
    # Filter the text and translate non-English words
    filtered_text = filter_text(processed_text)
    
    if not filtered_text:
        return {"error": "Text did not pass the filter."}
    
    translated_text = translate_non_english_words(processed_text)
    
    # Extract vehicle type (optional)
    vehicle_type = extract_vehicle_type(translated_text)  # This may return None
    
    # Perform sentiment analysis
    sentiment = extract_sentiment(translated_text)
    
    # Generate the additional text
    generated_text = generate_text(translated_text)
    
    # Return results (include None for missing values)
    return {
        "processed_text": translated_text,
        "date": date,
        "place": place,
        "vehicle_type": vehicle_type,
        "sentiment": sentiment,
        "generated_text": generated_text
    }
