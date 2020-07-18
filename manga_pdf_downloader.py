#! /usr/bin/python3
#
# Written by @HaydnNitzsche

from lxml import html
import requests
import os
import sys
import os.path
import argparse
from os import path
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader

# Set up parser for CLI arguments
PARSER = argparse.ArgumentParser(description="Download manga from kissmanga.com in pdf format", usage='%(prog)s url')
PARSER.add_argument('url', help='Manga url. Must be a link from https://www.mngdoom.com/')

MANGA_NAME = None
def get_manga_name():
    global MANGA_NAME
    if not MANGA_NAME:
        tree = get_base_path_tree()
        MANGA_NAME = tree.xpath("//title/text()")[0].split(" Manga - ")[0].split("Read ")[1]
    return MANGA_NAME

MANGA_BASE_PATH = None
def get_manga_base_path():
    global MANGA_BASE_PATH
    global PARSER
    if not MANGA_BASE_PATH:
        args = PARSER.parse_args()
        MANGA_BASE_PATH = args.url
    return MANGA_BASE_PATH

BASE_PATH_TREE = None
def get_base_path_tree():
    global BASE_PATH_TREE
    if not BASE_PATH_TREE:
        webpage = requests.get(get_manga_base_path())
        BASE_PATH_TREE = html.fromstring(webpage.content)
    return BASE_PATH_TREE

def main():
    validate_inputs()
    setup()
    download_chapters()

def validate_inputs():
    global PARSER
    args = PARSER.parse_args()
    if args.url.find("https://www.mngdoom.com/") is -1:
        sys.exit("manga_pdf_downloader: error: invalid value for url. Must be a link from https://www.mngdoom.com/")

def setup():
    manga_chapters_path = "manga/%s"%(get_manga_name())
    if not os.path.isdir(manga_chapters_path):
        print("Output directory not found, creating it now at %s."%(get_manga_name()))
        os.makedirs(manga_chapters_path)
    disclaimer_file_path = "manga/disclaimer.txt"
    if not os.path.isfile(disclaimer_file_path):
        print("Disclaimer file not found, creating it now at %s."%(disclaimer_file_path))
        disclaimer = open(disclaimer_file_path, "w+").write("Disclaimer: These chapters were downloaded from %s and are scanlations. The quality of typesetting/translation is not guaranteed to be great and, as such, you should buy the official releases if you want high quality translations." %(get_manga_base_path()))

def download_chapters():
    for chapter in get_base_path_tree().findall(".//span[@class='val']")[::-1]:
        chapter_title = chapter.text.strip()
        outfile_path = "manga/%s/%s.pdf" %(get_manga_name(), chapter_title)
        if path.exists(outfile_path):
            print("Skipping chapter: %s. Already downloaded." %(chapter_title))
        else:
            chapter_number = chapter_title.split(" - ")[-1]
            current_webpage_path = "%s/%s/all-pages" %(get_manga_base_path(), chapter_number)
            current_webpage = requests.get(current_webpage_path)
            tree = html.fromstring(current_webpage.content)
            img_urls = tree.xpath('//img/@src')
            generate_pdf(chapter_title,img_urls,outfile_path)
    print("Finished downloading chapters for: %s"%(get_manga_name()))

def generate_pdf(chapter_title, img_urls, out_file_path):
    print("Downloading images for chapter: %s."%(chapter_title))
    canvas = Canvas(out_file_path)
    canvas.setTitle(chapter_title)
    for img_url in img_urls:
        # Grabs the download link starting from the last occurence of http.
        # Helps solve some broken links
        img_url = img_url[img_url.rfind("http"):]
        print ('downloading image: %s' % img_url)
        filename = img_url.split('/')[-1]
        r = requests.get(img_url, allow_redirects=True)
        open(filename, "wb").write(r.content)
        try:
            image = ImageReader(filename)
            canvas.setPageSize(image.getSize())
            canvas.drawImage(image, x=0, y=0)
            canvas.showPage()
        except:
            print("Error, bad file %s downloaded from %s."%(filename,img_url))
        os.remove(filename)
    canvas.save()
    print("Finished downloading chapter: %s."%(chapter_title))

main()