from read_data import *
from sklearn.naive_bayes import GaussianNB
import numpy as np
import matplotlib.pyplot as plt

# Calculates the accuracy of prediction using a Gaussian Naive Bayes Model by training
# on <X_train, y_train> and testing on <X_test, y_test>.
# Returns the accuracy as a decimal between 0 and 1.
def get_accuracy(X_train, y_train, X_test, y_test):
	gnb = GaussianNB()
	gnb.fit(X_train, y_train)
	y_pred = gnb.predict(X_test)
	errors = 0
	for i in range(len(y_pred)):
		if(y_pred[i] != y_test[i]):
			errors += 1
	error_percent = float(errors) / float(len(y_pred))
	accuracy = 1.0 - error_percent
	return accuracy

# Training and Testing on the same data.
# Calculates the accuracy for each tag individually and then returns the average accuracy.
# Input Parameter Specifications:
# class_to_test   : '122_f15', '122_f16', '122_s17', '381', '601'
# train_percdent  : [0, 1]
# vectorizer_name : 'bag', 'tfidf'
# X_label         : 'title', 'body'
# y_label		  : 'tags', 'visibility'
def same_train_test(class_to_test, train_percent, vectorizer_name, X_label, y_label):
	(vocabs, dicts, vectors, orignals) = read_vectorized_data(class_to_test + "_posts.csv", vectorizer_name)
	num_tags = len(vectors[y_label][0])
	avg_accuracy = 0.0
	for i in range(num_tags):
		y = vectors[y_label]
		y = y[:,i]
		num = int(len(vectors[X_label]) * train_percent)
		y_train = y[:num]
		y_test = y[num:]
		X = vectors[X_label]
		X_train = X[:num]
		X_test = X[num:]
		accuracy = get_accuracy(X_train, y_train, X_test, y_test)
		avg_accuracy += accuracy

	avg_accuracy = avg_accuracy / float(num_tags)
	return avg_accuracy

# Training and Testing on different data
# Input Parameter Specifications:
# class_to_train / class_to_test : '122_f15', '122_f16', '122_s17', '381', '601'
# vectorizer_name                : 'bag', 'tfidf'
# X_label                        : 'title', 'body'
# y_label						 : 'tags', 'visibility'
def diff_train_test(class_to_train, class_to_test, vectorizer_name, X_label, y_label):
	(voc_train, dict_train, vec_train, orig_train) = read_vectorized_data(class_to_train + "_posts.csv", vectorizer_name)
	(voc_test, dict_test, vec_test, orig_test) = read_vectorized_data(class_to_test + "_posts.csv", vectorizer_name)
	train_tags = dict_train[y_label]
	test_tags = dict_test[y_label]
	train_vocab = dict_train[X_label]
	test_vocab = dict_test[X_label]
	common_tags = list(set(train_tags) & set(test_tags))
	common_vocab = list(set(train_vocab) & set(test_vocab))
	vocab_indices_train = []
	vocab_indices_test = []
	for i in range(len(common_vocab)):
		vocab_indices_train.append(train_vocab.index(common_vocab[i]))
		vocab_indices_test.append(test_vocab.index(common_vocab[i]))

	avg_accuracy = 0.0
	for i in range(len(common_tags)):
		train_idx = train_tags.index(common_tags[i])
		test_idx = test_tags.index(common_tags[i])
		X_train = vec_train[X_label][:, vocab_indices_train]
		y_train = vec_train[y_label][:, train_idx]
		X_test = vec_test[X_label][:, vocab_indices_test]
		y_test = vec_test[y_label][:, test_idx]
		accuracy = get_accuracy(X_train, y_train, X_test, y_test)
		avg_accuracy += accuracy

	avg_accuracy = avg_accuracy / float(len(common_tags))
	return avg_accuracy



#Experimental Tests:

# Helper Function for experimental Tests:

def plot_graph(X, Y, x_label='', y_label=''):
	plt.plot(X, Y)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.show()

print('1. ' + str(diff_train_test('122_f16', '122_f15', 'bag', 'body', 'tags')))
print('2. ' + str(diff_train_test('122_f16', '122_f15', 'tfidf', 'body', 'tags')))
print('3. ' + str(diff_train_test('122_f16', '122_f15', 'bag', 'body', 'visibility')))
print('4. ' + str(diff_train_test('122_f16', '122_f15', 'tfidf', 'body', 'visibility')))
print('5. ' + str(diff_train_test('122_f16', '122_f15', 'bag', 'title', 'tags')))
print('6. ' + str(diff_train_test('122_f16', '122_f15', 'tfidf', 'title', 'tags')))
print('7. ' + str(diff_train_test('122_f16', '122_f15', 'bag', 'title', 'visibility')))
print('8. ' + str(diff_train_test('122_f16', '122_f15', 'tfidf', 'title', 'visibility')))

print('9. ' + str(diff_train_test('122_f16', '122_s17', 'bag', 'body', 'tags')))
print('10. ' + str(diff_train_test('122_f16', '122_s17', 'tfidf', 'body', 'tags')))
print('11. ' + str(diff_train_test('122_f16', '122_s17', 'bag', 'body', 'visibility')))
print('12. ' + str(diff_train_test('122_f16', '122_s17', 'tfidf', 'body', 'visibility')))
print('13. ' + str(diff_train_test('122_f16', '122_s17', 'bag', 'title', 'tags')))
print('14. ' + str(diff_train_test('122_f16', '122_s17', 'tfidf', 'title', 'tags')))
print('15. ' + str(diff_train_test('122_f16', '122_s17', 'bag', 'title', 'visibility')))
print('16. ' + str(diff_train_test('122_f16', '122_s17', 'tfidf', 'title', 'visibility')))

print('17. ' + str(same_train_test('122_f15', 0.85, 'bag', 'body', 'tags')))
print('18. ' + str(same_train_test('122_f16', 0.85, 'bag', 'body', 'tags')))
print('19. ' + str(same_train_test('381', 0.85, 'bag', 'body', 'tags')))
print('20. ' + str(same_train_test('601', 0.85, 'bag', 'body', 'tags')))

print('21. ' + str(same_train_test('122_f15', 0.85, 'tfidf', 'body', 'tags')))
print('22. ' + str(same_train_test('122_f16', 0.85, 'tfidf', 'body', 'tags')))
print('23. ' + str(same_train_test('381', 0.85, 'tfidf', 'body', 'tags')))
print('24. ' + str(same_train_test('601', 0.85, 'tfidf', 'body', 'tags')))

acc = []
tr_percent = []
num_data_points = 20
incr = 0.85 / float(num_data_points)
curr_percent = incr
for i in range(num_data_points):
	tr_percent.append(curr_percent)
	acc.append(same_train_test('122_f15', curr_percent, 'bag', 'body', 'tags'))
	curr_percent += incr
print('got data')
plot_graph(tr_percent, acc, 'Train Percent', 'Accuracy')

