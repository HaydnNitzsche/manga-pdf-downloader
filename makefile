run:
	pip install -r dependencies.dep
	cp manga_pdf_downloader.py manga_pdf_downloader
	chmod +x manga_pdf_downloader
clean:
	$(RM) manga_pdf_downloader
