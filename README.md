# Community
A repository for gathering comments across major social platforms and storing them in AWS for analysis.

## ETL

### Reddit lambda function
The lambda function writes the articles and comments to json files in the s3 bucket. The next script converts those logs to csv files. The csv files are then inserted into Redshift.

### Redshift


## Other considerations

### Large amounts of new data

### Running regularly

### Team member access