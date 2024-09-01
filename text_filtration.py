from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
import torch

# Define the model architecture
print("Loading the model...")
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
print("Model loaded.")

# Load the weights from the .pth file
model_path = 'C:/Users/dynabook/Desktop/Text_Generation/Saved_model/1.pth'
try:
    # Load the model state dictionary with map_location to CPU
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    print("Weights loaded successfully.")
except Exception as e:
    print(f"Error loading weights: {e}")

# Make sure the model is in evaluation mode
model.eval()
print("Model set to evaluation mode.")

# Define the tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

# Function to predict the label for a single string
def predict_label(text):
    # Ensure text is a single string
    if isinstance(text, str):
        inputs = tokenizer(text, return_tensors="pt")
        
        # Move inputs to CPU as well
        inputs = {key: value.to(torch.device('cpu')) for key, value in inputs.items()}

        # Forward pass to get model predictions
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Get the predicted class
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        return predicted_class
    else:
        raise ValueError("Input is not a string.")

# Function to filter a single string based on the classification
def filter_text(text):
    # Predict the label for the input text
    predicted_class = predict_label(text)
    
    # Return the text if the predicted class is not 0
    if predicted_class != 0:
        return text
    else:
        return None

# # Example usage
# text = "The car accident was severe."

# filtered_text = filter_text(text)
# if filtered_text:
#     print("Filtered text:", filtered_text)
# else:
#     print("Text did not pass the filter.")
