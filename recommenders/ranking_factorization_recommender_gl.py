"""Recommender system based on user-index memory based collaborative filtering"""

import sys
import graphlab as gl
from calendar import timegm
from datetime import datetime


def main():
    country_name = "USA"

    # read in the CSV file for ratings
    ratings_csv = '../movie-lens-data/ratings.csv'
    ratings_data = gl.SFrame.read_csv(ratings_csv)

    # read in the CSV file for movie to movieIds
    movies_csv = '../scripts/output/movie-countries.csv'
    movies_data = gl.SFrame.read_csv(movies_csv)
    num_movies = movies_data.shape[0]

    # split into train and test data
    training_data, validation_data = gl.recommender.util.random_split_by_user(ratings_data, 'userId', 'movieId')

    model = gl.ranking_factorization_recommender.create(training_data, user_id='userId', item_id='movieId',
                                                        target='rating')

    model.save('saved-models/ranking_factorization_model')

    recommendations = model.recommend(users=range(1, 2), k=num_movies).join(movies_data, on='movieId') \
        .sort(sort_columns=['userId', 'rank'], ascending=True)
    recommendations.print_rows(num_rows=25)

    # filter for if country is credited
    recommendations_filter_has_country = recommendations[recommendations.apply(lambda x: country_name in x['country'])]
    print recommendations_filter_has_country.print_rows(num_rows=5)

    # filter for if country is sole creator
    recommendations_filter_sole_country = recommendations.filter_by(country_name, 'country')
    print recommendations_filter_sole_country.print_rows(num_rows=5)

    print "==== Precision Recall ===="
    print model.evaluate_precision_recall(validation_data)

    print "==== RMSE ===="
    print model.evaluate_rmse(validation_data, target='rating')['rmse_overall']

    # make a recommendation to the user
    new_user_data = prepare_new_user_data('../test-data/my_movie_ratings.csv', ratings_data)
    recommendations = model.recommend([new_user_data['userId'][0]], k=num_movies, new_observation_data=new_user_data)\
        .join(movies_data, on='movieId').sort(sort_columns=['rank'], ascending=True)
    print recommendations.filter_by(country_name, 'country')


def prepare_new_user_data(csv_path, ratings_data):
    new_user_data = gl.SFrame.read_csv(csv_path)
    new_user_data.remove_column('title')
    new_user_id = ratings_data['userId'].unique().shape[0] + 1
    new_user_data.add_column(gl.SArray([new_user_id] * new_user_data.shape[0]), name='userId')
    new_user_data.add_column(gl.SArray([timegm(datetime.utcnow().utctimetuple())] * new_user_data.shape[0]), name='timestamp')
    return new_user_data


if __name__ == '__main__':
    sys.exit(main())