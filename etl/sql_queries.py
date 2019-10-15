from community import config

# DROP TABLES
top_comments_table_drop = "DROP table if EXISTS top_comments"
youtube_general_table_drop = "DROP table if EXISTS youtube_general"
articles_table_drop = "DROP table IF EXISTS articles"
comments_table_drop = "DROP table IF EXISTS comments"

# CREATE TABLES
articles_table_create= ("""
CREATE TABLE IF NOT EXISTS articles
(
    title VARCHAR(1000),
    score INT,
    url VARCHAR(1000),
    author VARCHAR,
    created_utc DATE,
    archived DATE,
    subreddit VARCHAR,
    articleid VARCHAR
);
""")


comments_table_create = ("""
CREATE TABLE IF NOT EXISTS comments
(
    author VARCHAR,
    body VARCHAR(15000),
    ups INT,
    articleid VARCHAR
);
""")

top_comments_create = ("""
CREATE TABLE IF NOT EXISTS top_comments
(
    articleid VARCHAR,
    title VARCHAR(1000),
    created_utc DATE,
    subreddit VARCHAR,
    author VARCHAR,
    body VARCHAR(15000),
    ups INT
);
""")

youtube_general_create = ("""
CREATE TABLE IF NOT EXISTS youtube_general
(
    channel_id VARCHAR,
    channel_title VARCHAR,
    comment_count INT,
    like_count INT,
    title VARCHAR,
    view_count INT
);
""")

articles_copy = ("""
COPY articles(title, score, url, author, created_utc, archived, subreddit, articleid)
FROM '{}'
CREDENTIALS '{}'
region 'us-east-1'
CSV
ACCEPTANYDATE
dateformat 'auto'
maxerror as 250
IGNOREHEADER 1;
""").format(config.ARTICLES_CSV_LOCATION, config.ARN)


comments_copy = ("""
COPY comments(author, body, ups, articleid)
FROM '{}'
CREDENTIALS '{}'
region 'us-east-1'
ACCEPTINVCHARS AS '_'
CSV
dateformat 'auto'
maxerror as 250
IGNOREHEADER 1;
""").format(config.COMMENTS_CSV_LOCATION, config.ARN)

top_comments_sql = ("""
CREATE Table top_comments as SELECT A.articleid, A.title, A.created_utc, A.subreddit, B.author, B.body, B.ups
FROM articles A
LEFT JOIN comments B ON A.articleid = B.articleid 
WHERE B.ups > 500
""")

youtube_general_copy = ("""
COPY youtube_general(channel_id, channel_title,	comment_count,	like_count,	title,	view_count)
FROM '{}'
CREDENTIALS '{}'
region 'us-east-1'
ACCEPTINVCHARS AS '_'
CSV
dateformat 'auto'
maxerror as 250
IGNOREHEADER 1;
""").format(config.YOUTUBE_CSV_LOCATION, config.ARN)


# QUERY LISTS
create_table_queries = [
    articles_table_create,
    comments_table_create,
    top_comments_create,
    youtube_general_create,
    ]

drop_table_queries = [
    articles_table_drop,
    comments_table_drop,
    top_comments_table_drop,
    youtube_general_table_drop,
    ]

copy_table_queries = [
    # articles_copy,
    # comments_copy,

    youtube_general_copy,
]