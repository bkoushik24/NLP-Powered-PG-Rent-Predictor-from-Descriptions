**Step 1:Create Scorer.py manually**
"""

os.makedirs("utils", exist_ok=True)

with open("utils/scorer.py", "w") as f:
    f.write("""
import numpy as np

def calculate_fact_score(probabilities):
    \"""
    Convert prediction probabilities into fact scores (0–100).
    \"""
    max_confidence = np.max(probabilities, axis=1)
    fact_scores = (max_confidence * 100).round(2)
    return fact_scores
""")

"""**Step-2: Import your libraries**"""

import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

"""**Step-3: Import your Required Libraries**"""

import pandas as pd
import re
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np

"""**Step-4: Define the Fact-Score Function**"""

def calculate_fact_score(probabilities):
    max_confidence = np.max(probabilities, axis=1)
    return (max_confidence * 100).round(2)

"""**Step-5: Load your Dataset**"""

df = pd.DataFrame({
    'title': [
        'Nasa confirms water on the moon',
        'Donald Trump is a Martian',
        'Pfizer releases COVID-19 vaccine trial results',
        'Pope endorses Trump for president'
    ],
    'label': [
        'REAL',
        'FAKE',
        'REAL',
        'FAKE'
    ]
})

"""**Step-6: Preprocess the Text**"""

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

df['clean_title'] = df['title'].apply(preprocess)

"""**Step-7: Vectorize Text**"""

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['clean_title'])
y = df['label']

"""**Step-8: Train Model**"""

model = LogisticRegression()
model.fit(X, y)

"""**Step-9: Predict and Score**"""

y_pred = model.predict(X)
y_probs = model.predict_proba(X)
fact_scores = calculate_fact_score(y_probs)

"""**Step-10: Save to Predictions.csv**"""

results = pd.DataFrame({
    'title': df['title'],
    'prediction': y_pred,
    'fact_score': fact_scores
})

os.makedirs('outputs', exist_ok=True)
results.to_csv('outputs/predictions.csv', index=False)

print("predictions.csv saved in outputs/")
print(results)
