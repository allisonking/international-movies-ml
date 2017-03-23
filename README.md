# international-movies-ml
Machine learning to recommend movies from around the world!

Finds the user's preference in movies and returns to them a movie they would like from another country.

### scripts/getCountryData.py
This script uses the `requests` library to issue http requests to the OMDb API in order to find out further information about a given movie. The script runs through a list of movies (for example, MovieLens's links.csv), finds the IMDB ID, then looks up the movie through OMDb. From there, it finds the country associated with the movie and creates a new CSV that appends country data to the already existing movie data. 
