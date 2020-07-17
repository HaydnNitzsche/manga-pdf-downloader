# manga-pdf-downloader
Download manga from [MangaDoom](https://www.mngdoom.com/). 

## Install
- Download the repo ```git clone https://github.com/HaydnNitzsche/manga-pdf-downloader.git```
- Call ```makefile```

## How to Use manga-pdf-downloader

The only parameter needed is ```url```.

Calls follow the format ```./manga_pdf_downloader url```

Example: ```./manga_pdf_downloader https://www.mngdoom.com/Boku-no-Hero-Academia```

##Output
Chapters will be downloaded from oldest to newest and placed in a directory named after the manga.

## How it Works
Using ```lxml```, the DOM of the webpage is parsed and the chapter list is grabbed. The page for each chapter is then visited and all page images downloaded using ```requests```. The images are then added to a PDF by ```reportlab```. Currently, only MangaDoom is supported.

## Disclaimers
I can only guarantee that the scraper worked at the time of publishing. Additionally, I cannot guarantee the quality of scans or translations downloaded by the scraper. I can not also guarantee that all chapters/pages of a particular manga will be downloaded successfully.
