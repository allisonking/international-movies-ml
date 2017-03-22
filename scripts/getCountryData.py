"""Script to get the country that a movie is from and add it to the CSV file"""

import sys
import requests
import csv

def main():
    """Main entry point for the script."""

    # open links.csv in order to access IMDB id numbers
    # movieId, imdbId, tmbdId
    linkFile = open('../movie-lens-data/links.csv', "rb")
    linkReader = csv.reader(linkFile)

    # open movies.csv so we can append to it
    movieFile = open('../movie-lens-data/movies.csv', "rb")
    movieReader = csv.reader(movieFile)
    
    # writer
    ofile = open('movie-countries.csv', "wb")
    writer = csv.writer(ofile)
    
    # deal with headers
    link_header = linkReader.next() # skip first line
    country_header = movieReader.next()
    country_header.append("country")
    writer.writerow(country_header)

    # iterate through data
    index = 0
    for row in linkReader:
        if (index > 10):
            break
        
        # get the imdb url for the omdb api
        url = get_omdb_url(row[1])

        # get the list of countries associated with the movie
        countries = get_array_of_countries(url)
        
        # get the movie row
        movie_row = movieReader.next()
        print movie_row
        # append the countries to it
        movie_row.append(countries)

        # write to the file
        writer.writerow(movie_row)

        index = index + 1

    linkFile.close()
    movieFile.close()
    ofile.close()

def get_omdb_url(imdbId):
    omdb_url = 'http://www.omdbapi.com/?'
    id_search_string='i=tt'
    return omdb_url+id_search_string+imdbId

def get_array_of_countries(url):
    """Returns a list of countries associated with a given movie"""
    response = requests.get(url)
    countries = response.json()['Country']
    countries_string = str(countries)
    return str(countries).replace(', ', '|')

if __name__ == '__main__':
    sys.exit(main());
