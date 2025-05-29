from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
with open("test", "r") as file:
    sequence_to_classify = file.read()
candidate_labels = ['semantic bug', 'no semantic bug']
result = classifier(sequence_to_classify, candidate_labels, multi_label=False)

print(result['labels'])
print(result['scores'])
