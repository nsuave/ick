#!/usr/local/bin/python3

from bs4 import BeautifulSoup
from collections import OrderedDict
from fpdf import FPDF
import requests
import os
import sys

baseDomain = sys.argv[1]
series = sys.argv[2]
domain = baseDomain + "/" + sys.argv[3] + "/"
mailKey = sys.argv[4]
mailSandbox = sys.argv[5]
mailRecipient = sys.argv[6]
mailUrl = "https://api.mailgun.net/v3/" + mailSandbox + "/messages"

###
### FIND LATEST CHAPTER FROM ALL AVAILABLE CHAPTERS
###

# GET the HTML of the Chapters page and create bs4 soup object
reqChapters = requests.get(domain + series)
dataChapters = reqChapters.text
soupChapters = BeautifulSoup(dataChapters, features="html.parser")

# Define empty list
chapterList = []

# Find all links in page from bs4 soup, then append to list
for path in soupChapters.find_all('a', href=True):
    chapterList.append(path['href'])

# Only include the links that match the series name
matchingURI = [s for s in chapterList if "r/" + series in s]

# Create variable of the latest chapter URL
latestChapter = baseDomain + matchingURI[0]

###
### GET ALL URL'S VIA LATEST CHAPTER PAGE
###

reqLatestChapter = requests.get(latestChapter)
dataLatestChapter = reqLatestChapter.text
soupLatestChapter = BeautifulSoup(dataLatestChapter, features="html.parser")

chapterAllLinks = []

# Get the Base URI via chopping off the /# at the end of the matching URI
hold = matchingURI[0]
latestChapterBaseURI = hold[:-2]

#chapterLinks = soupLatestChapter.select("a[href*=next]")

for path in soupLatestChapter.find_all('a', href=True):
    chapterAllLinks.append(path['href'])

# Match based on baseURI
chapterAllURI = [s for s in chapterAllLinks if latestChapterBaseURI in s]

# Prepend the base domain so we have a full URL
chapterURLListRaw = [baseDomain + "{0}".format(i) for i in chapterAllURI]

# Removing duplicates
chapterURLList = list(OrderedDict.fromkeys(chapterURLListRaw))

###
### SCRAPE EACH URL FOR THEIR IMAGE URL'S
###
imageURLS = []

for url in chapterURLList:
    # GET the HTML of the current page and create bs4 soup object
    reqImage = requests.get(url)
    dataImage = reqImage.text
    soupImage = BeautifulSoup(dataImage, features="html.parser")

    # Find all images in current page from bs4 soup, then append src to list
    for img in soupImage.find_all('img'):
        imageURLS.append(img.get('src'))

# Prepend https:
imageURLS = ["https:{0}".format(i) for i in imageURLS]

###
### DOWNLOAD ALL IMAGES
###

# Include last 8 characters from the last / to get chapter number
latestChapterNumber = latestChapter[latestChapter.rfind("/")-8:]

# Only including the first 3 digits to get the last chapter number
latestChapterNumber = latestChapterNumber[:3]

# Create directory based on series and chapter number
directory = "/tmp/" + series + "_" + latestChapterNumber + "/"

# But first, check to see if it already exists
if os.path.exists(directory) == True:
    print("Directory " + directory + " already exists!")
    exit(1)
else:
    os.mkdir(directory)
    print(directory)

for url in imageURLS:
    r = requests.get(url)

    # Create filename variable based on url
    filename = url[url.rfind("/")+1:]

    if r.status_code == 200:
        with open(directory + filename,'wb') as f:
            f.write(r.content)

###
### CREATE PDF
###

# PDF file name setup, stripping trailing slash
convertedFile = directory.rstrip("/") + ".pdf"

# Sorting images and creating a pdf with static width
pdf = FPDF()
for image in sorted(os.listdir(directory)):
    pdf.add_page()
    pdf.image(directory + image, w=185)
pdf.output(convertedFile, "F")

###
### EMAIL
###

mailRequest = requests.post(
    mailUrl, 
    auth=("api", mailKey),  
    data={
        "from": "postmaster@" + mailSandbox,
        "to": mailRecipient,
        "subject": "Incoming!",
        "text": convertedFile
    },
    files={"attachment": (convertedFile, open(convertedFile, "rb"))},
)

print(mailRequest.status_code)
print(mailRequest.text)