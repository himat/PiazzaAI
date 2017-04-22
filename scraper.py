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

export_file = "posts.csv"

# Fields that are exported to be used for converting to features
TITLE_FIELDS = ["title", "body", "visibility", "tags"]

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

# response = class_122.get_post(2770)
response = class_381.get_post(189)

# for field in response:
    # print field, response[field]

children = response['children']
# for c in children:
    # print c

# all_responses = class_122.iter_all_posts(1000)

# count = 0
# for r in all_responses:
    # count+=1

    # if(count % 100 == 0):
        # print count


html_parser = HTMLParser()

def remove_html_tags(content):

    html_tags = ["p", "b", "tt", "div", "ul", "li"]

    for tag in html_tags:
        content = content.replace("<"+tag+">", "")
        content = content.replace("</"+tag+">", "")

    content = content.replace("<br />", " ")

    # Remove entirety of images
    content = re.sub("<img.*/>", " ", content)

    return content

def clean_text(content):
    # TODO: Return length of code

    # print "before\n", content
    
    # Convert HTML codes into normal unicode characters
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

# Returns a list of relevant fields from a post for exporting
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


def get_all_online_data():

    # Calling with no argument gets all posts
    all_responses = class_122.iter_all_posts()
    # all_responses = [class_122.get_post(2816)]
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

def write_bag_of_words(input_csv):

    data = pd.read_csv(input_csv, header=0)
    file_title = input_csv.split(".")[0]
    print file_title


    title_out_file = file_title + "_title_vector.csv"
    body_out_file = file_title + "_body_vector.csv"

    vectorizer = CountVectorizer(analyzer = 'word', stop_words = 'english')
    title_vector = (vectorizer.fit_transform(data['title'])).toarray()
    body_vector = (vectorizer.fit_transform(data['body'])).toarray()

    t_out_file = open(title_out_file, 'wb')

    np.savetxt(t_out_file, title_vector, delimiter=",", fmt="%02d")

    b_out_file = open(body_out_file, 'wb')
    np.savetxt(b_out_file, body_vector, delimiter=",", fmt="%02d")

    t_out_file = open(title_out_file, 'rb')

    read_title_vector = np.loadtxt(t_out_file, delimiter=",")
    b_out_file = open(body_out_file, 'rb')
    read_body_vector = np.loadtxt(b_out_file, delimiter=",")

    print title_vector.shape
    print read_title_vector.shape

    print title_vector[0]
    print read_title_vector[0]
    
    assert(np.array_equal(title_vector, read_title_vector))
    assert(np.array_equal(body_vector, read_body_vector))

# get_all_online_data()
write_bag_of_words("122_posts.csv")




