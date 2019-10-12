from community import config

# DROP TABLES
staging_articles_table_drop = "DROP table IF EXISTS staging_articles"
staging_comments_table_drop = "DROP table IF EXISTS staging_comments"
top_comments_table_drop = "DROP table if EXISTS top_comments"

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


articles_copy = ("""
COPY articles(title, score, url, author, created_utc, archived, subreddit, articleid)
FROM {}
CREDENTIALS {}
region 'us-east-1'
CSV
ACCEPTANYDATE
dateformat 'auto'
maxerror as 250
IGNOREHEADER 1;
""").format(config.ARTICLES_CSV_LOCATION, config.ARN)


comments_copy = ("""
COPY comments(author, body, ups, articleid)
FROM {}
CREDENTIALS {}
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

# QUERY LISTS
create_table_queries = [
    articles_table_create,
    comments_table_create,
    top_comments_create
    ]
drop_table_queries = [
    articles_table_drop,
    comments_table_drop,
    top_comments_table_drop
    ]
copy_table_queries = [
    articles_copy,
    comments_copy,
    top_comments_sql
]