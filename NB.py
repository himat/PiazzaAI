from read_data import *
from sklearn.naive_bayes import GaussianNB
import numpy as np

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
def same_train_test(class_to_test, train_percent):
	#class_to_test = '122_s17'
	(vocabs, dicts, vectors, orignals) = read_vectorized_data(class_to_test + "_posts.csv")
	#train_percent = 0.85
	num_tags = len(vectors['tags'][0])
	avg_accuracy = 0.0
	for i in range(num_tags):
		y = vectors['tags']
		y = y[:,i]
		num = int(len(vectors['body']) * train_percent)
		y_train = y[:num]
		y_test = y[num:]
		X = vectors['body']
		X_train = X[:num]
		X_test = X[num:]
		accuracy = get_accuracy(X_train, y_train, X_test, y_test)
		avg_accuracy += accuracy

	avg_accuracy = avg_accuracy / float(num_tags)
	return avg_accuracy

#Training and Testing on different data
def diff_train_test(class_to_train, class_to_test):
	(voc_train, dict_train, vec_train, orig_train) = read_vectorized_data(class_to_train + "_posts.csv")
	(voc_test, dict_test, vec_test, orig_test) = read_vectorized_data(class_to_test + "_posts.csv")
	train_tags = dict_train['tags']
	test_tags = dict_test['tags']
	train_vocab = dict_train['body']
	test_vocab = dict_test['body']
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
		X_train = vec_train['body'][:, vocab_indices_train]
		y_train = vec_train['tags'][:, train_idx]
		X_test = vec_test['body'][:, vocab_indices_test]
		y_test = vec_test['tags'][:, test_idx]
		accuracy = get_accuracy(X_train, y_train, X_test, y_test)
		avg_accuracy += accuracy
		#print('tag: ' + common_tags[i] + ' accuracy: ' + str(accuracy))

	avg_accuracy = avg_accuracy / float(len(common_tags))
	return avg_accuracy	

#print(diff_train_test('122_f15', '122_f16'))
print(same_train_test('601', 0.85))


