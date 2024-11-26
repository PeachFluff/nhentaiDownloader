import requests
import os
from bs4 import BeautifulSoup
import concurrent.futures
import time
#Pages count
#------------------------------
manga_id = 439211
imgs_to_cut = 1
#------------------------------

URL = "https://nhentai.net/g/%d/" % manga_id
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")


all_urls = []
pages_numbers = []

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

def image_parser(page_number):
    image_url = "https://nhentai.net/g/%d/%d/" % (manga_id, page_number)
    page = requests.get(image_url)
    soup = BeautifulSoup(page.content, "html.parser")
    page = soup.find("div", id="content")
    ab = page.find("section", id="image-container")
    dr = ab.find("img")["src"]
    return(dr)

for i in range(1,int(pages)+1):
    pages_numbers.append(i)

def new_download(page):
    urlq = image_parser(page)
    download_image(urlq, '%s/%d.jpg' % (title, page), page)

create_manga_folder(title)
start_time = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(new_download, pages_numbers)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.3f}s")