#! /usr/bin/python3
#
# Written by @HaydnNitzsche


from lxml import html
import requests
import os
import os.path
import argparse
from os import path
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader

WEBSITE_BASE_PATH = ""
BASE_PATH_TREE = None

def main():
    setup()
    download_chapters()
    
def download_chapters():
    for chapter in get_chapters()[::-1]:
        title = chapter.text.strip()
        outfile_path = "manga/%s/%s.pdf" %(get_manga_name(), title)
        if path.exists(outfile_path):
            print("Skipping chapter: %s. Already downloaded." %(title))
        else:
            chapter_number = title.split(" - ")[-1]
            current_webpage_path = build_chapter_path(chapter_number) 
            current_webpage = requests.get(current_webpage_path)
            tree = html.fromstring(current_webpage.content)
            img_urls = tree.xpath('//img/@src')
            generate_pdf(title,img_urls,outfile_path)

def generate_pdf(chapter_title, img_urls, out_file_path):
    print("Downloading images for chapter: %s."%(chapter_title))
    canvas = Canvas(out_file_path)
    canvas.setTitle(chapter_title)
    for img_url in img_urls:
        print ('downloading image: %s' % img_url)
        filename = img_url.split('/')[-1]
        download_img(img_url, filename)
        try:
            image = ImageReader(filename)
            canvas.setPageSize(image.getSize())
            canvas.drawImage(image, x=0, y=0)
            canvas.showPage()
        except:
            print("Error, bad file %s downloaded from %s."%(filename,img_url))
        os.remove(filename)
    canvas.save()
    print("Finished downloading images for chapter: %s."%(chapter_title))

def setup():
    global WEBSITE_BASE_PATH
    parser = argparse.ArgumentParser(description="Download manga from kissmanga.com in pdf format", usage='%(prog)s url')
    parser.add_argument('url', help='Manga url. Must be from https://www.mngdoom.com/.')
    args = parser.parse_args()
    WEBSITE_BASE_PATH = args.url
    manga_name = get_manga_name()
    disclaimer_file_path = "manga/disclaimer.txt"
    manga_chapters_path = "manga/%s"%(manga_name)
    if not os.path.isdir(manga_chapters_path):
        print("Output directory not found, creating it now at %s."%(manga_name))
        os.makedirs(manga_chapters_path)
    if not os.path.isfile(disclaimer_file_path):
        print("Disclaimer file not found, creating it now at %s."%(disclaimer_file_path))
        disclaimer = open(disclaimer_file_path, "w+").write("Disclaimer: These chapters were downloaded from %s and are scanlations. The quality of typesetting/translation is not guaranteed to be great and, as such, you should buy the official releases if you want high quality translations." %(WEBSITE_BASE_PATH))

def get_chapters():
    tree = get_base_path_tree()
    chapters = tree.findall(".//span[@class='val']")
    return chapters

def get_manga_name():
    tree = get_base_path_tree()
    return tree.xpath("//title/text()")[0].split(" Manga - ")[0].split("Read ")[1]

def get_base_path_tree():
    global BASE_PATH_TREE
    if not BASE_PATH_TREE:
        webpage = requests.get(WEBSITE_BASE_PATH)
        BASE_PATH_TREE = html.fromstring(webpage.content)
    return BASE_PATH_TREE

def download_img(img_url, filename):
    r = requests.get(img_url, allow_redirects=True)
    downloaded_img = open(filename, "wb").write(r.content)

def build_chapter_path(chapter_number):
    global WEBSITE_BASE_PATH
    return WEBSITE_BASE_PATH + "/%s/all-pages" %(chapter_number)

main()