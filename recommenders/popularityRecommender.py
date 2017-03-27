"""Recommender system based solely on popularity"""

import sys
import pandas as pd
import graphlab
import graphlab.aggregate as agg
from sklearn.model_selection import train_test_split


def main():
    """This is based on https://www.analyticsvidhya.com/blog/2016/06/quick-guide-build-recommendation-engine-python/"""
    # declare country we are interested in
    country = "China"

    # path to files we will read in
    ratings_csv = "../movie-lens-data/ratings.csv"
    movies_csv = "../scripts/output/movie-countries.csv"

    # get training data from ratings.csv as an sframe
    train_data = get_training_data_sframe(ratings_csv)

    # get movie-country data as an sframe
    movies = load_sframe(movies_csv)

    # merge them
    train_data_country = train_data.join(movies, on='movieId')

    # filter for country
    country_filter = train_data_country[train_data_country.apply(lambda x: country in x['country'])]

    # create the popularity model
    popularity_model = graphlab.popularity_recommender.create(country_filter,
                                                              user_id='userId', item_id='movieId',
                                                              target='rating')

    # get a list of top five recommended movies for user#1
    # because this is a popularity model, it will be the same for every user
    popularity_recommendations = popularity_model.recommend(users=range(1, 2), k=5).join(movies, on='movieId')
    popularity_recommendations.print_rows(num_rows=5)

    print_rating_stats(train_data_country)


def load_sframe(path):
    return graphlab.SFrame(pd.read_csv(path, encoding='utf-8', keep_default_na=False))


def get_training_data_sframe(ratings_path):
    # read in ratings
    ratings = pd.read_csv(ratings_path, encoding='latin-1')
    print "total number of ratings: %d" % ratings.shape[0]

    # split into test and training data using sklearn
    train, test = train_test_split(ratings, test_size=0.2)
    print "number of ratings in training set: %d" % train.shape[0]
    print "number of ratings in test set: %d" % test.shape[0]

    # transform pandas dframe into graphlab sframe
    train_data = graphlab.SFrame(train)

    return train_data


def print_rating_stats(data):
    # this is just to see what the training data mean rating is to see if the popularity recommender is working
    stats = data.groupby(key_columns='movieId',
                         operations={
                                   'mean_rating': agg.MEAN('rating'),
                                   'std_rating': agg.STD('rating')
                               })

    # sort by mean rating, only show the ones with 5.0 ratings, merge with movie name/country data
    print stats.sort(sort_columns='mean_rating', ascending=False).filter_by([5.0], 'mean_rating')

if __name__ == '__main__':
    sys.exit(main())