
# international-movies-ml
Machine learning to recommend movies from around the world!

Finds the user's preference in movies and returns to them a movie they would like from another country.

## scripts
Folder for some helper scripts in order to gather initial data.

### getCountryData.py
This script uses the `requests` library to issue http requests to the OMDb API in order to find out further information about a given movie. The script runs through a list of movies (for example, MovieLens's links.csv), finds the IMDB ID, then looks up the movie through OMDb. From there, it finds the country associated with the movie and creates a new CSV that appends country data to the already existing movie data. 

### getCountryStats.py
This script creates a csv with three columns- country, number of movies, and number of primary movies. The country is the country associated with a movie, the number of movies is how many movies in the dataset are associated with the country, and the number of primary movies is how many movies list that country as its first country. This script takes in the output of `getCountryData.py`

### getCountryStatsPandas.py
This script was an early attempt at learning to use [pandas](https://www.google.com "pandas homepage") to read and write CSV files, as well as to manipulate the data. Its output is the same as getCountryStats.py, though it also outputs a plot of how many times a country is associated with a movie in the dataset. The output plot should look like ![movie country plot][figures/movie_country_data.png]