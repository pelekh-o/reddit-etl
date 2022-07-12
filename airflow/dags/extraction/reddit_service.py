import pandas as pd
import praw
import sys
from datetime import datetime
import extraction.config_helper as config_helper

SUBREDDIT = 'ukraine'


def extract_posts_data():
    posts = get_posts()

    posts_list = []
    for p in posts:
        posts_list.append(vars(p))
    extracted_df = pd.DataFrame(posts_list)
    # Leave only required columns
    headers_list = ['id', 'title', 'score', 'num_comments', 'author',
                    'downs', 'ups', 'upvote_ratio', 'total_awards_received',
                    'permalink', 'url', 'created_utc', 'is_video', 'over_18']
    extracted_df = extracted_df[headers_list]
    
    transformed = transform_posts(extracted_df)
    save_to_csv(transformed)


def get_posts(posts_count=None):
    reddit_service = get_reddit_service()

    subreddit = reddit_service.subreddit(SUBREDDIT)
    if posts_count:
        return subreddit.top(time_filter='day', limit=posts_count)
    return subreddit.top(time_filter='day', limit=None)


def get_reddit_service():
    reddit_configs = config_helper.get_config_section('reddit')
    try:
        return praw.Reddit(client_id = reddit_configs.get('client_id'),
                     client_secret = reddit_configs.get('client_secret'),
                     user_agent ='reddit-etl-ukraine')
    except Exception as ex:
        print(f'Failed to connect to Reddit API: {ex}')
        sys.exit(1)


def transform_posts(posts_df):
    # Convert time format
    posts_df['created_utc'] = pd.to_datetime(posts_df['created_utc'], unit='s')
    # Edit the permalink field to save the full URL
    posts_df['permalink'] = posts_df['permalink'].apply(lambda x: "{}{}".format('https://reddit.com', x))

    return posts_df


def save_to_csv(extracted_data):
    filename = f'/tmp/r_{SUBREDDIT}_{datetime.now().strftime("%Y%m%d")}.csv'
    extracted_data.to_csv(filename, index=False, encoding='utf-8')