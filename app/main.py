from miro_api import get_miro_items
from text_processing import clean_text
from sentiment_model import analyze_text
from report_generator import generate_report

def main():
    miro_items = get_miro_items()
    results = []

    for item in miro_items:
        cleaned = clean_text(item["text"])
        analysis = analyze_text(cleaned)
        results.append({
            "id": item["id"],
            "original": item["text"],
            "cleaned": cleaned,
            "analysis": analysis
        })

    generate_report(results)

if __name__ == "__main__":
    main()
