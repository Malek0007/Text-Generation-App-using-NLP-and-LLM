
from transformers import pipeline
from text_filtration import filter_text
def generate_text(prompt):
    # Load the model with authentication
    generator = pipeline("text-generation", model="distilbert/distilgpt2")
    result = generator(prompt, max_length=50, num_return_sequences=3, truncation=True)
    return result[0]['generated_text']