import os
import string
import spacy
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pathlib import Path

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = ''.join([char for char in text if char not in string.punctuation])
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    doc = nlp(' '.join(words))
    lemmatized_words = [token.lemma_ for token in doc]
    return ' '.join(lemmatized_words)

def generate_wordcloud(text, output_folder, filename):
    if len(text.strip()) == 0:
        return
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    wordcloud_img_path = os.path.join(output_folder, f"{filename}_wordcloud.png")
    try:
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(wordcloud_img_path)
        plt.close()
    except Exception as e:
        print(f"Error generating wordcloud for {filename}: {e}")

def analyze_text_folder(input_folder):
    output_folder = 'data/texts/output'
    others_folder = os.path.join(output_folder, 'others')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(others_folder):
        os.makedirs(others_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.txt'):
            file_path = os.path.join(input_folder, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                preprocessed_text = preprocess_text(text)

                vectorizer = TfidfVectorizer()
                X = vectorizer.fit_transform([preprocessed_text])
                feature_names = vectorizer.get_feature_names_out()
                feature_index = X[0, :].nonzero()[1]
                tfidf_scores = zip(feature_index, [X[0, x] for x in feature_index])
                sorted_tfidf_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)

                print(f"TF-IDF Scores for {filename}:")
                for score in sorted_tfidf_scores[:5]:
                    print(f"{feature_names[score[0]]}: {score[1]:.4f}")
                print()

                high_keywords = [feature_names[score[0]] for score in sorted_tfidf_scores if score[1] > 0.4]
                if high_keywords:
                    category_folder = os.path.join(output_folder, '_'.join(high_keywords))
                    if not os.path.exists(category_folder):
                        os.makedirs(category_folder)

                    tfidf_output_path = os.path.join(category_folder, f"{filename}_tfidf.txt")
                    with open(tfidf_output_path, 'w', encoding='utf-8') as tfidf_file:
                        tfidf_file.write(f"TF-IDF Scores for {filename}:\n")
                        for score in sorted_tfidf_scores[:5]:
                            tfidf_file.write(f"{feature_names[score[0]]}: {score[1]:.4f}\n")
                    generate_wordcloud(text, category_folder, filename)
                else:
                    tfidf_output_path = os.path.join(others_folder, f"{filename}_tfidf.txt")
                    with open(tfidf_output_path, 'w', encoding='utf-8') as tfidf_file:
                        tfidf_file.write(f"No significant keywords found for {filename}\n")
                    generate_wordcloud(text, others_folder, filename)

            print(f"Processed {filename}.")

    print("Analysis complete!")
