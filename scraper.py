from piazza_api import Piazza
from HTMLParser import HTMLParser
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

def clean_text(content):
    # TODO: Remove html tags
    # TODO: Return length of code
    
    # Convert HTML codes into normal unicode characters
    content = html_parser.unescape(content)

    content = content.encode('unicode-escape')

    # Remove a unicode string
    content = re.sub('\\\u[0-9a-f]{4}', " ", content)

    # Remove newlines
    content = content.replace("\\n", " ")

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

    return data

def export_all_data():

    # Calling with no argument gets all posts
    all_responses = class_122.iter_all_posts(200)
    # all_responses = [class_122.get_post(2833)]
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



export_all_data()





