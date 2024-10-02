# title: 9
# aim: Program to implement Naïve Bayes Algorithm using Python.


class NaiveBayes:
    def __init__(self):
        self.data = []
        self.class_probs = {}

    def train(self, data):
        self.data = data
        total_count = len(data)
        for item in data:
            label = item[-1]
            if label not in self.class_probs:
                self.class_probs[label] = 0
            self.class_probs[label] += 1
        for label in self.class_probs:
            self.class_probs[label] /= total_count

    def predict(self, item):
        label = max(self.class_probs, key=self.class_probs.get)
        print(f"Predicted class for {item}: {label}")
        return label


nb = NaiveBayes()
data = [
    ["sunny", "hot", "high", "false", "no"],
    ["sunny", "hot", "high", "true", "no"],
    ["overcast", "hot", "high", "false", "yes"],
    ["rainy", "mild", "high", "false", "yes"],
]
nb.train(data)
nb.predict(["sunny", "cool", "high", "false"])
