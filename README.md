# Text Generation App using NLP and LLM

The project is a text generation application that processes accident descriptions using Natural Language Processing (NLP) and Large Language Model (LLM) techniques.

The text generation application is structured around two main components:
- Text Processing
- Text Generation
<img src="static/images/GenAI.png" alt="Architecture Diagram" width="400"/>
The process begins with text processing, where raw text is cleaned and prepared. Then, text generation uses the processed text as a base to produce generated content.

Below is the general architecture of the application development in Visual Studio Code. I divided my code into two main parts:
- **Frontend**: Developed using Flask
- **Backend**: Developed in Python with the following components:
  - Error Correction Stage
  - Information Extraction Stage
  - General Processing Stage
  - Translation Stage
  - Filtering Stage
  - Generation Stage

**Information Extraction Stage**

This first stage involves extracting the date and location of the accident from the description. It is considered the initial step to ensure that these essential pieces of information are not removed during the subsequent text cleaning process.

Date extraction is performed using the regex library, while location extraction is achieved through Named Entity Recognition (NER) in NLP.

<img src="static/images/Date_place.png" alt="Architecture Diagram" width="400"/>

**Text Cleaning Stage**

Text cleaning is an essential step in natural language processing. In this project, the cleaning process involves removing URLs, email addresses, arbitrary numbers, HTML tags, and any other unnecessary information. It also includes removing words that are not found in the dictionary, using the BERT model from Hugging Face.

**Text Correction Stage**

For the text correction stage, a function is used to correct typographical errors, as well as grammar and spelling mistakes. This is done using specific tools depending on the language: pyspellchecker for French and TextBlob for English.

**Text Translation Stage**

For the text translation stage, we start by translating individual words from a file named car-accident-translation, which contains a list of French words and their English translations related to accidents. If a word is not found in this file, we use the Google Translate API to translate the individual word into English, as it supports translation between many languages. If the translation via the API is not sufficient for the context, we use the pre-trained MarianMTModel from Hugging Face to provide a more contextual and accurate translation.


