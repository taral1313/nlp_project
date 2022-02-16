# Import the necessary libraries ------> BeautifulSoup
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen,Request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from newspaper import Article
import csv, re


"""     Get the Article....
#author=[],article_date= []
#author.append(article.authors),article_date.append(article.publish_date),df and file and scrapes the Urls for summaries.
"""    
def newspaper3k_summary_from_df(df,column_url_name="URL",output_file_name='summaries'):
    url_df= df[column_url_name]
    article_summary=[]
    title=[]
    counter= 0
    for url in url_df:
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            title.append(article.title)
            article_summary.append(article.summary)
            counter+=1
            print(counter)
        except Exception as e:
            title.append(e)
            article_summary.append(e)
            counter+=1
            print(counter)
    data = {'Article_title':title,"Article_summary": article_summary}#"Date_Time":article_date,"Author": author,
    summary_df = pd.DataFrame.from_dict(data)
    summary_df["URL"] =url_df
    summary_df.to_csv(output_file_name+".csv")
    print(output_file_name+".csv is created")
    return summary_df


def newspaper3k_summary_from_csvfile(file_name,output_file_name='summaries'):
    df = pd.read_csv(file_name).drop(["Unnamed: 0"],axis = 1)
    url_df= df["URL"]
    article_summary=[]
    title=[]
    counter= 0
    for url in url_df:
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            title.append(article.title)
            article_summary.append(article.summary)
            counter+=1
            print(counter)
        except Exception as e:
            title.append(e)
            article_summary.append(e)
            counter+=1
            print(counter)    
    data = {'Article_title':title,"Article_summary": article_summary}
    summary_df = pd.DataFrame.from_dict(data)
    summary_df["URL"] =url_df
    summary_df.to_csv(output_file_name+".csv")
    print(output_file_name+".csv is created")
    return summary_df



def finviz_parser_data(ticker):
    
    url = 'https://finviz.com/quote.ashx?t={}'.format(ticker)
    # sending request for getting the html code of the Url
    try:
        request = Request(url=url,headers={'user-agent':'my-app'})
        response = urlopen(request)

        #parsing the HTML with BeautifulSoup
        soup = BeautifulSoup(response,'html')
        return soup
    except Exception as e:
        print(e)
    
def correct_time_formatting(time_data):
    date = []
    time=[]
    for z in time_data:
        a = z.split(" ")
        if len(a) == 2:
            date.append(a[0])
            time.append(a[1])
        else:
            date.append("r")
            time.append(a[0])
    l=0
    r=1
    lister=[]
    #print(l,r)
    while r<len(date):
        if len(date[r]) ==9:
            lister.append(date[l:r])
            #print(l,r)
            l=r
            #print(l,r)
        elif r== len(date)-1:                      
                r=len(date)    
                #print(l,r)
                lister.append(date[l:r])
        r+=1
    n =0
    while n <len(lister):

        lister[n] =[lister[n][0] for x in lister[n] if x=='r' or x==lister[n][0] ]
        n+=1
    final_time= []
    y =0
    while y<len(lister):
        final_time+=lister[y]
        y+=1    
    count = 0
    time_correct =[]
    while count<len(final_time):
        time_correct.append((final_time[count]+" "+time[count]))
        count+=1
    return time_correct

def finviz_create_write_data(soup,file_name="MSFT"):   
    try:
        news_reporter_title = [row.text for row in soup.find_all(class_ ='news-link-right') if row is not None]
        #news_reporter_title
        news_reported = [row.text for row in soup.find_all(class_ ='news-link-left') if row is not None]
        #news_reported
        news_url = [row.find('a',href=True)["href"] for row in soup.find_all(class_ ='news-link-left') if row is not None]
        '''
        solution 2:
        atags = [row.find('a') for row in soup.find_all(class_ ='news-link-left') if row is not None]
        news_url = [link['href'] for link in atags]
        '''
        date_data = [row.text for row in soup.find_all('td', attrs ={"width":"130",'align':'right'}) if row is not None]
        time = correct_time_formatting(date_data)
    except Exception as e:
        print(e)
    data = { "Time":time,'News Reporter': news_reporter_title,"News Headline": news_reported, "URL": news_url }
    finviz_news_df = pd.DataFrame.from_dict(data)
    finviz_news_df.to_csv(f"C:/Users/Taral/Study/Master Thesis/Thesis Project/stock_files/{file_name}_finviz_stock.csv")
    print(file_name + "_finviz_stock.csv is created" )
    return finviz_news_df

soup = finviz_parser_data("TSLA")
finviz_create_write_data(soup,file_name="Tesla")


ticker_list = ['WOOF','MSFT',"GOOG",'FB',"AMZN"]
def create_csv_ticker_list(ticker_list):
    try:
        for ticker in ticker_list:
            soup = finviz_parser_data(ticker)
            finviz_create_write_data(soup,file_name=ticker)
    except Exception as e:
        print(e)

create_csv_ticker_list(ticker_list)


def finviz_view_pandas_dataframe(ticker):
    url = 'https://finviz.com/quote.ashx?t={}'.format(ticker)
    # sending request for getting the html code of the Url
    try:
        request = Request(url=url,headers={'user-agent':'my-app'})
        response = urlopen(request)
        news_reporter_title = [row.text for row in soup.find_all(class_ ='news-link-right') if row is not None]
        news_reported = [row.text for row in soup.find_all(class_ ='news-link-left') if row is not None]
        news_url = [row.find('a',href=True)["href"] for row in soup.find_all(class_ ='news-link-left') if row is not None]
        date_data = [row.text for row in soup.find_all('td', attrs ={"width":"130",'align':'right'}) if row is not None]
        time = correct_time_formatting(date_data)
    except Exception as e:
        print(e)
    data = { "Time":time,'News Reporter': news_reporter_title,"News Headline": news_reported, "URL": news_url }
    finviz_news_df = pd.DataFrame.from_dict(data)
    return finviz_news_df


# def on_ticker_input(ticker):
google_stock = finviz_view_pandas_dataframe('GOOG')


google_stock["Time_pdformat"]= pd.to_datetime(google_stock['Time'],infer_datetime_format=True)
    # google_stock


#google_stock = finviz_view_pandas_dataframe('GOOG') previously executed
# Url= google_stock["URL"]
# Url

google_stock5 = google_stock.head(12)
newspaper3k_summary_from_df(google_stock5,output_file_name=f'GOOG_summaries')

# google_summaries5 = pd.read_csv("google_summaries.csv")
# for i, txt in enumerate(google_summaries5.Article_title):
#     if '403' not in txt:
#         print(txt)
# #         print(i)
#         print("True", i)
#         break
        

# google_summaries5.head()


