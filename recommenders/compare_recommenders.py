"""Compare different recommender models"""

import sys
import graphlab as gl


def main():
    # get our data sets
    ratings_path = '../movie-lens-data/ratings.csv'
    train, test = get_training_test_data(ratings_path)

    # load in our competing models
    popularity_model = gl.popularity_recommender.create(train, user_id='userId', item_id='movieId', target='rating')
    item_similarity_model = gl.item_similarity_recommender.create(train, user_id='userId', item_id='movieId',
                                                                  target='rating', similarity_type='cosine')
    ranking_factorization_model = gl.ranking_factorization_recommender.create(train, user_id='userId', item_id='movieId',
                                                                              target='rating')

    print "==== Comparing Models ===="
    gl.recommender.util.compare_models(test, [popularity_model, item_similarity_model, ranking_factorization_model],
                                       metric='precision_recall')


def get_training_test_data(path):
    # read in data
    ratings_file = '../movie-lens-data/ratings.csv'
    ratings_data = gl.SFrame.read_csv(ratings_file)

    train, test = gl.recommender.util.random_split_by_user(ratings_data, 'userId', 'movieId')

    return train, test

if __name__ == '__main__':
    sys.exit(main())