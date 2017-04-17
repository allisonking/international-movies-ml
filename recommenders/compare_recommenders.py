"""Compare different recommender models"""

import sys
import graphlab as gl


def main():
    # load in our competing models
    popularity_model = gl.load_model('saved-models/popularity_model')
    item_similarity_model = gl.load_model('saved-models/item_similarity_model')
    ranking_factorization_model = gl.load_model('saved-models/ranking_factorization_model')

    # get some data to test on. TODO: read in uniform training/test data in separate file
    test_data = gl.SFrame.read_csv('../movie-lens-data/ratings.csv')



if __name__ == '__main__':
    sys.exit(main())