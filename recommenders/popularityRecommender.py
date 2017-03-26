"""Recommender system based solely on popularity"""

import sys
import pandas as pd
import graphlab
import graphlab.aggregate as agg
from sklearn.model_selection import train_test_split


def main():
    """This is based on https://www.analyticsvidhya.com/blog/2016/06/quick-guide-build-recommendation-engine-python/"""

    # path to files we will read in
    ratings_csv = "../movie-lens-data/ratings.csv"
    movies_csv = "../scripts/output/movie-countries.csv"

    # read in ratings
    ratings = pd.read_csv(ratings_csv, encoding='latin-1')
    print "total number of ratings: %d" % ratings.shape[0]

    # split into test and training data using sklearn
    train, test = train_test_split(ratings, test_size=0.2)
    print "number of ratings in training set: %d" % train.shape[0]
    print "number of ratings in test set: %d" % test.shape[0]

    # transform pandas dframe into graphlab sframe
    train_data = graphlab.SFrame(train)
    movies = graphlab.SFrame(pd.read_csv(movies_csv, encoding='utf-8', keep_default_na=False))

    # create the popularity model
    popularity_model = graphlab.popularity_recommender.create(train_data,
                                                              user_id='userId', item_id='movieId',
                                                              target='rating')

    # get a list of top five recommended movies for user#1
    # because this is a popularity model, it will be the same for every user
    popularity_recommendations = popularity_model.recommend(users=range(1, 2), k=5)

    # join with movie-countries data so we can see the names of movies and country they are from
    result = popularity_recommendations.join(movies, on='movieId')
    result.print_rows()

    # this is just to see what the training data mean rating is to see if the popularity recommender is working
    stats = train_data.groupby(key_columns='movieId',
                               operations={
                                   'mean_rating': agg.MEAN('rating'),
                                   'std_rating': agg.STD('rating')
                               })

    # sort by mean rating, only show the ones with 5.0 ratings, merge with movie name/country data
    print stats.sort(sort_columns='mean_rating', ascending=False).filter_by([5.0], 'mean_rating')\
        .join(movies, on='movieId')

if __name__ == '__main__':
    sys.exit(main())