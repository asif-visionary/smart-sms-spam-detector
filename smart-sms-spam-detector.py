import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import streamlit as st

# Load dataset
data = pd.read_csv('spam.csv', encoding='latin-1')

# Remove duplicate rows
data.drop_duplicates(inplace=True)

# Replace labels
data['Category'] = data['Category'].map({
    'ham': 'Not Spam',
    'spam': 'Spam'
})

# Features and target
messages = data['Message']
categories = data['Category']

# Split dataset
messages_train, messages_test, categories_train, categories_test = train_test_split(
    messages,
    categories,
    test_size=0.2,
    random_state=42
)

# Convert text into numerical features
cv = CountVectorizer(stop_words='english')
features = cv.fit_transform(messages_train)

# Train model
model = MultinomialNB()
model.fit(features, categories_train)

# Test accuracy
messages_test_features = cv.transform(messages_test)
accuracy = model.score(messages_test_features, categories_test)

# Prediction function
def predict_message(message):
    inp_message = cv.transform([message])
    prediction = model.predict(inp_message)
    return prediction[0]


# Streamlit UI
st.set_page_config(page_title="Spam Detection App", page_icon="📩")

st.title("📩 Spam Detection App")
st.write("Enter a message below to check whether it is Spam or Not Spam.")

# Show model accuracy
st.info(f"Model Accuracy: {accuracy:.2%}")

# User input
input_message = st.text_area(
    "Enter your message:",
    height=150
)

# Predict button
if st.button("Predict"):
    if input_message.strip() == "":
        st.warning("Please enter a message.")
    else:
        result = predict_message(input_message)

        if result == "Spam":
            st.error("🚨 This message is classified as SPAM.")
        else:
            st.success("✅ This message is classified as NOT SPAM.")

        st.write(f"**Prediction:** {result}")