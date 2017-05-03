import numpy as np
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_multilabel_classification

from sys import exit

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

print "Vocab list: ", vocabs["tags"]
print "Num classes: ", len(vocabs["tags"].keys())

clf = OneVsRestClassifier(SVC())

X_titles = vectors["title"]
X_posts = vectors["body"]
Y = vectors["tags"]

total_num = 1800
X_titles = X_titles[:total_num]
X_posts = X_posts[:total_num]
Y = Y[:total_num]

print "Y: ", Y
print Y.shape
print X_posts.shape

print Y[0]
print Y[4]

num_inputs = Y.shape[0]
num_classes = Y.shape[1]

p_train = 0.80
num_train = int(num_inputs * p_train)

X = X_posts

X_train = X[0:num_train]
X_test = X[num_train:]

Y_train = Y[0:num_train]
Y_test = Y[num_train:]


# freqs = Y_train.mean(axis=0)
# print "Frequencies: ", freqs
# print "total: ", freqs.sum()

# for y in Y:
    # print vecToTag(y, vocabs["tags"])

print "Training classifier"
clf.fit(X_train, Y_train)
print "Done training"

# test_X_titles = X_titles[0,:]
# test_X_titles = test_X_titles.reshape((1,-1))
# print test_X_titles.shape

# pred = clf.predict(test_X_titles)
# print vecToTag(pred, vocabs["tags"])

print "Predicting"
preds = clf.predict(X_test)
# print preds[:3]
# print Y[:3]

print "pred: ", preds
print "True y: ", Y_test

acc = accuracy_score(Y_test, preds)
print "Accuracy (from titles): ", acc

print "X_test shape: ", X_test.shape
dec_func = clf.decision_function(X_test)
print dec_func.shape

# Remove zeros for classes that didn't exist in training data
dec_func[dec_func == 0] = float("-inf")

pred_indices = np.argmax(dec_func, axis=1)

pred_classes = np.array([np.array([int(i == pred_i) for i in range(num_classes)]) for pred_i in pred_indices])
print pred_classes.shape

acc = accuracy_score(Y_test, pred_classes)
print "Accuracy (from posts): ", acc

exit()

print "Training classifier"
clf.fit(X_posts, Y)
print "Done training"

print X_posts[:3]

print "Predicting"
preds = clf.predict(X_posts)
acc = accuracy_score(Y, preds)
print "Accuracy (from posts): ", acc


# for p in preds:
    # print vecToTag(p, vocabs["tags"])




