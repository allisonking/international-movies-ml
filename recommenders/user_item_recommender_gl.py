"""Recommender system based on user-index memory based collaborative filtering"""

import sys
import graphlab as gl


def main():
    # read in the CSV file for ratings
    ratings_csv = '../movie-lens-data/ratings.csv'
    ratings_data = gl.SFrame.read_csv(ratings_csv)

    # read in the CSV file for movie to movieIds
    movies_csv = '../scripts/output/movie-countries.csv'
    movies_data = gl.SFrame.read_csv(movies_csv)

    # split into train and test data
    training_data, validation_data = gl.recommender.util.random_split_by_user(ratings_data, 'userId', 'movieId')

    # build an item similarity model using Pearson similarity
    model = gl.item_similarity_recommender.create(training_data, user_id='userId', item_id='movieId',
                                                  target='rating', similarity_type='cosine')

    # make 5 recommendations for users 1-6
    recommendations = model.recommend(users=range(1,6), k=5).join(movies_data, on='movieId').sort(sort_columns=['userId', 'rank'],
                                                                                                  ascending=True)
    recommendations.print_rows(num_rows=25)

    print model.evaluate_rmse(validation_data, target='rating')


if __name__ == '__main__':
    sys.exit(main())