# CHATGPT SIMILARITY FN
import difflib

def similarity_score(str1, str2):
    # Convert the strings to lowercase to make the comparison case-insensitive
    str1 = str1.lower()
    str2 = str2.lower()
    # Calculate the similarity ratio between the two strings
    similarity_ratio = difflib.SequenceMatcher(None, str1, str2).ratio()
    return similarity_ratio

# Test the function with your example strings
string1 = 'gang of youths life is hell'
string2 = 'gang of youths life'

score = similarity_score(string1, string2)
print(f'Similarity Score: {score:.2f}')



# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.tokenize import RegexpTokenizer
# from nltk.stem import PorterStemmer
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Sample texts
# text1 = "The Clash London Calling"
# text2 = "The Clash, London Calling (Remastered)"

# # Preprocess the text
# tokenizer = RegexpTokenizer(r'\w+')
# stemmer = PorterStemmer()
# stop_words = set(stopwords.words('english'))

# def preprocess_text(text):
#     tokens = tokenizer.tokenize(text.lower())
#     tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]
#     return ' '.join(tokens)

# preprocessed_text1 = preprocess_text(text1)
# preprocessed_text2 = preprocess_text(text2)

# # Calculate TF-IDF vectors
# vectorizer = TfidfVectorizer()
# tfidf_matrix = vectorizer.fit_transform([preprocessed_text1, preprocessed_text2])

# # Compute cosine similarity
# cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

# print("Cosine Similarity:", cosine_sim[0][0])
