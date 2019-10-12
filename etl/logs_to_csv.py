import pandas as pd
import boto3
import json
from io import StringIO
import datetime as dt
from datetime import date
# Use the bucket to get keys
s3 = boto3.resource('s3')
buck = s3.Bucket('wsankey-capstone')
# Load json files using the client
s3cli = boto3.client('s3')

ARTICLE_CSV_FILES_ALREADY_EXISTING = [i.key for i in buck.objects.filter(Prefix='articlecsvs')]
COMMENT_CSV_FILES_ALREADY_EXISTING = [i.key for i in buck.objects.filter(Prefix='commentcsvs')]
ARTICLE_KEYS = ["title", "score", "url", "author", "created_utc", "archived", "subreddit", "articleid"]
COMMENT_KEYS = ["articleid", "author", "body", "ups"]
PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_- "   


def main():
    """
    For log files that we haven't processed, mainpulate them
    into dataframes then push them to S3.
    """
    for log in buck.objects.filter(Prefix='articles'):
        num = 0
        filename = 'articlecsvs/' + log.key.split("/")[1].split('.')[0]
        if (log.key == 'articles/') or (filename  + str(num) + '.csv' in ARTICLE_CSV_FILES_ALREADY_EXISTING):
            pass
        else:
            dat = []
            data = s3cli.get_object(Bucket='wsankey-capstone', Key=log.key)
            data = json.loads(data['Body'].read())

            for key, value in data.items():
                if isinstance(value, dict):        
                    value['articleid'] = str(key)
                    title = str(value.get('title', 'none').strip('"'))
                    title = title.replace('"', '')
                    value['title'] = title
                    val = {k:v for (k, v) in value.items() if k in ARTICLE_KEYS}
                    dat.append(val)
                    if len(dat) > 95:
                        csv_buffer = StringIO()
                        num += 1
                        df = pd.DataFrame(dat)
                        df.to_csv(csv_buffer, index=False)
                        s3.Object('wsankey-capstone', filename + str(num) + '.csv').put(Body=csv_buffer.getvalue())
                        del df
                        ARTICLE_CSV_FILES_ALREADY_EXISTING.append(filename + str(num) + '.csv')
                        print("Saved {} to bucket".format(filename + str(num)))
                        dat = []
                        del csv_buffer
    # Comments             
    for log in buck.objects.filter(Prefix='comments'):
        filename = 'commentcsvs/' + log.key.split("/")[1].split('.')[0] + '.csv'
        if (log.key == 'comments/') or (filename in COMMENT_CSV_FILES_ALREADY_EXISTING):
            pass
        else:
            dat = []
            data = s3cli.get_object(Bucket='wsankey-capstone', Key=log.key)
            data = json.loads(data['Body'].read())

            for key, value in data.items():
                if isinstance(value, dict) and isinstance(value['ups'], int):
                    value['articleid'] = value['article_id']
                    body = value['body']
                    body = ''.join(c for c in body if c in PERMITTED_CHARS)

                    value['body'] = body
                    val = {k:v for (k, v) in value.items() if k in COMMENT_KEYS}
                    dat.append(val)

            df = pd.DataFrame(dat)
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            s3.Object('wsankey-capstone', filename).put(Body=csv_buffer.getvalue())
            del df
            COMMENT_CSV_FILES_ALREADY_EXISTING.append(filename)
            print("Saved {} to bucket".format(filename))
            dat = []
            del csv_buffer


if __name__ == '__main__':
    main()