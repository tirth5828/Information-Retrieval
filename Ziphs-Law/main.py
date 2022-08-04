# Importing from
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from scipy.stats import linregress
from wordcloud import WordCloud

# Importing
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import nltk

# Downloading
nltk.download('stopwords')


# Defining functions
def count_word(file_name):
    with open(file_name, encoding='utf8') as f:
        return Counter(f.read().split())


# Main
if __name__ == '__main__':
    # Opening the Book in read only mode
    book_open = open("C:\\Users\\TIRTH JOSHI\\Desktop\\IR\\Ziphs-Law\\829-0.txt", 'r', encoding='mbcs')
    data = book_open.read().lower()
    words = data.split()
    number_of_words = len(words)
    print('Number of words in text file :', number_of_words)

    # Converting file to include only small letters and formatting it
    words = [word.strip('_*-.,!;:"`()[]') for word in words]
    words = [word.strip("'") for word in words]
    words = [word.replace("'s", '') for word in words]
    words = [word.replace("`s", '') for word in words]
    with open(r'words_list.txt', 'w', encoding='utf8') as fp:
        for item in words:
            fp.write("%s\n" % item)

    # Applying Potters Stemmer
    ps = PorterStemmer()
    words = [ps.stem(word) for word in words]
    with open(r'stemmer.txt', 'w', encoding='utf8') as fp:
        for item in words:
            fp.write("%s\n" % item)

    # Graphing frequency of words
    word_freq = count_word("stemmer.txt")
    df = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
    df['Log_Freq'] = df['Frequency'].apply(lambda x: np.log(x))
    df['Rank'] = df['Frequency'].rank(ascending=False)
    df.sort_values(by='Frequency', ascending=False, inplace=True)
    print(df)
    graph = sns.lineplot(x='Word', y='Log_Freq', data=df)
    graph.set(xticklabels=[])
    plt.ylim(-1, 10)
    plt.savefig('graph.png')
    plt.show()

    # Linear Regression
    fig, ax = plt.subplots()
    x_lr = df['Rank'].values
    y_lr = df['Log_Freq'].values
    plt.scatter(x_lr, y_lr, color="m", marker="o", s=30)
    res1 = linregress(x_lr, y_lr)
    ax.plot(x_lr, res1.intercept + res1.slope * x_lr, 'r')
    plt.savefig('linear_regression.png')
    plt.show()

    # Printing results of Alpha and k in ln(f) = -(alpha)*ln(r) + k
    print("---------------------------------------------------")
    print("Alpha =", res1.slope)
    print("k =", res1.intercept)
    print("---------------------------------------------------")

    # Making the Word cloud
    filtered = {}
    for word in word_freq:
        if word not in stopwords.words('english'):
            filtered[word] = word_freq[word]

    word_cloud = WordCloud(background_color='white', max_words=100, max_font_size=50).generate_from_frequencies(
        filtered)
    plt.figure(figsize=(10, 8), facecolor=None)
    plt.imshow(word_cloud)
    plt.savefig('word_cloud.png')
    plt.show()

    # Closing the file
    book_open.close()

# ----------------------------------------------------------------------------------------------------------------------
# By- Janmay Joshi (@JanMayhem) <3
# ----------------------------------------------------------------------------------------------------------------------
