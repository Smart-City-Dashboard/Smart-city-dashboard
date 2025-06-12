
import streamlit as st
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import time

# Replace with your own Twitter Bearer Token
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAOu72QEAAAAA66wAs6k5mWGy2fa06Z2B7IX%2BOFU%3DQctWl6s6zTqGVOMz4yo8icnBWHNdELSxJYQcbH3iLqmoKLJb9c"

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_tweets(keyword, max_tweets=10):
    query = f"{keyword} lang:en -is:retweet"
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=min(max_tweets, 100),
            tweet_fields=["created_at", "text"]
        )
        tweets = [tweet.text for tweet in response.data] if response.data else []
        return tweets
    except tweepy.TooManyRequests:
        st.warning("⚠️ You've hit Twitter’s rate limit. Please wait 15–30 minutes and try again.")
        st.stop()
    except tweepy.Unauthorized:
        st.error("❌ Unauthorized: Check your Twitter Bearer Token.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        st.stop()

def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def plot_sentiment_distribution(sentiments):
    sentiment_series = pd.Series(sentiments)
    sentiment_counts = sentiment_series.value_counts()
    st.subheader("📊 Sentiment Distribution")
    st.bar_chart(sentiment_counts)

def generate_wordcloud(tweets):
    text = " ".join(tweets)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    st.subheader("☁️ Word Cloud of Tweets")
    st.image(wordcloud.to_array())

def show_emojis(sentiments):
    st.subheader("😊 Emoji Summary")
    pos = sentiments.count("Positive")
    neu = sentiments.count("Neutral")
    neg = sentiments.count("Negative")
    st.markdown(f"- 😀 Positive: **{pos}**")
    st.markdown(f"- 😐 Neutral: **{neu}**")
    st.markdown(f"- 😠 Negative: **{neg}**")

def run_sentiment_analysis_view():
    st.title("🧠 Twitter Sentiment Analysis")
    keyword = st.text_input("Enter a keyword or hashtag", value="smart city")
    max_tweets = st.slider("Number of Tweets", 10, 100, 30)

    if st.button("Analyze Sentiment"):
        with st.spinner("Fetching tweets and analyzing sentiment..."):
            tweets = fetch_tweets(keyword, max_tweets=max_tweets)
            if not tweets:
                st.warning("No tweets found. Try a different keyword.")
                return
            sentiments = [analyze_sentiment(tweet) for tweet in tweets]
            plot_sentiment_distribution(sentiments)
            show_emojis(sentiments)
            generate_wordcloud(tweets)
            st.success("✅ Sentiment analysis complete.")

if __name__ == "__main__":
    run_sentiment_analysis_view()
