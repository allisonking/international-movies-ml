"""Recommender system based on user-index memory based collaborative filtering"""

import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import mean_squared_error
from math import sqrt


def main():
    """Main entry point. This is largely based on the Cambridge Coding tutorial"""
    # path to ratings.csv
    ratings_csv = "../movie-lens-data/ratings.csv"
    ratings_data = pd.read_csv(ratings_csv, encoding='latin-1')

    # get number of users and number of movies
    n_users = ratings_data.userId.unique().shape[0]
    n_movies = ratings_data.movieId.unique().shape[0]

    movie_map = get_index_movie_map(ratings_data)

    # get our training and test data
    train_data, test_data = get_training_data(ratings_data)

    # create a matrix for user-item (users who are similar to you also like...)
    train_data_matrix = get_user_item_matrix(n_users, n_movies, train_data, movie_map)
    test_data_matrix = get_user_item_matrix(n_users, n_movies, test_data, movie_map)

    # calculate the cosine similarity
    user_similarity = pairwise_distances(train_data_matrix, metric='cosine')
    item_similarity = pairwise_distances(train_data_matrix.T, metric='cosine')

    item_prediction = predict(train_data_matrix, item_similarity, type='item')
    user_prediction = predict(train_data_matrix, user_similarity, type='user')

    print 'User-based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix))
    print 'Item-based CF RMSE: ' + str(rmse(item_prediction, test_data_matrix))


def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))


def predict(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        prediction = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(
            similarity).sum(axis=1)]).T

    elif type == 'item':
        prediction = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])

    return prediction


def get_index_movie_map(data):
    movie_map = {}
    no_duplicates = data.movieId.unique()
    index = 0
    for movieId in no_duplicates:
        movie_map[movieId] = index
        index = index + 1

    return movie_map


def get_user_item_matrix(n_users, n_items, data, movie_map):
    """Returns the user item matrix for a given set of data"""
    matrix = np.zeros((n_users, n_items))
    for line in data.itertuples():
        matrix[line[1]-1, movie_map[line[2]]] = line[3]

    return matrix


def get_training_data(ratings_data):
    """Returns the training data set as a data frame"""
    print "total number of ratings: %d" % ratings_data.shape[0]

    # split into test and training data using sklearn
    train, test = train_test_split(ratings_data, test_size=0.2)
    print "number of ratings in training set: %d" % train.shape[0]
    print "number of ratings in test set: %d" % test.shape[0]

    return train, test

if __name__ == '__main__':
    sys.exit(main())