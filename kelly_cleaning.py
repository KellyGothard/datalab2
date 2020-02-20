## Script to explore SMAC dataset

## Imports
import pandas as pd
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt

## Functions
def na_plot(df,title,out):
    ## Plot missing data
    sns.heatmap(df.isnull(), cbar=False, cmap = 'binary')
    plt.title(title)
    plt.savefig('figs/'+out)

def word_count_dist(original_df, out):
    n_words_total = []
    data = []

    for col in original_df.columns:
        col_list = []
        for index, row in original_df.iterrows():
            try:
                text = row[col].split(' ')
                n = len(text)
            except:
                n = 0
            col_list.append(n)
            n_words_total.append(n)
        data.append(col_list)

    counted = Counter(data[0])
    df = pd.DataFrame.from_dict(counted, orient='index', columns=[original_df.columns[0]])
    for i in range(1, len(data)):
        counted = Counter(data[i])
        temp = pd.DataFrame.from_dict(counted, orient='index', columns=[df.columns[i]])
        df = df.merge(temp, how='outer', left_index=True, right_index=True)

    sns.lineplot(data=df)
    plt.ylim(0, 1000)
    plt.savefig('figs/'+out+'by_col.png')
    plt.close()

    sns.lineplot(data=df)
    plt.xscale('log')
    plt.ylim(0, 1000)
    plt.savefig('figs/'+out+'by_col_log.png')
    plt.close()

    ## Plot distribution of words in all responses
    n_words_dist = Counter(n_words_total)
    plt.title('Distribution of Words per Response')
    sns.lineplot(x=list(n_words_dist.keys()),
                 y=list(n_words_dist.values()))
    plt.savefig('figs/'+out+'.png')
    plt.close()


## Read in codes if necessary, helpful for looking up on the go
codes_df = pd.read_excel('smac/all_paper_data.xlsx',
                         sheet_name = 'Codebook',
                         skiprows = 1)

codes = codes_df.set_index('Code').T.to_dict('list')

## Read in Trigger Other sheet from all_paper_data.xlsx
trigger_other = pd.read_excel('smac/all_paper_data.xlsx',
                              sheet_name = 'Trigger Other')

new_names = {'Name_of_community':'Community', 't_q1':'Time_since?',
             't_q2': 'Action_plan?', 't_q3':'Champion?',
             't_q4':'Champ_pos?', 't_q5':'Sess_outcome?',
             't_q6':'Concerns?', 't_q7':'Common_qs?',
             't_q8':'Key_risks?', 't_q9':'Bye_laws?',
             't_q10':'Else?', 't_q11':'Do_AP?'}

trigger_other = trigger_other.rename(columns = new_names)

## Questions t_q6 to t_q11 seem to be the free response questions here
free_response = trigger_other.loc[:,'Concerns?':'Do_AP?']

## Get dist of words per response
word_count_dist(free_response, out = 'trigger_other_t_q6-11_word_dist')

## Look into missing data
na_plot(trigger_other, title='Trigger Other Missing Data', out='trigger_other_missingdata.png')


## Trying to get # of days out of question 1 'How many days since last ebola case'
# t_q1 = trigger_other['t_q1'].values
# for entry in t_q1:
#     contains_int = False
#     try:
#         for char in entry:
#             try:
#                 integer_char = int(char)
#                 contains_int = True
#             except:
#                 pass
#             else:
#                 print(integer_char)
#         if contains_int == True:
#             print('\"'+entry+'\"'+' contains integer '+str(integer_char))
#         else:
#             print('\"'+entry+'\"'+' contains no integers.')
#     except:
#         print('Error: '+str(entry))

