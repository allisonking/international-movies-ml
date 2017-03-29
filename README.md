
# international-movies-ml
Machine learning to recommend movies from around the world!

Finds the user's preference in movies and returns to them a movie they would like from another country.

## scripts
Folder for some helper scripts in order to gather initial data.

### getCountryData.py
This script uses the [requests](http://docs.python-requests.org/en/master/ "requests homepage") library to issue http requests to the OMDb API in order to find out further information about a given movie. The script runs through a list of movies (for example, MovieLens's links.csv), finds the IMDB ID, then looks up the movie through OMDb. From there, it finds the country associated with the movie and creates a new CSV that appends country data to the already existing movie data. 

When running on a very large dataset (i.e. Movielens's 20 million ratings set), the http requests can often return a connection error due to too many requests. When the script gets a connection error, it sleeps for five seconds, then tries again. So far, this has always worked to successfully complete the http request. Sometimes, the returned JSON will be malformed, though it is not consistently on the same http request that this happens. If there is an error, then the script will fill in 'JSONERROR' under the country name and the user should go back and manually fill in the country. In the 100k dataset, this problem did not come up at all, however in the 20m dataset, it occurred 4 times. 

### getCountryStats.py
This script creates a csv with three columns- country, number of movies, and number of primary movies. The country is the country associated with a movie, the number of movies is how many movies in the dataset are associated with the country, and the number of primary movies is how many movies list that country as its first country. This script takes in the output of `getCountryData.py`

### getCountryStatsPandas.py
This script was an early attempt at learning to use [pandas](http://pandas.pydata.org/ "pandas homepage") to read and write CSV files, as well as to manipulate the data. Its output is the same as getCountryStats.py, though it also outputs a plot of how many times a country is associated with a movie in the dataset. The output plot should look like: ![movie country plot](figures/movie_country_data.png "movie country plot")

## recommenders

### popularityRecommender.py
A simple popularity recommender using [GraphLab](https://turi.com/ "graphlab homepage"), mostly based on [this tutorial](https://www.analyticsvidhya.com/blog/2016/06/quick-guide-build-recommendation-engine-python/ "tutorial"). This will always recommend the same movies for every user since there is no personalitzation- it is just recommending the most popular movies. This script uses 80% of the ratings.csv data and filters out the country the user is interested in. The script then recommends the top five movies from that country based on popularity.