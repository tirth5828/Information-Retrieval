import re
import collections
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def process_text(text):
    # Remove punctuation and make everything lowercase
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = text.split()
    return words

def compute_word_frequencies(words):
    word_counts = collections.Counter(words)
    return word_counts

def zipfs_law(word_counts):
    sorted_word_counts = word_counts.most_common()
    ranks = range(1, len(sorted_word_counts) + 1)
    frequencies = [freq for word, freq in sorted_word_counts]
    return ranks, frequencies

def plot_zipfs_law(ranks, frequencies):
    plt.figure(figsize=(10, 6))
    plt.loglog(ranks, frequencies, marker=".")
    plt.title("Zipf's Law")
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.grid(True, which="both", linestyle="--")
    return plt

def plot_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, frequencies = zip(*top_words)
    plt.figure(figsize=(10, 6))
    plt.bar(words, frequencies)
    plt.title(f"Top {top_n} Most Frequent Words")
    plt.xlabel("Words")
    plt.ylabel("Frequencies")
    return plt

# Streamlit app

def main():
    st.title("Zipf's Law Visualization")

    st.header("What is Zipf's Law?")
    st.write("""
    Zipf's Law is an empirical law formulated using mathematical statistics that refers to the fact that many types of data studied in the physical and social sciences can be approximated with a Zipfian distribution, a kind of power law distribution. The law is named after the linguist George Zipf, who first proposed it.

    Zipf's Law states that in a given corpus of natural language, the frequency of any word is inversely proportional to its rank in the frequency table. For example, the second most common word occurs half as often as the most common word, the third most common word occurs one-third as often, and so on.
    """)

    st.header("Implications of Zipf's Law")
    st.write("""
    Zipf's Law has significant implications in various fields:
    - **Linguistics**: It helps in understanding the distribution of words in natural languages.
    - **Information Retrieval**: It aids in designing efficient algorithms for searching and indexing.
    - **Data Compression**: The predictable distribution of words can be leveraged for better compression algorithms.
    - **Social Sciences**: It can be used to analyze patterns in human behavior and social dynamics.
    """)
    
    st.header("Try it Out!")

    uploaded_file = st.file_uploader("Choose a text file", type="txt")
    
    if uploaded_file is not None:
        # Read the file content
        text = uploaded_file.read().decode("utf-8")
        
        # Process the text
        words = process_text(text)

        # Compute word frequencies
        word_counts = compute_word_frequencies(words)

        # Apply Zipf's law
        ranks, frequencies = zipfs_law(word_counts)

        st.header("Word Frequencies")
        st.write(pd.DataFrame(word_counts.items(), columns=["Word", "Frequency"]))

        st.header("Zipf's Law Plot")
        st.pyplot(plot_zipfs_law(ranks, frequencies))

        st.header(f"Top 10 Most Frequent Words")
        st.pyplot(plot_top_words(word_counts))

if __name__ == "__main__":
    main()
