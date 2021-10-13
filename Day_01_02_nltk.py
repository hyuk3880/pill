#applekoong@naver.com 김정훈

import nltk
import string

def datasets():
    nltk.download('gutenberg')
    nltk.download('stopwords')
    nltk.download('webtext')
    nltk.download('wordnet')
    nltk.download('reuters')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt')

    # nltk.download()

# datasets()

def corpus():
    print(nltk.corpus.gutenberg)

    print(nltk.corpus.gutenberg.fileids())
    emma = nltk.corpus.gutenberg.raw('austen-emma.txt')
    print(emma)
    print(type(emma))
    print(nltk.corpus.gutenberg.words())

def tokenize():
    text = nltk.corpus.gutenberg.raw('austen-emma.txt')
    text = text[:1000]
    print(text)
    print(nltk.tokenize.simple.SpaceTokenizer().tokenize(text))
    print(nltk.tokenize.sent_tokenize(text))

    for sent in nltk.tokenize.sent_tokenize(text):
        print(sent)
        print('-------')
    print(nltk.tokenize.RegexpTokenizer(r'[a-zA-Z]+').tokenize(text))
    print(nltk.tokenize.RegexpTokenizer(r'\w+').tokenize(text))
    print(nltk.tokenize.WordPunctTokenizer().tokenize(text))

def stemming():
    words = ['lives','dies','flies','died']
    st = nltk.stem.PorterStemmer()
    print(st.stem('leaves'))
    print([st.stem(w) for w in words])

    st = nltk.stem.LancasterStemmer()
    print(st.stem('leaves'))
    print([st.stem(w) for w in words])



# corpus()
# tokenize()
stemming()