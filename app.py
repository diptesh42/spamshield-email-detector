from flask import Flask, render_template, request, jsonify
import pickle
import os

app = Flask(__name__)

# Load models at startup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "models", "spam_classifier.pkl"), "rb") as f:
    classifier = pickle.load(f)

with open(os.path.join(BASE_DIR, "models", "vectorizer.pkl"), "rb") as f:
    vectorizer = pickle.load(f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    email_text = request.form.get("email_text", "").strip()

    if not email_text:
        return jsonify({"error": "Please enter some email text."}), 400

    # Transform and predict
    features = vectorizer.transform([email_text])
    prediction = classifier.predict(features)[0]
    proba = classifier.predict_proba(features)[0]

    spam_index = list(classifier.classes_).index("Spam")
    ham_index = list(classifier.classes_).index("Not spam")

    return jsonify(
        {
            "prediction": prediction,
            "is_spam": prediction == "Spam",
            "spam_confidence": round(float(proba[spam_index]) * 100, 2),
            "ham_confidence": round(float(proba[ham_index]) * 100, 2),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
