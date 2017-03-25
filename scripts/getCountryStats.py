"""Script to get the number of movies per country"""

import sys
import csv


def main():
    """Main entry point for the script."""

    # open links.csv in order to access IMDB id numbers
    ifile = open('movie-countries.csv', "rb")
    reader = csv.reader(ifile)
    
    # writer for csv with countries
    ofile = open('country_stats.csv', "wb")
    writer = csv.writer(ofile)

    # deal with headers
    reader.next() # skip first line
    writer.writerow(['country', 'number of movies', 'number of primary movies'])

    # one dictionary for all mention of a country, one dictionary for if the country was the first one listed
    country_count_dict = {}
    country_count_primary_dict= {}

    # iterate through data
    for row in reader:
        # get the countries column
        countries = row[3]

        # add to dicionary of countries
        for country in countries.split("|"):
            country_count_dict[country] = country_count_dict.get(country, 0) + 1

            # if it's the primary country
            if country == countries.split("|")[0]:
                country_count_primary_dict[country] = country_count_primary_dict.get(country, 0) + 1

    # write to the file
    for key, value in country_count_dict.iteritems():
        writer.writerow([key , str(value), country_count_primary_dict.get(key, "0")])

    ifile.close()
    ofile.close()

if __name__ == '__main__':
    sys.exit(main())
