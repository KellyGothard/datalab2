import warnings

warnings.simplefilter("ignore", DeprecationWarning)
# Load the LDA model from sk-learn
from sklearn.decomposition import LatentDirichletAllocation as LDA

# Load the library with the CountVectorizer method
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_style('whitegrid')

# Helper function
def plot_10_most_common_words(count_data, count_vectorizer, col):
    import matplotlib.pyplot as plt
    words = count_vectorizer.get_feature_names()
    total_counts = np.zeros(len(words))
    for t in count_data:
        total_counts += t.toarray()[0]

    count_dict = (zip(words, total_counts))
    count_dict = sorted(count_dict, key=lambda x: x[1], reverse=True)[0:10]
    words = [w[0] for w in count_dict]
    counts = [w[1] for w in count_dict]
    x_pos = np.arange(len(words))

    plt.figure(2, figsize=(15, 15 / 1.6180))
    plt.subplot(title='10 most common words')
    sns.set_context("notebook", font_scale=1.25, rc={"lines.linewidth": 2.5})
    sns.barplot(x_pos, counts, palette='husl')
    plt.xticks(x_pos, words, rotation=90)
    plt.xlabel('words')
    plt.ylabel('counts')
    plt.title('10 Most Common Words in '+col)
    plt.savefig('figs/'+col+'_top10.png')

# Helper function
def print_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

def lda_col(df, col, na_values, n_topics = 5, n_words_per_topic = 10):

    df = df[df[col].notna()]
    for na_value in na_values:
        df = df[df[col] != na_value]

    df[col] = df[col].astype(str)

    # Initialise the count vectorizer with the English stop words
    count_vectorizer = CountVectorizer(stop_words='english')
    # Fit and transform the processed titles
    try:
        count_data = count_vectorizer.fit_transform(df[col])
    except ValueError as e:
        print(e)
    else:
        # Visualise the 10 most common words
        plot_10_most_common_words(count_data, count_vectorizer, col)

        # Tweak the two parameters below
        # Create and fit the LDA model
        lda = LDA(n_components=n_topics, n_jobs=-1)
        lda.fit(count_data)
        # Print the topics found by the LDA model
        print("Topics found via LDA in "+col+":")
        print_topics(lda, count_vectorizer, n_words_per_topic)


## Read in Trigger Other sheet from all_paper_data.xlsx
trigger_other = pd.read_excel('smac/all_paper_data.xlsx',
                              sheet_name = 'Trigger Other')

new_names = {'Name_of_community':'Community', 't_q1':'Time_since?',
             't_q2': 'Action_plan?', 't_q3':'Champion?',
             't_q4':'Champ_pos?', 't_q5':'Sess_outcome?',
             't_q6':'Concerns?', 't_q7':'Common_qs?',
             't_q8':'Key_risks?', 't_q9':'Bye_laws?',
             't_q10':'Else?', 't_q11':'Do_AP?'}

na_values = [0,'0','000']
for i in range(1,11):
    col = 't_q'+str(i)
    col_name = new_names[col]
    print(col_name)
    lda_col(trigger_other, col, na_values)