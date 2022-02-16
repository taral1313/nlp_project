from pydoc import text
from nbformat import write
from numpy import column_stack
import streamlit as st
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
# from transformers import pipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from load_models import question_answering, sentiment, summarization
# from scrapper import finviz_parser_data, finviz_create_write_data, finviz_view_pandas_dataframe, newspaper3k_summary_from_df
from wordcloud import WordCloud
from transformers import PegasusTokenizer, PegasusForConditionalGeneration, TFPegasusForConditionalGeneration
import matplotlib.pyplot as plt
# from matplotlib import animation, cbook
from analysis import bi_gram, pie_ch, polarity_hist, alt_all_cols, lin_word, scatter_, word_cloud
from tika import parser

st.set_page_config(
    page_title = 'Streamlit Sample Dashboard Template',
    page_icon = '✅',
    layout = 'wide'
)

st.sidebar.write("Tasks")
option = st.sidebar.selectbox("Which task? ", ("Text Analysis", "Sentiment", "Summarization", "Question-Answering with user input"))
st.header(option)

google_summaries5 = pd.read_csv("google_summaries.csv")


if option == 'Text Analysis':
    # st.subheader("Text analysis")
    
    chart1, chart2 = st.columns(2)
    with chart1:
        # st.text("Sentiment Polarity of the headlines")
        st.markdown(f"<h6 style='text-align: center; color: black;'>Sentiment Polarity of the news</h6>", unsafe_allow_html=True)
        polarity_hist()
    
    with chart2:
        # st.text("Headline length, Polarity and word count")
        st.markdown(f"<h6 style='text-align: center; color: black;'>Length of news, Polarity and word count</h6>", unsafe_allow_html=True)
        alt_all_cols()
    
    chart3, chart4 = st.columns(2)

    with chart3:
         # st.text("Line chart for length of headline articles")
        st.markdown(f"<h6 style='text-align: center; color: black;'>News reporter and sources</h6>", unsafe_allow_html=True)
        pie_ch()

    with chart4:
    
        # st.text("Word cloud showing the most used words")
        st.markdown(f"<h6 style='text-align: center; color: black;'>Common words Wordcloud</h6>", unsafe_allow_html=True)
        word_cloud()

    chart5, chart6 = st.columns(2)

    with chart5:
        st.markdown(f"<h6 style='text-align: center; color: black;'>Top 20 Bigrams</h6>", unsafe_allow_html=True)
        bi_gram()
    # lin_word()
    with chart6:
        st.markdown(f"<h6 style='text-align: center; color: black;'>Scatterplot for word count and Length of news</h6>", unsafe_allow_html=True)
        scatter_()


if option == 'Sentiment':
    # user_input = st.text_input("Text for sentiment Analysis", value='')
    summary_list = []
    
    for i, txt in enumerate(google_summaries5.Article_title):
        if '403' not in txt:
            summary_list.append(txt)

    sentiment_out = sentiment(summary_list)
    for i in range(len(sentiment_out)):
        # st.subheader("Summarized text: ", txt)
        # st.text(f'{i+1}. {summary_list[i]}')
        st.markdown(f"<h6 style='text-align: center; color: blue;'>{i+1}. {summary_list[i]}</h6>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; color: black;'>{sentiment_out[i]}</h4>", unsafe_allow_html=True)
        # st.text(sentiment_out[i])
  

if option == 'Summarization':
    # user_input_s = st.text_input("Enter text to summarize", value='')

    summary_list = []
    # google_summaries5 = pd.read_csv("google_summaries.csv")
    for i, txt in enumerate(google_summaries5.Article_summary):
        if '403' not in txt:
            summary_list.append(txt)

    sum_out = summarization(summary_list)
    for i in range(len(sum_out)):
        # st.subheader("Summarized text: ", txt)
        st.text(f'{i+1}. {summary_list[i]}')
        st.markdown(f"<h3 style='text-align: center; color: green;'>{sum_out[i]}</h3>", unsafe_allow_html=True)

        
# from scrapper import on_ticker_input
if option == 'Question-Answering with user input':
    uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
    if uploaded_file is not None:
        raw = parser.from_file(uploaded_file)
    # context = st.text_input("Enter the text paragraph", value='')
        question = st.text_input("Enter the question?", value='')
        context = raw[0:1000]

        st.subheader("Answer: ")

        question_answering(question, context)
        qa_summary = summarization([context])
        qa_sentiment = sentiment([context])
        # st.markdown(f"<h4 style='text-align: center; color: black;'>Sentiment: {context}</h4>", unsafe_allow_html=True)
        # st.markdown(f"<h4 style='text-align: center; color: green;'>Summary: {context}</h4>", unsafe_allow_html=True)

        st.markdown(f"<h4 style='text-align: center; color: black;'>Sentiment: {qa_sentiment[0]}</h4>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; color: green;'>Summary: {qa_summary[0]}</h4>", unsafe_allow_html=True)

    # on_ticker_input(tic)

    # -------------------------------------
    




# text_for_summary()
# def text_for_summary():
#     soup = finviz_parser_data("TSLA")
#     finviz_create_write_data(soup, file_name="Tesla")

#     google_stock = finviz_view_pandas_dataframe('GOOG')
# # google_stock
#     # file_name_n = 'GOOG'
#     google_stock["Time_pdformat"]= pd.to_datetime(google_stock['Time'],infer_datetime_format=True)
#     # google_stock.to_csv(f'C:/Users/Taral/Study/Master Thesis/Thesis Project/stock_files/{file_name_n}_finviz_stock.csv')
#     google_stock5 = google_stock.head(12)
#     newspaper3k_summary_from_df(google_stock5,output_file_name='google_summaries')

#     google_summaries5 = pd.read_csv("google_summaries.csv")
#     app = []
#     for i, txt in enumerate(google_summaries5.Article_summary):
#         if '403' not in txt:
#             app.append(txt)
            
#     return(app[0])
