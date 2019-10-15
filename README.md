# Community
A repository for gathering comments across major social platforms and storing them in AWS for analysis.

The unit of analysis for nearly all of the data sources in this codebase is a comment. At the comment level everyone has a voice, however, this means the data is exceedingly large. Running the lambda function collecting comments from Reddit on a half-hour basis for three days yielded over 1.7M (million) comments. Data at this scale requires cloud resources.

### Use cases
Having a database of comments for various themes allows us to see what a community is thinking down at the user level and over time. One potential use-case is to provide insight into how a community is responding to a particular issue or set of issues across any give time.

### Config
You will need access to AWS, Reddit's PRAW API, and the YouTube API to get started with this repository.

## Data model and statistics
The following image shows the working data model for Reddit (Articles, Comments, and Top Comments) and Youtube (Youtube General) tables.


After running the Reddit lambda pipeline over two days and executing the YouTube command line argument for "gaming" one time.


## Data sources
The following data sources are currently being supported:
* Reddit
* YouTube (in progress)

Future work will gather data from:
* Twitch

## ETL
Data is extracted from the data sources into .json files stored on S3. Those json files are parsed, cleaned, and turned into CSVs (also stored on S3) which are copied over into the postgres db.

The lambda functions handle extracting the data into the JSON. The pipeline construced in the `etl` directory changes the log files into the CSVs. It also handles connecting and copying into Redshift.

### Reddit lambda function
The lambda function writes the articles and comments to json files in the s3 bucket. The next script converts those logs to csv files. The csv files are then inserted into Redshift.

#### Cleaning Reddit data
Reddit comment threads can be excessively messy. Hence we only allow alpha-numeric characters (and spaces) into the body field in the Redshift postgres table.

### YouTube lambda function
TBD

#### Cleaning YouTube data
TBD

## Other considerations and future work

### Large amounts of new data

### Running regularly

### Team member access