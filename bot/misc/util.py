import os
import json


# translations["greeting"][language]
def _(text, lang):
    # Get the directory path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute file path for translation.json
    translation_file = os.path.join(script_dir, "translation.json")

    # Load the translation JSON file
    with open(translation_file, "r", encoding="utf-8") as file:
        translations = json.load(file)

    # Use English as a fallback language if the requested language is not available
    if lang not in translations[text]:
        lang = "en"

    try:
        return translations[text][lang]
    except KeyError:
        return text
