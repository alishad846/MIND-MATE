import nltk
nltk.download('punkt_tab')

from transformers import pipeline, AutoTokenizer, TFAutoModelForSequenceClassification
from nltk.tokenize import sent_tokenize

model_name = "cardiffnlp/twitter-roberta-base-emotion"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

emotion_classifier = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    top_k=3,
    framework="tf"
)

def detect_emotions_long_text(text):
    sentences = sent_tokenize(text)
    all_scores = {}

    for sent in sentences:
        results = emotion_classifier(sent)
        # When top_k > 1, results is a list of lists, so unwrap the first list
        if isinstance(results[0], list):
            results = results[0]
        for r in results:
            label = r['label']
            score = r['score']
            all_scores[label] = all_scores.get(label, 0) + score

    total = sum(all_scores.values())
    for k in all_scores:
        all_scores[k] /= total

    sorted_emotions = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_emotions

if __name__ == "__main__":
    test_text = "Bhai honestly I’m exhausted from job stress. Kal manager ne daant diya and now I feel useless. I just want some peace and motivation."
    emotions = detect_emotions_long_text(test_text)
    print("Detected Emotions:", emotions)
