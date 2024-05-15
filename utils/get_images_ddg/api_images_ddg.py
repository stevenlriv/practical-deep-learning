import requests
import re
import json
import os
import random
import string

# Main Function
# Search images by keyword on DuckDuckGo
# And saves them to a folder 
def search_images_ddg():
    keyword = input('Enter the search keyword: ')
    amount = input('Enter how many images you want: ')
    print('Looking for ' + amount + ' images of: ' + keyword)
    i = 0
    while i < int(amount):
        search_image(keyword)
        i += 1

# Sub Function 1
# Search image by keyword on DuckDuckGo
# This does not requires an API key
def search_image(keywords):
    url = 'https://duckduckgo.com/'
    params = {
        'q': keywords
    }

    print('Hitting DuckDuckGo for Token')

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M | re.I)

    if not searchObj:
        print('Token Parsing Failed !')
        print("Response:", res.text)  # Print the response for debugging
        return -1

    print('Obtained Token')

    headers = {
        'dnt': '1',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'x-requested-with': 'XMLHttpRequest',
        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6,ms;q=0.4',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': 'https://duckduckgo.com/',
        'authority': 'duckduckgo.com',
    }

    params = (
        ('l', 'wt-wt'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '2')
    )

    requestUrl = url + "i.js"

    try:
        res = requests.get(requestUrl, headers=headers, params=params)
        data = json.loads(res.text)
        saveImage(data["results"], keywords)
    except ValueError as e:
        print('Hitting Url Failure.')

# Sub Function 2
# Saves the Image in a folder
# and creates the folder if it does not exists
def saveImage(objs, keyword):
    for obj in objs:
        img_link = obj['image']
        img_data = requests.get(img_link).content

        # Specify the directory names
        main_directory = 'downloads'
        sub_directory = main_directory + "/" + keyword 

        # Check if the main directory exists
        if not os.path.exists(main_directory):
            os.mkdir(main_directory)

        # Check if the new subdirectory exists
        if not os.path.exists(sub_directory):
            os.mkdir(sub_directory)

        # Lets assign a name for the image
        filename = sub_directory + "/" + keyword + "_" + generate_random_string(6) + ".png"
        with open(filename, 'wb+') as f:
            f.write(img_data)

        print('File: ' + filename + ' successfully downloaded.')

# Utilities Functions

## Generates a random string based on the lenght provided
def generate_random_string(length):
    # Define the character set
    characters = string.ascii_letters + string.digits

    # Generate the random string
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string