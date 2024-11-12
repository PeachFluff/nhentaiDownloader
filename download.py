import requests
import os
from bs4 import BeautifulSoup

#Pages count
#------------------------------
manga_id = 537501
imgs_to_cut = 0
#------------------------------

URL = "https://nhentai.net/g/%d/" % manga_id
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

#Pretty name
info = soup.find(id="info")  
pages = info.find_all("span", class_ = "name")[-1].text

title = info.find_all("span", class_="pretty")
title = title[0].text
bad_chars = ["/","\\", ":","*","?","<",">","|"]
for i in bad_chars:
    title = title.replace(i, '')

def create_manga_folder(name):
    
    try:
        os.mkdir(name)
        print(f"Directory '{name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{name}' already exists.")

def download_image(url, save_as, image_number):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_as, 'wb') as file:
            file.write(response.content)
        print("Image downloaded", image_number, " / ", int(pages) - imgs_to_cut)
    else:
        print("Error Downloading Image")

def image_parser(manga_id, page_number):
    image_url = "https://nhentai.net/g/%d/%d/" % (manga_id, page_number)
    page = requests.get(image_url)
    soup = BeautifulSoup(page.content, "html.parser")
    page = soup.find("div", id="content")
    ab = page.find("section", id="image-container")
    dr = ab.find("img")["src"]
    return(dr)
image_parser(manga_id, 1)

def initiate_download(id):
    create_manga_folder(title)
    for aboba in range(1,int(pages)+1-imgs_to_cut):
        save_as = '%s/%d.jpg' % (title, aboba)
        download_image(image_parser(id, aboba), save_as, aboba)

initiate_download(manga_id)