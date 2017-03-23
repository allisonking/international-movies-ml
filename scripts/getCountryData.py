"""Script to get the country that a movie is from and add it to the CSV file"""

import sys
import requests
import csv

def main():
    """Main entry point for the script."""

    # open links.csv in order to access IMDB id numbers
    linkFile = open('../movie-lens-data/links.csv', "rb")
    linkReader = csv.reader(linkFile)

    # open movies.csv so we can find the data to append to
    movieFile = open('../movie-lens-data/movies.csv', "rb")
    movieReader = csv.reader(movieFile)
    
    # writer for csv with countries
    movie_countries_ofile = open('movie-countries.csv', "wb")
    writer = csv.writer(movie_countries_ofile)

    # writer for text file with every country we have movies from
    all_countries_ofile = open('all_countries.txt', "wb")
    
    # deal with headers
    link_header = linkReader.next() # skip first line
    country_header = movieReader.next()
    country_header.append("country")
    writer.writerow(country_header)

    # iterate through data
    all_countries = set()
    for row in linkReader:
        # get the imdb url for the omdb api
        url = get_omdb_url(row[1])

        # get the list of countries associated with the movie
        countries = get_array_of_countries(url)

        # add to set of countries
        for country in countries.split("|"):
            all_countries.add(country)
        
        # get the movie row
        movie_row = movieReader.next()

        # append the countries to it
        movie_row.append(countries)
        print movie_row # this is mostly here so we can see the program is still running

        # write to the file
        writer.writerow(movie_row)

    for country in all_countries:
        all_countries_ofile.write(country +"\n")

    linkFile.close()
    movieFile.close()
    movie_countries_ofile.close()
    all_countries_ofile.close()

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
