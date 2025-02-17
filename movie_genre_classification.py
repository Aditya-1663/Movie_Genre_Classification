# -*- coding: utf-8 -*-
"""Movie_Genre_Classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1f699Wmq4bS9kLoDR8YLWUvHewrCeQJWa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

!pip install kaggle
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!kaggle datasets download -d hijest/genre-classification-dataset-imdb
!unzip -q /content/genre-classification-dataset-imdb.zip

train_path = "/content/Genre Classification Dataset/train_data.txt"
train_data = pd.read_csv(train_path, sep=':::', names=['Title', 'Genre', 'Description'], engine='python')
train_data

test_path = "/content/Genre Classification Dataset/test_data.txt"
test_data = pd.read_csv(test_path, sep=':::', names=['Id', 'Title', 'Description'], engine='python')
test_data

train_data.describe()

test_data.describe()

train_data.isnull().sum()

test_data.isnull().sum()

class_distribution = train_data['Genre'].value_counts()
print("Class Distribution:")
print(class_distribution)

plt.figure(figsize=(8, 6))
class_distribution.plot(kind='bar', color='skyblue')
plt.title('Class Distribution')
plt.xlabel('Class')
plt.ylabel('Frequency')
plt.xticks(rotation=65)
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
min_class_size = min(class_distribution)

balanced_train_data = pd.DataFrame(columns=['Title', 'Genre', 'Description'])

for genre, count in class_distribution.items():
  class_data = train_data[train_data['Genre'] == genre].sample(n=min_class_size, random_state=42)
  balanced_train_data = pd.concat([balanced_train_data, class_data], ignore_index=True)

balanced_train_data.describe()
balanced_class_distribution = balanced_train_data['Genre'].value_counts()

print("Balanced Class Distribution:")
print(balanced_class_distribution)

plt.figure(figsize=(8, 6))
balanced_class_distribution.plot(kind='bar', color='skyblue')
plt.title('Balanced Class Distribution')
plt.xlabel('Class')
plt.ylabel('Frequency')
plt.xticks(rotation=65)
plt.show()

balanced_train_data

import re
import numpy as np

def remove_link(text):
    pattern = re.compile(r'https?://\S+|www\.\S+')
    if pattern:
        return pattern.sub(r'', text)
    else:
        return text

import string
Exclude=string.punctuation



def remove_punctuation(text):
    return text.translate(str.maketrans('','',Exclude))

def remove_html_tag(text):
    i=0
    pattern=re.compile(r'<.*?>')
    if pattern:
      list=np.array(pattern.findall(text))
      n=list.shape[0]
    for i in range(n):
      text= text.replace(list[i],'')
    return text


from textblob import TextBlob

def correct_spell(text):
    textblb=TextBlob(text)
    return textblb.correct().string


import nltk

from nltk.corpus import stopwords

nltk.download('stopwords')


extra=stopwords.words('english')
stopwrd=np.array(extra)

def remove_stopwords(text, stopwords):
    split_text = text.split()
    filtered_text = []

    for word in split_text:
        if word not in stopwords:
            filtered_text.append(word)

    result = ' '.join(filtered_text)
    return result

def remove_emoji(text):
    pattern=re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    if pattern:
       list= pattern.findall(text)
    return pattern.sub(r'', text)

import spacy
nlp = spacy.load("en_core_web_sm")

def lemmatization(text):
    doc=nlp(text)
    text_=[]
    for word in doc:
       text_.append(word.lemma_)

    result = ' '.join(text_)
    return result

def text_cleaning(text,stopwords):
    text1=remove_link(text)
    text2=remove_html_tag(text1)
    text3=remove_emoji(text2)
    text4=remove_stopwords(text3,stopwords)
    text5=remove_punctuation(text4)
    text6=lemmatization(text5)
    text7=correct_spell(text6)
    return text7

balanced_train_data['Description'] = balanced_train_data['Description'].apply(text_cleaning, stopwords=stopwrd)

tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(balanced_train_data['Description'])
y_train = balanced_train_data['Genre']


nb_classifier = MultinomialNB()
nb_classifier.fit(X_train_tfidf, y_train)


y_train_pred = nb_classifier.predict(X_train_tfidf)


print("Accuracy on training set:", accuracy_score(y_train, y_train_pred))
print("Classification Report on training set:\n", classification_report(y_train, y_train_pred))

class Inference:
  def __init__(self, model, vectorizer):
    self.model = model
    self.vectorizer = vectorizer

  def predict(self, text):
    text = text_cleaning(text, stopwrd)
    text_vectorized = self.vectorizer.transform([text])
    prediction = self.model.predict(text_vectorized)[0]
    return prediction

inference = Inference(nb_classifier, tfidf_vectorizer)

inference.predict("Chronicles a multi-faceted, 15-year span of pre-and post-Civil War expansion and settlement of the American west.")











