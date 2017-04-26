import numpy as np
from sklearn.naive_bayes import GaussianNB

from scraper import *

class_to_test = "122"
input_file = class_to_test + "_posts.csv"

data = read_vectorized_data(input_file)

print data["title"]



