<<<<<<< HEAD

from transformers import pipeline
from text_filtration import filter_text
def generate_text(prompt):
    # Load the model with authentication
    generator = pipeline("text-generation", model="distilbert/distilgpt2")
    result = generator(prompt, max_length=50, num_return_sequences=3, truncation=True)
=======

from transformers import pipeline
from text_filtration import filter_text
def generate_text(prompt):
    # Load the model with authentication
    generator = pipeline("text-generation", model="distilbert/distilgpt2")
    result = generator(prompt, max_length=50, num_return_sequences=3, truncation=True)
>>>>>>> 9d9211599fffdb82adf728b8e63ab4c5405b95eb
    return result[0]['generated_text']