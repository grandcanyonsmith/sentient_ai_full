from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")

model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")


def select_classification_label(text):
    from transformers import pipeline
    classifier = pipeline("zero-shot-classification",
                        model="facebook/bart-large-mnli")


    sequence_to_classify = text
    candidate_labels = ['Execute send text', 'Execute write python code', 'Do nothing', 'Send email', 'Edit code', 'Analyze file', 'Edit file', 'Scan file', 'Execute command', 'Do me a favor']
    
    results = classifier(sequence_to_classify, candidate_labels)
    confidence = results['scores'][0]
    best_label = results['labels'][0]
    print(best_label, confidence)
    
    return best_label, confidence

select_classification_label("Edit start_file in websocket client")




