# Reddit API

This is a Python library that provides functionality to interact with the Reddit API using the Python Reddit API Wrapper (PRAW). It allows you to perform various tasks, such as searching for posts by keyword, fetching comments from specific Reddit posts, and pulling all posts from a specified subreddit.

## Getting Started

### Prerequisites

Before using this library, you will need to have the following:

- Reddit API credentials (client ID, client secret, user agent)
- Python installed on your system
- PRAW library installed (you can install it using pip)

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/reddit-api-python.git
```

Install the required dependencies:
```bash
pip install praw
```
Update config.json with your Reddit API credentials.

Run the Python scripts to use the library for Reddit data extraction.

Features
RedditAPI Class
reddit_connection: Establishes a connection to the Reddit API using your credentials.

format_subreddit: Validates subreddit names, allowing lists or "all" as inputs.

format_keyword: Formats keywords, optionally ignoring whitespace.

check_time_filter: Validates time filter options.

pull_comments_from_post: Retrieves comments from a specified Reddit post.

pull_reddit_post_data_by_keyword: Fetches data from specified subreddits by searching for a keyword.

pull_all_posts_from_subreddit: Retrieves all posts from a specified subreddit.


Usage
You can use the provided functions to interact with the Reddit API. See the example usage in the code and adapt it to your needs.

# Example: Pull all posts from a subreddit
```bash
reddit_api = RedditAPI(client_id='your_client_id', client_secret='your_client_secret', user_agent='your_user_agent')
subreddit_name = "example_subreddit"
all_posts = reddit_api.pull_all_posts_from_subreddit(subreddit_name)
for post in all_posts:
    print(post)
```
# Example: Pull all posts and comments by Keyword
```bash
reddit_api = RedditAPI(client_id='your_client_id', client_secret='your_client_secret', user_agent='your_user_agent')
keyword = "example keyword"
time_filter = "year"
include_comments = True
posts = reddit_api.pull_reddit_post_data_by_keyword(keyword=keyword,
                                                             ignore_keyword_whitespace=False,
                                                             time_filter=time_filter,
                                                             subreddit_names=None,
                                                             include_comments=include_comments
                                                             )
```
License
This project is licensed under the MIT License - see the LICENSE.md file for details.

Acknowledgments
This library is built using the PRAW library for Python.
Refer to the official PRAW documentation and Reddit API documentation for more details and advanced usage.
