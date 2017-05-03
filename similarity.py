import numpy as np

from scraper import *

class_to_test = "122_s17"
input_file = class_to_test + "_posts.csv"

(vocabs, dicts, vectors, originals) = read_vectorized_data(input_file)


tags_vector = vectors["tags"]
body_vector = vectors["body"]

body_original = originals["body"]

limit = 1800
tags_vector = tags_vector[:limit]
body_vector = body_vector[:limit]

body_dict = dicts["body"]


print body_vector.shape

bv = body_vector[0]
print bv.shape
# print body_vector[0, 1080:1090]
# print body_vector[0, body_vocab["exams"]]

print bv
nonzeros = np.where(bv > 0) 
nonzeros = nonzeros[0]
print nonzeros

print nonzeros[0]
print "Word: ", body_dict[nonzeros[0]]

n_samples, n_features = body_vector.shape

dists = np.zeros((n_samples, n_samples))

print "Computing euclidean distance matrix"
for i in range(n_samples):
    for j in range(n_samples):
        a = body_vector[i]
        b = body_vector[j]
        dists[i,j] = np.sqrt(np.sum((a-b)**2))

print dists.shape
# print dists

close = np.logical_and(dists >= 0, dists < 0.5)

# Ignore everything below and including the diagonal
# since the matrix is symmetric
for i in range(n_samples):
    for j in range(i+1):
        close[i,j] = False

close_inds = np.where(close)

# close = close[0]
close_inds = np.asarray(close_inds)
close_inds = close_inds.T


for (c1, c2) in close_inds:
    break
    print "\n\n"

    close1 = body_original[c1]
    close2 = body_original[c2]

    print "Dist: ", dists[c1, c2]
    print close1, "\n"
    print close2


# print "----"
# print body_original[2], "\n-", body_original[4]



## Cosine similarity
print "\n\n"
print "Performing cosine similarity analysis"

norms = np.sqrt(np.sum(body_vector * body_vector, axis=1, keepdims=True))
body_vector_normed = body_vector / norms
similarities = np.dot(body_vector_normed, body_vector_normed.T)
similarities = np.round(similarities, 2)
cos_dists = 1 - similarities
# print cos_dists

cos_close = np.logical_and(cos_dists >= 0, cos_dists < 0.15)

# Ignore everything below and including the diagonal
# since the matrix is symmetric
for i in range(n_samples):
    for j in range(i+1):
        cos_close[i,j] = False

close_inds = np.where(cos_close)

close_inds = np.asarray(close_inds)
close_inds = close_inds.T
# print close_inds


for (c1, c2) in close_inds:
    print "\n\n"

    close1 = body_original[c1]
    close2 = body_original[c2]

    print "cos dist: ", cos_dists[c1, c2]
    print close1, "\n"
    print close2


