import pandas as pd
import praw
import sys
from datetime import datetime
import extraction.config_helper as config_helper

SUBREDDIT = 'ukraine'
POSTS_NUM = None

def extract_posts_data():
    reddit_service = _get_reddit_service()
    subreddit = reddit_service.subreddit(SUBREDDIT)
    subbmissions = subreddit.top(time_filter='day', limit=POSTS_NUM)

    subbmissions_list = []
    for s in subbmissions:
        s = vars(s)
        s = {k:str(v) for k, v in s.items()}
        #s = dict((k,str(v)) for k,v in s.items())
        subbmissions_list.append(s)
    print(f'Retrieved {len(subbmissions_list)} subbmissions from reddit')
    return subbmissions_list


def _get_reddit_service():
    reddit_configs = config_helper.get_config_section('reddit')
    try:
        return praw.Reddit(client_id = reddit_configs.get('client_id'),
                     client_secret = reddit_configs.get('client_secret'),
                     user_agent ='reddit-etl-ukraine')
    except Exception as ex:
        print(f'Failed to connect to Reddit API: {ex}')
        sys.exit(1)


def transform_posts(posts_list):
    headers_list = ['id', 'title', 'score', 'num_comments', 'author',
                    'downs', 'ups', 'upvote_ratio', 'total_awards_received',
                    'permalink', 'url', 'created_utc', 'is_video', 'over_18']
    posts_list = [{key: d[key] for key in headers_list} for d in posts_list]
    for p in posts_list:
        # Edit the permalink field to save the full URL
        p.update((k, f'https://reddit.com{v}') for k, v in p.items() if k == "permalink")
        # Convert time format
        p.update((k, datetime.utcfromtimestamp(float(v)).strftime('%Y-%m-%dT%l:%M:%S%z')) for k, v in p.items() if k == "created_utc")
    return posts_list


def save_to_csv(extracted_data):
    extracted_data_df = pd.DataFrame(extracted_data)
    filename = f'/tmp/r_{SUBREDDIT}_{datetime.now().strftime("%Y%m%d")}.csv'
    extracted_data_df.to_csv(filename, index=False, encoding='utf-8')
    