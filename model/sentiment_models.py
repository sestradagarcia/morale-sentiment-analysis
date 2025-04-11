import json
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    pipeline
)

# Load models and tokenizers
emotion_model_id = "j-hartmann/emotion-english-distilroberta-base"
emotion_tokenizer = AutoTokenizer.from_pretrained(emotion_model_id)
emotion_model = AutoModelForSequenceClassification.from_pretrained(emotion_model_id)
emotion_pipeline = pipeline("text-classification", model=emotion_model, tokenizer=emotion_tokenizer, return_all_scores=True)

sentiment_model_id = "cardiffnlp/twitter-roberta-base-sentiment"
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_id)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_id)
sentiment_pipeline = pipeline("text-classification", model=sentiment_model, tokenizer=sentiment_tokenizer, return_all_scores=True)

morale_model_id = "facebook/bart-large-mnli"
morale_pipeline = pipeline("zero-shot-classification", model=morale_model_id)

# Morale-specific candidate labels
morale_labels = [
    "high morale",
    "low morale",
    "engaged",
    "disengaged",
    "motivated",
    "unmotivated",
    "energised",
    "tired",
    "frustrated",
    "calm",
    "supported",
    "unsupported",
    "under pressure",
    "burnout",
    "happy",
    "relaxed",
    "overwhelmed",
    "underwhelmed",
    "productively focused",
    "connected",
    "disinterested",
    "aspirational",
    "uplifted",
    "communicative",
    "uncertain",
    "blocked",
    "growth-oriented",
    "curious",
    "collaborative"
]


# Map sentiment label ids to human-readable labels
sentiment_label_map = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

def analyse_sentiment(data):
    analysed = []

    for item in data:
        text = item["cleaned_text"]

        # Run emotion analysis
        emotion_result = emotion_pipeline(text)[0]
        top_emotion = max(emotion_result, key=lambda x: x['score'])

        # Run sentiment polarity
        sentiment_result = sentiment_pipeline(text)[0]
        top_sentiment = max(sentiment_result, key=lambda x: x['score'])

        # Map sentiment label to human-readable label
        sentiment_label = sentiment_label_map.get(top_sentiment["label"], "unknown")

        # Run zero-shot classification for morale
        zero_shot_result = morale_pipeline(text, morale_labels)
        top_morale = {
            "label": zero_shot_result["labels"][0],
            "score": zero_shot_result["scores"][0]
        }

        analysed.append({
            "id": item["id"],
            "type": item["type"],
            "text": text,
            "emotion": {
                "label": top_emotion["label"],
                "score": round(top_emotion["score"], 4)
            },
            "sentiment": {
                "label": sentiment_label,
                "score": round(top_sentiment["score"], 4)
            },
            "morale": {
                "label": top_morale["label"],
                "score": round(top_morale["score"], 4)
            }
        })

    return analysed

if __name__ == "__main__":
    # Load cleaned Miro data from text_processing.py (or from saved .json)
    cleaned_data_file_path = "../data/data_preprocessing/cleaned_data.json"
    with open(cleaned_data_file_path, "r") as f:
        cleaned_data = json.load(f)

    results = analyse_sentiment(cleaned_data)

    # Save results to file
    with open("sentiment_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Sentiment analysis complete. Results saved to sentiment_results.json")
