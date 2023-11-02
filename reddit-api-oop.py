import praw
from praw.exceptions import InvalidURL

class RedditAPI:
    def __init__(self,client_id,client_secret,user_agent):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent

    # Function reddit_connection establishes connection via Reddit
    def reddit_connection(self):
        reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent
        )
        return reddit

    # Function check_subreddit_parameters validates subreddit_names. It can be either list or None type
    def format_subreddit(self,subreddit_names):
        if((subreddit_names == None) | (subreddit_names == "all")):
            return ["all"]
        elif(type(subreddit_names) is list):
            return subreddit_names
        else:
            raise ValueError("subreddit_names must be a list or None type")

    # Function format_keyword checks if user wants to ignore whitespace in keyword or not
    def format_keyword(self,keyword,ignore_keyword_whitespace):
        if(ignore_keyword_whitespace == True):
            format_keyword = f'"{keyword}"'
        elif(ignore_keyword_whitespace == False):
            format_keyword = keyword
        else:
            raise ValueError("keyword must be a string")
        return format_keyword

    # Function check_time_filter checks selection of time_filter. Returns 'all' as default
    def check_time_filter(self,time_filter):
        options = ["hour","day","week","month","year","all"]
        if(time_filter not in options):
            new_time_filter = "all"
            print("time filter is set to 'all' by default")
            return new_time_filter
        else:
            return time_filter

        # Function to pull comments from a specified Reddit post
    def pull_comments_from_post(self, post_url):
        reddit = self.reddit_connection()
        try:
            submission = reddit.submission(url=post_url)
        except InvalidURL as e:
            raise ValueError("Invalid URL. Please provide a valid Reddit post URL.")

        comments_list = [] # List where comments will be kept

        submission.comments.replace_more(limit=None)  # Retrieve all comments, including nested ones
        for comment in submission.comments.list():
            comment_info = {
                "post_url": post_url,
                "comment_author": comment.author.name if comment.author else "[deleted]",
                "comment_body": comment.body,
                "comment_score": comment.score,
            }
            comments_list.append(comment_info)

        return comments_list

    # Function pull_reddit_post_data_by_keyword is using Reddit API to pull the data from specified subreddits by searching by keyword. It also crawls comments if specified
    def pull_reddit_post_data_by_keyword(self,keyword,ignore_keyword_whitespace,time_filter="year",subreddit_names=None,include_comments=False):
        reddit = self.reddit_connection()
        subreddits = self.format_subreddit(subreddit_names=subreddit_names)
        new_keyword = self.format_keyword(keyword=keyword,
                                      ignore_keyword_whitespace=ignore_keyword_whitespace)
        new_time_filter = self.check_time_filter(time_filter=time_filter)

        all_posts_list = [] # List where posts data will be kept

        for subreddit_name in subreddits:
            subreddit = reddit.subreddit(subreddit_name)
            for submission in subreddit.search(new_keyword,limit=None,time_filter=new_time_filter):
                # Pulling post data
                post_info = {"title" : submission.title,
                             "text" : submission.selftext,
                             "url" : submission.url,
                             "subreddit" : subreddit_name,
                             "keyword" : new_keyword}
                print(f"crawling reddit post {submission.url}")

                # Pulling comment data if requested
                if(include_comments == True): # Check if user wants to pull comments data also
                    submission.comments.replace_more(limit=None)  # Retrieve all comments, including nested ones
                    for comment in submission.comments.list():
                        comment_info = {
                            "comment_author": comment.author.name if comment.author else "[deleted]",
                            "comment_body": comment.body,
                            "comment_score": comment.score,
                        }
                        full_post_info = {**post_info, **comment_info}
                        print(full_post_info)
                        all_posts_list.append(full_post_info)
                else:
                    all_posts_list.append(post_info)

            return all_posts_list


    # Function to pull all posts from a specified subreddit
    def pull_all_posts_from_subreddit(self,subreddit_name):
        reddit = self.reddit_connection()
        try:
            subreddit = reddit.subreddit(subreddit_name)
            all_posts_list = []

            for submission in subreddit.new(
                    limit=None):
                post_info = {
                    "title": submission.title,
                    "text": submission.selftext,
                    "url": submission.url,
                    "subreddit": subreddit_name
                }
                all_posts_list.append(post_info)

            return all_posts_list

        except praw.exceptions.RedditAPIException as e:
            raise ValueError(f"Error while fetching posts from {subreddit_name}: {e}")

