import numpy as np
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score

from scraper import *

class_to_test = "122"
input_file = class_to_test + "_posts.csv"

def vecToTag(test_y, vocab):
    one_ind = np.where(test_y == 1)
    one_ind = one_ind[0][0]
    print one_ind

    for key, value in vocab.items():
        if value == one_ind:
            tag = key
    return tag

(vocabs, vectors) = read_vectorized_data(input_file)

print vocabs["tags"]

clf = OneVsRestClassifier(SVC())

X_titles = vectors["title"]
Y = vectors["tags"]

for y in Y:
    print vecToTag(y, vocabs["tags"])

print X_titles.shape
print Y.shape
clf.fit(X_titles, Y)

print X_titles.shape
test_X_titles = X_titles[0,:]
test_X_titles = test_X_titles.reshape((1,-1))
print test_X_titles.shape

print test_X_titles
pred = clf.predict(test_X_titles)
print vecToTag(pred, vocabs["tags"])

preds = clf.predict(X_titles)
print preds[:3]
print Y[:3]

acc = accuracy_score(Y, preds)
print "Accuracy (from titles): ", acc


X_posts = vectors["body"]

clf.fit(X_posts, Y)

print X_posts[:3]

preds = clf.predict(X_posts)
acc = accuracy_score(Y, preds)
print "Accuracy (from posts): ", acc

print preds

# for p in preds:
    # print vecToTag(p, vocabs["tags"])




