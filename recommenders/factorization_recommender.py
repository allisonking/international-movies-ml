import sys
import numpy as np
import pandas as pd
from math import sqrt
import matplotlib
import matplotlib.pyplot as plt

def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    step_error = []
    Q = Q.T
    # we'll do this for # steps
    for step in xrange(steps):
        # iterate through the ratings matrix
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                # we only want to minimize the value on nonzero values
                if R[i][j] > 0:
                    # eij is the difference between the true rating and our current estimate
                    eij = R[i][j] - np.dot(P[i, :], Q[:, j])
                    # update based on the gradient- the formula is the derivative of squared error,
                    # with the beta adjustment)
                    # alpha is our learning rate
                    # beta is an additional parameter to prevent overfitting (regularization)
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        # at this point we have adjusted for gradient descent (for this step, anyway)
        eR = np.dot(P,Q)

        # now let's see how it does by summing the errors against the actual ratings
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                # it's an actual rating!
                if R[i][j] > 0:
                    # sum the error
                    e = e + pow(R[i][j] - np.dot(P[i, :], Q[:, j]), 2)
                    # regularization to avoid overfitting
                    for k in xrange(K):
                        e = e + (beta/2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))
        step_error.append([step, e])
        if e < 0.001:
            break

    df = pd.DataFrame(step_error, columns=['step', 'error'])
    axes = df.plot(x='step', y='error', kind='line', title='Error Adjustment', legend=False)
    # set the axes and set display
    axes.set_xlabel("Step")
    axes.set_ylabel("Error")
    plt.tight_layout()
    plt.show()
    return P, Q.T


def main():
    R = [
        [1, 2, 0, 3, 0],
        [4, 0, 0, 1, 2],
        [0, 3, 0, 5, 1],
        [2, 0, 4, 0, 0],
        [0, 1, 3, 4, 0],
        [0, 4, 2, 0, 5],
    ]

    R = np.array(R)

    num_users = len(R)
    num_movies = len(R[0])
    K = 2

    # P is the strength of associations between a USER and the features
    P = np.random.rand(num_users, K)
    # Q is the strength of associations between a MOVIE and the features
    Q = np.random.rand(num_movies, K)

    nP, nQ = matrix_factorization(R, P, Q, K)
    nR = np.dot(nP, nQ.T)

    print nR

if __name__ == '__main__':
    sys.exit(main())