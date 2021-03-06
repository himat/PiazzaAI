from piazza_api import Piazza
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import numpy as np
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
    data["tags"] = data["tags"].replace(" ", "")
    data["tags"] = data["tags"].replace("|", " ")

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

    class_122_s17 = p.network("ix087c2ns5p656")
    class_122_f15 = p.network("idt0ymj51qr5do")
    class_122_f16 = p.network("irz1akgnpve6eo")
    class_381 = p.network("ixz5scp9zqi583")
    class_601 = p.network("ixs4v2xr1cz10d")

    ### Change this to download a different class's data
    class_to_download = None
    if piazza_class == "122_s17":
        class_to_download = class_122_s17
    elif piazza_class == "122_f15":
        class_to_download = class_122_f15
    elif piazza_class == "122_f16":
        class_to_download = class_122_f16
    elif piazza_class == "381":
        class_to_download = class_381
    elif piazza_class == "601":
        class_to_download = class_601
    else:
        raise ValueError("Invalid class name")
    export_file = piazza_class + export_file_suffix
    ###


    # Calling with no argument gets all posts
    all_responses = class_to_download.iter_all_posts()
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

        # print fields_dict["tags"]
        
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




class_to_test = "122_f16"
# f15, f16
# get_all_online_data(class_to_test)
# data = read_vectorized_data(class_to_test + "_posts.csv")

# print data




