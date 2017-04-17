"""Recommender system based solely on popularity"""

import sys
import pandas as pd
from sklearn.model_selection import train_test_split


def main():
    """Main entry point"""
    # declare country we are interested in
    country = "China"

    # path to files we will read in
    ratings_csv = "../movie-lens-data/ratings.csv"
    movies_csv = "../scripts/output/movie-countries.csv"

    # get training data from ratings.csv as a data frame
    train_data = get_training_data(ratings_csv)

    # get movie-country data as a data frame
    movies = pd.read_csv(movies_csv, encoding='utf-8', keep_default_na=False)

    # merge them
    train_data_country = pd.merge(train_data, movies, on='movieId')

    # filter for country
    country_filter = train_data_country[train_data_country.apply(lambda x: country in x['country'], axis=1)]
    print "total number of movies associated with %s: %d" %(country, country_filter.shape[0])

    # get a list of the most popular movies
    list_of_movies = get_ranking_of_movies(country_filter)

    # print the five most popular movies
    print "=== Highest rated movies from %s ===" %(country)
    print list_of_movies.head(n=5)


def get_training_data(ratings_path):
    """Returns the training data set as a data frame"""
    # read in ratings
    ratings = pd.read_csv(ratings_path, encoding='latin-1')
    print "total number of ratings: %d" % ratings.shape[0]

    # split into test and training data using sklearn
    train, test = train_test_split(ratings, test_size=0.2)
    print "number of ratings in training set: %d" % train.shape[0]
    print "number of ratings in test set: %d" % test.shape[0]

    return train


def get_ranking_of_movies(data):
    """Returns a data frame of sorted movies by rating average"""
    stats = data.groupby(by='title')['rating'].mean().sort_values(ascending=False)
    return stats


if __name__ == '__main__':
    sys.exit(main())