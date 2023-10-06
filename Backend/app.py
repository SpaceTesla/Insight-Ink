import asyncio
import json

from flask import Flask, request, render_template

from text_crawler import scrape_ndtv_archive
from image_crawler import perform_ocr
from google_translator import perform_translation

app = Flask(__name__, template_folder = "../Frontend")

media_outlets = {
    "Hindustan": ["Hindi", "hin"],
    "Prajavani": ["Kannada", "kan"],
    "Dinamalar": ["Tamil", "tam"],
    "Mathrubhumi": ["Malayalam", "mal"],
    "Eenadu": ["Telugu", "tel"]
}

@app.route("/", methods = ["GET", "POST"])
def home() -> str:
    if request.method == "POST":
        news_source = request.form["news_source"]
        target_date = request.form["target_date"]

        if news_source == "NDTV":
            source_url = f'https://archives.ndtv.com/articles/{target_date}.html'
            max_articles_to_scrape = 100

            asyncio.run(scrape_ndtv_archive(news_source, target_date, source_url, max_articles_to_scrape))

            with open(r'Backend\english.json', "r", encoding = "utf-8") as json_file:
                scraped_data = json.load(json_file)

            return render_template("test.html", json_data = json.dumps(scraped_data, indent = 4))

        elif news_source in media_outlets:
            source_language = media_outlets[news_source][0]
            image_file_path = rf'Backend\Assets\{media_outlets[news_source][1]}-1.jpg'

            with open(r'Backend\language_codes.json', "r", encoding = "utf-8") as json_file:
                language_mappings = json.load(json_file)

            extracted_text = perform_ocr(image_file_path, language_mappings[source_language][1])
            json_file_path = rf'Backend\{source_language.lower()}.json'
            perform_translation(news_source, extracted_text, json_file_path, language_mappings[source_language][0])

            with open(json_file_path, "r", encoding = "utf-8") as json_file:
                scraped_data = json.load(json_file)

            return render_template("test.html", json_data = json.dumps(scraped_data, indent = 4))

        else:
            return "News source not supported"
    else:
        return render_template("test.html")

if __name__ == "__main__":
    app.run()
