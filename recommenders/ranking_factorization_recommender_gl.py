"""Recommender system based on user-index memory based collaborative filtering"""

import sys
import graphlab as gl


def main():
    country_name = "India"

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

    print "==== Precision Recall ===="
    print model.evaluate_precision_recall(validation_data)

    print "==== RMSE ===="
    print model.evaluate_rmse(validation_data, target='rating')['rmse_overall']


if __name__ == '__main__':
    sys.exit(main())