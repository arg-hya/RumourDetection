import mysql.connector
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import json
import tweepy
import re
import urllib.request
import ssl

host="localhost"
user="root"
password=""
db_name="tweet"

CONSUMER_KEY = "ZQOemQvcZol76yOFZUPrbBmeX"
CONSUMER_SECRET = "oI3GotFv9TFiOmrRSuHlN2jpRCZO2LwW8d94XIpbXtx8tUyoXz"
OAUTH_TOKEN = "1400825474444525571-PqMxHAIRlqoJ0zMP1jiEgs6H7phnbN"
OAUTH_TOKEN_SECRET = "6vJgEM1PZUA0Cc4ySwDoeySAHVCn2Y1KQSTE8IP2nvjDb"



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
OUTPUT_FILE = 'output.txt'

def get_tweet_id():
    f = open('rumor_detection_acl2017/twitter15/source_tweets.txt')
    lines = f.readlines()
    for line in lines:
        tweet_id = line.split('\t')[0]
        sql_command = "INSERT INTO tweet (tweet_id) VALUES ('" + tweet_id + "')"
        mycursor.execute(sql_command)
        db.commit()
        # with open(OUTPUT_FILE, 'a') as the_file:
        #     the_file.write(tweet_id + '\n')

def extract_url_from_tweet_id():
    # f = open(OUTPUT_FILE)
    # lines = f.readlines()
    sql_command = "SELECT tweet_id FROM tweet WHERE status=\'ERROR\'"
    mycursor.execute(sql_command)
    tweet_id_all = mycursor.fetchall()
    for tweet_id in tweet_id_all:
        # string_current = lines[index].split('\n')[0]
        # tweet_id = lines[index].split('\n')[0]
        tweet_id_string = tweet_id[0]
        try:
            status = api.get_status(tweet_id_string)
            entity = status.entities
            urls = entity.get('urls')
            if len(urls) > 0:
                url = urls[0].get('expanded_url')
            # tweet = api.get_status(tweet_id_string).text


            sql_command = "UPDATE tweet SET url=\'" + url + "\' WHERE tweet_id=" + tweet_id_string
            mycursor.execute(sql_command)
            db.commit()
        except Exception as e:
            continue

def get_headline_and_contents():
    # f_read = open(OUTPUT_FILE)
    # lines = f_read.readlines()
    sql_command = "SELECT id, tweet_id, url FROM tweet WHERE url IS NOT NULL AND id > 776"
    mycursor.execute(sql_command)
    lines = mycursor.fetchall()
    for line in lines:
        id = line[0]
        tweet_id = line[1]
        url = line[2]
        print("Get headline and content for tweet " + str(id))
        try:
            response = requests.get(url,verify=False)
            if (response.status_code == 200):
                headline = get_headlines(response.text)
                if headline != 'JavaScript is not available.':
                    sql_command = "UPDATE tweet SET url_status= \'OK\' WHERE tweet_id=" +tweet_id
                    mycursor.execute(sql_command)
                    db.commit()

                    sql_command = "UPDATE tweet SET headline= %s WHERE tweet_id= %s"
                    val = (headline, tweet_id)
                    mycursor.execute(sql_command, val)
                    db.commit()
                else:  #this is a Tweet without link
                    sql_command = "UPDATE tweet SET url_status= \'Tweet URL\' WHERE tweet_id=" + tweet_id
                    mycursor.execute(sql_command)
                    db.commit()
            else:
                sql_command = "UPDATE tweet SET url_status= \'NOT OK\' WHERE tweet_id=" + tweet_id
                mycursor.execute(sql_command)
                db.commit()

        except Exception as e:
            sql_command = "UPDATE tweet SET status= \'ERROR\' WHERE tweet_id=" + tweet_id
            mycursor.execute(sql_command)
            db.commit()
            print(e)
            continue

def get_headline_and_contents_for_error():
    # f_read = open(OUTPUT_FILE)
    # lines = f_read.readlines()
    sql_command = "SELECT id, tweet_id, url FROM tweet WHERE status= \'ERROR\' AND id > 737"
    mycursor.execute(sql_command)
    lines = mycursor.fetchall()
    for line in lines:
        id = line[0]
        tweet_id = line[1]
        url = line[2]
        print("Get headline for tweet error" + str(id))
        try:
            # response = requests.get(url,verify=False)
            response = requests.get(url, verify=False)
            if (response.status_code == 200):
                headline = get_headlines(response.text)
                if headline != 'JavaScript is not available.':
                    sql_command = "UPDATE tweet SET url_status= \'OK\' WHERE tweet_id=" +tweet_id
                    mycursor.execute(sql_command)
                    db.commit()

                    sql_command = "UPDATE tweet SET status= NULL WHERE tweet_id=" + tweet_id
                    mycursor.execute(sql_command)
                    db.commit()

                    sql_command = "UPDATE tweet SET headline= %s WHERE tweet_id= %s"
                    val = (headline, tweet_id)
                    mycursor.execute(sql_command, val)
                    db.commit()
                else:  #this is a Tweet without link
                    sql_command = "UPDATE tweet SET url_status= \'Tweet URL\' WHERE tweet_id=" + tweet_id
                    mycursor.execute(sql_command)
                    db.commit()

                    sql_command = "UPDATE tweet SET status= NULL WHERE tweet_id=" + tweet_id
                    mycursor.execute(sql_command)
                    db.commit()
            else:
                sql_command = "UPDATE tweet SET url_status= \'NOT OK\' WHERE tweet_id=" + tweet_id
                mycursor.execute(sql_command)
                db.commit()

                sql_command = "UPDATE tweet SET status= NULL WHERE tweet_id=" + tweet_id
                mycursor.execute(sql_command)
                db.commit()

        except Exception as e:
            print(e)
            continue




def get_contents():
    # f_read = open(OUTPUT_FILE)
    # lines = f_read.readlines()
    sql_command = "SELECT id, tweet_id, url FROM tweet WHERE headline IS NOT NULL AND content IS NULL"
    mycursor.execute(sql_command)
    lines = mycursor.fetchall()
    for line in lines:
        id = line[0]
        tweet_id = line[1]
        url = line[2]
        print("Get content for tweet " + str(id))
        try:
            response = requests.get(url,verify=False, timeout=10)
            if (response.status_code == 200):
                content = get_content_from_html(response.text)
                sql_command = "UPDATE tweet SET content = %s WHERE tweet_id = %s"
                val = (content, tweet_id)
                mycursor.execute(sql_command, val)
                db.commit()
            else:
                pass
                # sql_command = "UPDATE tweet SET url_status= \'NOT OK\' WHERE tweet_id=" + tweet_id
                # mycursor.execute(sql_command)
                # db.commit()

        except Exception as e:
            # sql_command = "UPDATE tweet SET status= \'ERROR\' WHERE tweet_id=" + tweet_id
            # mycursor.execute(sql_command)
            # db.commit()
            print(e)
            continue


def get_headlines(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    headlines = soup.find_all('h1')
    headline_longest = headlines[0].text
    #get the longest headline
    for headline in headlines:
        if len(headline.text) > len(headline_longest):
            headline_longest = headline.text
    return headline_longest

def get_content_from_html(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    p_tag_list = soup.find_all('p')
    content = ''
    for p_tag in p_tag_list:
        content = content + p_tag.text
    content = remove_emoji(content)
    return content


def get_original_tweet():
    f = open('rumor_detection_acl2017/twitter15/source_tweets.txt')
    lines = f.readlines()
    for line in lines:
        try:
            tweet_id = line.split('\t')[0]
            original_tweet = line.split('\t')[1]
            original_tweet = original_tweet.split('\n')[0]
            original_tweet = remove_emoji(original_tweet)
            sql_command = "UPDATE tweet SET original_tweet= %s WHERE tweet_id= %s"
            val = (original_tweet, tweet_id)
            mycursor.execute(sql_command, val)
            db.commit()
        except Exception as e:
            print(e)
            continue


def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def write_to_file():
    sql_command = "SELECT id, tweet_id, headline, content FROM tweet WHERE headline IS NOT NULL AND content IS not NULL"
    mycursor.execute(sql_command)
    lines = mycursor.fetchall()
    for line in lines:
        id = line[0]
        tweet_id = line[1]
        headline = line[2]
        content = line[3]
        print("Write to file  " + str(id))
        file_name = "headline_and_content/" + tweet_id + ".json"
        file = open(file_name, "w+")
        dict_of_objetct = {"id": tweet_id, "headline": headline, "content": content}
        jsonString = json.dumps(dict_of_objetct)
        file.write(jsonString)
        file.close()

if __name__ == "__main__":
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        # session = requests.Session()
        # retry = Retry(connect=3, backoff_factor=0.5)
        # adapter = HTTPAdapter(max_retries=retry)
        # session.mount('http://', adapter)
        # session.mount('https://', adapter)
        db = mysql.connector.connect(host=host, user=user, passwd=password, database=db_name)
        mycursor = db.cursor()

        # get_original_tweet()
        # extract_url_from_tweet_id()
        # get_headline_and_contents()
        # get_headline_and_contents_for_error()
        # get_contents()
        write_to_file()
        print("End")
    except Exception as e:
        print(e)
        print("here")