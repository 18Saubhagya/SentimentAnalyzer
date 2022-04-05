from ast import Return
from fileinput import filename
from sqlite3 import dbapi2
from statistics import mode
from turtle import heading, width
import pandas as pd
import tweepy
import re
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def scrape(words, date_since, numtweet,db):
    tweets = tweepy.Cursor(api.search_tweets,words, lang="en",since_id=date_since,tweet_mode='extended').items(numtweet)
    list_tweets = [tweet for tweet in tweets]
    i = 1
    for tweet in list_tweets:
        username = tweet.user.screen_name
        location = tweet.user.location
        hashtags = tweet.entities['hashtags']
        is_retweet = hasattr(tweet, 'retweeted_status')
        if is_retweet==True:
            continue
        else:
            text = tweet.full_text
            text=text.lower()
            hashtext = list()
            for j in range(0, len(hashtags)):
                hashtext.append(hashtags[j]['text'])
                ith_tweet = [username,location,text,hashtext]
                db.loc[len(db)] = ith_tweet
                i = i+1


def clean(tweet):
    tweet=re.sub(r'@[A-Za-z0-9]+','',tweet)
    tweet=re.sub(r'#','',tweet)
    tweet=re.sub(r'https?:\/\/\S+','',tweet)
    return tweet

def preprocess(tweet):
    stop=stopwords.words('english')
    x=word_tokenize(tweet)
    words=[word for word in x if word not in (stop)]
    ps=PorterStemmer()
    swords=[ps.stem(a) for a in words]
    lem=WordNetLemmatizer()
    lwords=[lem.lemmatize(w,pos='a') for w in swords]
    return " ".join(lwords)

def subject(tweet):
    return TextBlob(tweet).sentiment.subjectivity

def polar(tweet):
    return TextBlob(tweet).sentiment.polarity

def analysis(point):
    if point<0 :
        return 'Negative'
    elif point==0 :
        return 'Neutral'
    else:
        return 'Positive'

def percent(s,df):
    twee=df[df.analysis==s]
    twee=twee['text']
    if df.shape[0]==0:
        return 0.00
    return round((twee.shape[0]/df.shape[0])*100,2)

def answer(df):
    df['subjectivity']=df['text'].apply(subject)
    df['polarity']=df['text'].apply(polar)
    df['analysis']=df['polarity'].apply(analysis)
    positivet=percent('Positive',df)
    negativet=percent('Negative',df)
    neutralt=percent('Neutral',df)
    return [{'positive':positivet},{'negative':negativet},{'neutral':neutralt}]

def find(input):
    db = pd.DataFrame(columns=['username','location','text','hashtags'])
    date=datetime.now()
    date=date-relativedelta(months=+6)
    words = input
    numtweet = 100
    scrape(words, date, numtweet,db)
    db['text']=db['text'].apply(clean)
    db['text']=db['text'].apply(preprocess)
    #db.to_csv(path_or_buf=r"C:\\Users\\Acer\\Desktop\\projects\\sentiment\\scraped_tweets.csv")
    words=' '.join([t for t in db['text']])
    wordcloud=WordCloud(width=500,height=300,random_state=21,max_font_size=119).generate(words)
    wordcloud.to_file("C:/Users/Acer/Desktop/projects/static/first_review.png")
    engine=db[db['text'].str.contains("engine") | db['text'].str.contains("fuel") | db['text'].str.contains("motor") | db['text'].str.contains("diesel") | db['text'].str.contains("shape") | db['text'].str.contains("petrol")]
    mileage=db[db['text'].str.contains("mileage") | db['text'].str.contains("distance") | db['text'].str.contains("range") | db['text'].str.contains("mile") | db['text'].str.contains("speed") | db['text'].str.contains("time")]
    comfort=db[db['text'].str.contains("comfort") | db['text'].str.contains("easy") | db['text'].str.contains("relief") | db['text'].str.contains("assure") | db['text'].str.contains("poor") | db['text'].str.contains("stress") | db['text'].str.contains("discomfort") | db['text'].str.contains("suffer")]
    safe=db[db['text'].str.contains("safe") | db['text'].str.contains("secure") | db['text'].str.contains("protect") | db['text'].str.contains("guard") | db['text'].str.contains("danger") | db['text'].str.contains("harm") | db['text'].str.contains("damage")]
    #engine.to_csv(path_or_buf=r"C:\\Users\\Acer\\Desktop\\projects\\SocialMediaSentiment\\engine.csv")
    #mileage.to_csv(path_or_buf=r"C:\\Users\\Acer\\Desktop\\projects\\SocialMediaSentiment\\mileage.csv")
    #comfort.to_csv(path_or_buf=r"C:\\Users\\Acer\\Desktop\\projects\\SocialMediaSentiment\\comfort.csv")
    #safe.to_csv(path_or_buf=r"C:\\Users\\Acer\\Desktop\\projects\\SocialMediaSentiment\\safe.csv")
    main=answer(db)
    eng=answer(engine)
    mil=answer(mileage)
    com=answer(comfort)
    saf=answer(safe)
    print('Scraping has been completed!')
    return [{'Sentiments':main},{'Engine':eng},{'Mileage':mil},{'Comfort':com},{'Safety':saf}]
#print(find(x))


#print(find("#honda"))

    

