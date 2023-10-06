import json

from googletrans import Translator

from sentiment_analyzer import analyze_sentiment
from department_categorizer import categorize_department

def perform_translation(news_source: str, extracted_text: tuple, json_file_path: str, language: str) -> None:
    google_translator = Translator()

    file_name = extracted_text[1]
    extracted_lines = extracted_text[0].split("\n")

    print(f'\nTranslating: {file_name}')

    translated_text = [
        google_translator.translate(str(line), src = language, dest = "en").text
        for line in extracted_lines
        if line is not None and line.strip() != ""
    ]

    print("Done ...")

    print(f'\nSaving data to file: {json_file_path}')

    formatted_string = " ".join(translated_text)

    article_data = {
        "id": 1,
        "source": news_source,
        "publication_date": None,
        "text": formatted_string,
        "tone": analyze_sentiment(formatted_string),
        "government-body": categorize_department(formatted_string)
    }

    with open(json_file_path, "w", encoding = "utf-8") as json_file:
        json.dump(article_data, json_file, ensure_ascii = False, indent = 4)

    print("Done ...")
