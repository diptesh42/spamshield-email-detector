📧 SpamShield — Email Spam Detector


 📌 Overview

SpamShield is a full-stack ML project that detects whether an email is spam or legitimate (ham). The user pastes any email body into the web interface, and the app processes it through a trained NLP pipeline — returning a prediction along with a **confidence percentage** for both classes, shown as animated progress bars.

Built as a complete end-to-end deployment project: from model training and serialization to a Flask web server with a custom dark-themed UI.

🎬 Results

| Input | Prediction | Confidence |
|---|---|---|
| "Congratulations! You won a free iPhone. Click here now!" | 🚨 SPAM | 93.55% |
<img width="1000" height="307" alt="Untitled Diagram drawio" src="https://github.com/user-attachments/assets/105c3b66-45ec-427c-96d8-996420a9b973" />

| "Hey, are we still meeting for lunch tomorrow?" | ✅ Not Spam | 99.71% |
<img width="1000" height="310" alt="Untitled Diagram drawio (1)" src="https://github.com/user-attachments/assets/8edd8282-6b6c-4979-9dde-6d466475e3a4" />

⚙️ How It Works

Every submitted email goes through a two-step NLP pipeline:
Raw Email Text


▼




│   CountVectorizer   │  →  Converts text into a word-frequency matrix






▼


│   MultinomialNB     │  →  Predicts Spam / Not Spam + probability scores






▼




JSON Response → Flask → Browser UI



🔢 Why CountVectorizer?
Text cannot be fed directly into a machine learning model — it must first be converted into numbers. CountVectorizer was chosen deliberately for this problem:

- **Word frequency is the right signal for spam.** Spam emails rely on repeated high-trigger words like "free", "winner", "click", "prize". CountVectorizer captures exactly this — how many times each word appears — which is more meaningful here than simply knowing whether a word is present or not.
- **It removes stop words automatically.** With `stop_words='english'`, common words like "the", "is", "and" are stripped out before training, so the model only pays attention to words that actually carry meaning.
- **It is simple, fast, and interpretable.** For a text classification task like spam detection, complex embeddings (like TF-IDF or Word2Vec) often add noise without a meaningful accuracy gain. CountVectorizer keeps the feature space clean and the model easy to reason about.
- **It pairs perfectly with Naive Bayes.** MultinomialNB is mathematically designed to work on count data — non-negative integer frequencies — which is exactly what CountVectorizer produces. They are a natural fit.



🧠 Why MultinomialNB?
Multinomial Naive Bayes is one of the most well-established algorithms for text classification, and for good reason:
- **Built for word counts.** The "Multinomial" in the name means the algorithm is specifically designed for features that represent counts or frequencies — exactly the output of CountVectorizer. It models the probability of each word appearing in a spam vs. non-spam email, and uses that to classify new messages.
- **Bayes' Theorem applied to text.** The model calculates P(spam | words in email) using the frequency of each word observed during training. Words like "free", "winner", and "urgent" will have a much higher probability of appearing in spam emails, so emails containing them get pushed toward the spam class.
- **Fast and efficient.** MultinomialNB trains in milliseconds even on large datasets, and predictions are near-instant at inference time — ideal for a live web application where response speed matters.
- **Works well on small and large datasets.** Unlike deep learning models that need massive amounts of data, Naive Bayes performs strongly even with a modest training set, making it a practical first choice for spam detection.
- **Outputs real probabilities.** Using `predict_proba()`, the model returns a confidence score (0–100%) for both classes, not just a binary label. This lets the UI display exactly how confident the model is, which makes the app more informative and trustworthy.
- **Industry precedent.** Naive Bayes has been used in spam filtering since the early days of email (SpamAssassin, early Gmail filters). It is not just academically sound — it is battle-tested in production.



🛠️ Tech Stack
| Layer | Technology |
|---|---|
| Language | Python 3.8+ |
| Web Framework | Flask |
| ML Library | scikit-learn |
| NLP | CountVectorizer |
| Classifier | MultinomialNB |
| Frontend | HTML, CSS, Vanilla JS |
| Model Serialization | Pickle (.pkl) |



📁 Project Structure
spamshield-email-detector/
│


├── app.py                  # Flask application & prediction route


├── requirements.txt        # Python dependencies

│


├── models/


│   ├── spam_classifier.pkl # Trained MultinomialNB model

│   └── vectorizer.pkl      # Fitted CountVectorizer

│

└── templates/


└── index.html          # Frontend UI



🚀 Getting Started
**1. Clone the repository**
```bash
git clone https://github.com/your-username/spamshield-email-detector.git
cd spamshield-email-detector
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
python app.py
```

**4. Open your browser**
http://127.0.0.1:5000



📬 Usage
1. Paste any email body into the text area
2. Click **Analyse Email** (or press `Ctrl + Enter`)
3. The app returns:
   - ✅ **Not Spam** or 🚨 **SPAM** verdict
   - Confidence percentage for both classes
   - Animated progress bars showing the probability split
