import warnings
warnings.simplefilter("ignore", DeprecationWarning)
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.model_selection import GridSearchCV

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
        print("\t\tTopic #%d:" % topic_idx)
        print("\t\t"+" ".join([words[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

def lda_col(df, col, na_values, n_topics = 5, n_words_per_topic = 10):

    df = df[df[col].notna()]
    for na_value in na_values:
        df = df[df[col] != na_value]

    df[col] = df[col].astype(str)

    # Initialise the count vectorizer with the English stop words
    count_vectorizer = TfidfVectorizer(stop_words='english')
    # Fit and transform the processed titles
    try:
        count_data = count_vectorizer.fit_transform(df[col])
    except ValueError as e:
        print(e)
    else:
        # Visualise the 10 most common words
        # plot_10_most_common_words(count_data, count_vectorizer, col)

        # Grid search
        optimal_lda(count_data)

        # Tweak the two parameters below
        # Create and fit the LDA model
        #
        # lda = LDA(n_components=n_topics, n_jobs=-1)
        # lda.fit(count_data)
        # # Print the topics found by the LDA model
        # print("\tTopics found via LDA in "+col+":")
        # print_topics(lda, count_vectorizer, n_words_per_topic)

def optimal_lda(data):
    # Define Search Param
    search_params = {'n_components': [2, 3, 4, 5, 6], 'learning_decay': [.5, .7, .9]}

    # Init the Model
    lda = LDA()

    # Init Grid Search Class
    model = GridSearchCV(lda, param_grid=search_params)

    # Do the Grid Search
    model.fit(data)

    # Best Model
    best_lda_model = model.best_estimator_

    # Model Parameters
    print("Best Model's Params: ", model.best_params_)

    # Log Likelihood Score
    print("Best Log Likelihood Score: ", model.best_score_)

    # Perplexity
    print("Model Perplexity: ", best_lda_model.perplexity(data))

    # Get Log Likelyhoods from Grid Search Output
    n_topics = [10, 15, 20, 25, 30]
    log_likelyhoods_5 = [round(gscore.mean_validation_score) for gscore in model.cv_results_ if
                         gscore.parameters['learning_decay'] == 0.5]
    log_likelyhoods_7 = [round(gscore.mean_validation_score) for gscore in model.cv_results_ if
                         gscore.parameters['learning_decay'] == 0.7]
    log_likelyhoods_9 = [round(gscore.mean_validation_score) for gscore in model.cv_results_ if
                         gscore.parameters['learning_decay'] == 0.9]

    # Show graph
    plt.figure(figsize=(12, 8))
    plt.plot(n_topics, log_likelyhoods_5, label='0.5')
    plt.plot(n_topics, log_likelyhoods_7, label='0.7')
    plt.plot(n_topics, log_likelyhoods_9, label='0.9')
    plt.rcParams.update({'font.size': 22})
    plt.title("Choosing Optimal LDA Model")
    plt.xlabel("Num Topics")
    plt.ylabel("Log Likelihood Scores")
    plt.legend(title='Learning decay', loc='best')
    plt.show()


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
for i in range(4,12):
    # for n_topic in range(4,5):
    if i != 5:
        col = 't_q'+str(i)
        col_name = new_names[col]
        print(col_name)
        print('++++++++++++++++++++++++++++')
        # print('\tNumber of Topics: '+str(n_topic))
        lda_col(trigger_other, col, na_values, n_topics = 2, n_words_per_topic = 5)