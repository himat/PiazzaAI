from piazza_api import Piazza
from HTMLParser import HTMLParser
import csv
import re


config_file = "config.txt"
export_file = "posts.csv"

features = ["title", "body", "tags"]


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

def clean_post_content(content):
    # TODO: Remove html tags and code blocks
    # TODO: Return length of code as well 

    # Remove a unicode string
    content = re.sub(u'\xa0', " ", content)

    # Remove newlines
    content = content.replace("\n", "")

    # Convert HTML codes into normal unicode characters
    content = html_parser.unescape(content)
    
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
    data["title"] = title

    # Question text
    content_ = question["content"]
    content = clean_post_content(content_)
    data["body"] = content 

    # Question tags
    tags = post_resp["folders"]
    data["tags"] = "|".join(tags)

    for f in features:
        assert(f in data)

    return data

def export_all_data():
    all_responses = class_122.iter_all_posts(4)
    # all_responses = [class_122.get_post(2279)]
    
    out_file = open(export_file, "wb")
    csv_writer = csv.writer(out_file)


    # Write column headers of feature names
    csv_writer.writerow(features)

    for response in all_responses:
        
        fields_dict = get_relevant_fields(response)
        print fields_dict
        print fields_dict["body"]
        
        values = [fields_dict[k] for k in features]
        
        line = ','.join(values)

        csv_writer.writerow(values)

    

    out_file.close()



export_all_data()





