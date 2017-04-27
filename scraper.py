from piazza_api import Piazza
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import os
import csv
import re


# First line in config should be piazza email
# Second line in config should be piazza password
config_file = "config.txt"


# Fields that are exported to be used for converting to features
TITLE_FIELDS = ["title", "body", "visibility", "tags"]

def clean_text(content):
    # TODO: Return length of code

    # print "before\n", content
    
    # Convert HTML codes into normal unicode characters
    html_parser = HTMLParser()
    content = html_parser.unescape(content)

    # Turn hidden unicode characters into their escape codes
    content = content.encode('unicode-escape')

    # Remove unicode characters
    content = re.sub('\\\u[0-9a-f]{4}', " ", content)

    # Remove \xa0 character
    content = content.replace('\\xa0', " ")

    # Remove newlines
    content = content.replace("\\n", " ")
   
    # Remove html tags
    content = (BeautifulSoup(content, "lxml")).get_text()

    # Remove any characters other than letters and '
    content = re.sub("[^a-zA-Z']", " ", content)

    # Convert to lowercase
    content = content.lower()

    content = " ".join(content.split())

    # print "\n\nafter\n", content

    return content

# Returns a list of the extracted fields from a post for exporting
# Input: post_resp is a response from the piazza api
# Output: dictionary of feature names with associated data
def get_relevant_fields(post_resp):
    children = post_resp["children"]
    history = post_resp["history"]
    question = history[0] # Get most recent question text

    data = {}
    
    # Question title
    title = question["subject"]
    data["title"] = clean_text(title)

    # Question text
    content = question["content"]
    data["body"] = clean_text(content)

    # Question tags
    tags = post_resp["folders"]
    data["tags"] = "|".join(tags)

    # Public/private
    visibility = post_resp["status"]
    if visibility == "active":
        visibility = "public"
    if visibility != "public" and visibility != "private":
        print visibility
        raise ValueError("Strange visibility")
    data["visibility"] = visibility


    # Makes sure that fields are synced in this function and globally
    assert(set(TITLE_FIELDS) == set(data.keys()))

    # ID of post (Only for debugging purposes)
    data["cid"] = post_resp["nr"]

    # If any field is blank, we can't use this post
    for key in data:
        if data[key] == "":
            return None

    return data

# Downloads and writes all post data
# Data saved to export_file
# piazza_class is a string of which class you want to download
def get_all_online_data(piazza_class):

    # Appends this string to the class name when storing the data
    export_file_suffix = "_posts.csv"

    # Read credentials
    with open(config_file) as f:
        content = f.readlines()
    creds = [x.strip() for x in content]
    username = creds[0]
    password = creds[1]

    p = Piazza()
    p.user_login(username,password)

    class_122 = p.network("ix087c2ns5p656")
    class_381 = p.network("ixz5scp9zqi583")

    ### Change this to download a different class's data
    class_to_download = None
    if piazza_class == "122":
        class_to_download = class_122
    elif piazza_class == "381":
        class_to_download = class_381
    else:
        raise ValueError("Invalid class name")
    export_file = piazza_class + export_file_suffix
    ###


    # Calling with no argument gets all posts
    all_responses = class_to_download.iter_all_posts(20)
    # all_responses = [class_to_download.get_post(2806)]
    print "Finished getting all posts"
    
    out_file = open(export_file, "wb")
    csv_writer = csv.writer(out_file)

    # Write column headers of feature names
    csv_writer.writerow(TITLE_FIELDS)
    
    count = 0

    for response in all_responses:

        # for r in response:
            # print r, response[r]
        
        fields_dict = get_relevant_fields(response)

        # print fields_dict
        
        if fields_dict == None:
            continue

        
        values = [fields_dict[k] for k in TITLE_FIELDS]
        
        line = ','.join(values)

        try:
            csv_writer.writerow(values)
        except Exception as e:
            print "Failed on id=", fields_dict["cid"]
            print(e)
            exit(1)

        if count % 200 == 0:
            print count
        count+=1

    

    out_file.close()

# Reads in the input_csv file and generates the bag of words representation and saves that to multiple files
def write_vectorized_data(input_csv):

    data = pd.read_csv(input_csv, header=0)
    file_title = input_csv.split(".")[0]

    title_vector_file = file_title + "_title_vector.csv"
    body_vector_file = file_title + "_body_vector.csv"

    vectorizer = CountVectorizer(analyzer = 'word', stop_words = 'english')
    title_vector = (vectorizer.fit_transform(data['title'])).toarray()
    body_vector = (vectorizer.fit_transform(data['body'])).toarray()

    t_out_file = open(title_vector_file, 'wb')
    np.savetxt(t_out_file, title_vector, delimiter=",", fmt="%02d")

    b_out_file = open(body_vector_file, 'wb')
    np.savetxt(b_out_file, body_vector, delimiter=",", fmt="%02d")

    # TODO add tags and visibility fields

# Reads in the multiple bag of words vectorized data files and returns as a single dictionary
def read_vectorized_data(orig_file_name):
    data = {}
    print "Reading vectorized data from file"

    file_title = orig_file_name.split(".")[0]

    title_vector_file = file_title + "_title_vector.csv"
    body_vector_file = file_title + "_body_vector.csv"

    t_file = open(title_vector_file, 'rb')
    title_vector = np.loadtxt(t_file, delimiter=",")
    data["title"] = title_vector

    b_file = open(body_vector_file, 'rb')
    body_vector = np.loadtxt(b_file, delimiter=",")
    data["body"] = body_vector

    # TODO add tags and visibility fields

    return data

class_to_test = "122"
get_all_online_data(class_to_test)
# write_vectorized_data(class_to_test + "_posts.csv")
# data = read_vectorized_data(class_to_test + "_posts.csv")

# print data




