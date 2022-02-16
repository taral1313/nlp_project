import pandas as pd
from textblob import TextBlob
import streamlit as st
import altair as alt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib as plt
# Analysis functions
import plotly_express as px
df = pd.read_csv("C:/Users/Taral/Study/Master Thesis/Thesis Project/stock_files/Tesla_finviz_stock.csv")

df.drop('Unnamed: 0', axis=1, inplace=True)
# df.drop('Title', axis=1, inplace=True)
df = df[~df['News Headline'].isnull()]

def preprocess(ReviewText):
    ReviewText = ReviewText.str.replace("(<br/>)", "")
    ReviewText = ReviewText.str.replace('(<a).*(>).*(</a>)', '')
    ReviewText = ReviewText.str.replace('(&amp)', '')
    ReviewText = ReviewText.str.replace('(&gt)', '')
    ReviewText = ReviewText.str.replace('(&lt)', '')
    ReviewText = ReviewText.str.replace('(\xa0)', ' ')  
    return ReviewText
    
df['Headline Text'] = preprocess(df['News Headline'])

df['polarity'] = df['Headline Text'].map(lambda text: TextBlob(text).sentiment.polarity)

df['headline_word_length'] = df['Headline Text'].astype(str).apply(len)
df['headline_word_count'] = df['Headline Text'].apply(lambda x: len(str(x).split()))
df['char_length'] = df['Headline Text'].apply(len)
# df['char_length'].hist()
def word_cloud():
    text = ' '.join(df['Headline Text'].values)
    word_cloud = WordCloud(width=500, height=300, collocations = False, background_color = 'white').generate(text)
    return st.image(word_cloud.to_array(), use_column_width=True)

def scatter_():

    # fig, ax = plt.subplots()
    # ax.scatter(x=df['char_length'], y=df['headline_word_length'])
    plot = px.scatter(data_frame=df, x='char_length', y='headline_word_count')
        # display the chart
        
    # plt.show()
    return st.plotly_chart(plot, use_container_width=True)

def pie_ch():
    x = df['News Reporter'].value_counts()[:5].index
    y = df['News Reporter'].value_counts()[:5].values

    df_ = pd.DataFrame({'Reporter_name':x, 'count':y})
    fig = px.pie(df_, values='count', names='Reporter_name', title='News Reporter Sources', height=400)

    return st.plotly_chart(fig, use_container_width=True)

def polarity_hist():
    return st.area_chart(df['polarity'])

def alt_all_cols():   
    c = alt.Chart(df[['polarity','headline_word_length','headline_word_count']]).mark_circle().encode(
        x='headline_word_count', y='headline_word_length', size='polarity', color='polarity', tooltip=['polarity', 'headline_word_length', 'headline_word_count'])

    return st.altair_chart(c, use_container_width=True)

def lin_word():
    # p = figure(
    #  title='simple line example',
    #  x_axis_label='x',
    #  y_axis_label='y')

    # p.line(df['headline_word_length'], df['headline_word_count'], legend_label='Trend', line_width=2)
    return st.line_chart(df['headline_word_length'])


def bi_gram():
    corpus = df['Headline Text']
    n = 15
    vec = CountVectorizer(ngram_range=(2, 2)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    
    common_words = words_freq[:n]
    for word, freq in common_words:
        print(word, freq)
    df3 = pd.DataFrame(common_words, columns = ['ReviewText' , 'count'])
    dfbi_grams = df3.groupby('ReviewText').sum()['count'].sort_values(ascending=False)

    return st.bar_chart(dfbi_grams)