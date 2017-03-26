"""Script to get the country that a movie is from and add it to the CSV file"""

import sys
import requests
import csv
import time


def main():
    """Main entry point for the script."""

    # open links.csv in order to access IMDB id numbers
    link_file = open('../movie-lens-data-20m/links.csv', "rb")
    link_reader = csv.reader(link_file)

    # open movies.csv so we can find the data to append to
    movie_file = open('../movie-lens-data-20m/movies.csv', "rb")
    movie_reader = csv.reader(movie_file)
    
    # writer for csv with countries
    movie_countries_ofile = open('output/movie-countries-20m.csv', "wb")
    writer = csv.writer(movie_countries_ofile)
    
    # deal with headers
    link_reader.next() # skip first line
    country_header = movie_reader.next()
    country_header.append("country")
    writer.writerow(country_header)

    # iterate through data
    for row in link_reader:
        # get the imdb url for the omdb api
        url = get_omdb_url(row[1])

        # get the list of countries associated with the movie
        countries = get_array_of_countries(url)
        
        # get the movie row
        movie_row = movie_reader.next()

        # append the countries to it
        movie_row.append(countries)
        print movie_row # this is mostly here so we can see the program is still running

        # write to the file
        writer.writerow(movie_row)

    link_file.close()
    movie_file.close()
    movie_countries_ofile.close()


def get_omdb_url(imdbId):
    """Returns the OMDb http string request for the movie with this imdbId"""
    omdb_url = 'http://www.omdbapi.com/?'
    id_search_string='i=tt'
    return omdb_url+id_search_string+imdbId


def get_array_of_countries(url):
    """Returns a list of countries associated with a given movie"""
    try:
        response = requests.get(url)

    except requests.exceptions.ConnectionError:
        print("Connection refused by server... sleeping then trying again")
        time.sleep(5)
        print("Trying again...")
        response = requests.get(url)

    try:
        countries = response.json()['Country']
    except ValueError:
        print("JSON could not be parsed...")
        return "JSONERROR"
    return countries.encode('utf-8').replace(', ', '|')

if __name__ == '__main__':
    sys.exit(main())
