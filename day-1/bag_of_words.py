# import re


def tokenize(text):
    return text.split()
    # return re.findall(r"\w+", text.lower(), flags=re.UNICODE)


def build_vocabulary(corpus):
    vocabulary = set()

    for document in corpus:
        vocabulary.update(tokenize(document))

    return sorted(vocabulary)


def bag_of_words(text, vocabulary):
    tokens = tokenize(text)

    return {word: tokens.count(word) for word in vocabulary}


def vectorize(text, vocabulary):
    bow = bag_of_words(text, vocabulary)

    return [bow[word] for word in vocabulary]


corpus = ["Tôi thích môn Toán", "Tôi thích AI", "Tôi thích âm nhạc"]
input_text = "Tôi thích AI thích Toán"

vocabulary = build_vocabulary(corpus)
bow = bag_of_words(input_text, vocabulary)
vector = vectorize(input_text, vocabulary)

print("Vocabulary:", vocabulary)
print("BOW:", bow)
print("Vector:", vector)
