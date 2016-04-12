# electrodas
CSCI-544 Project for generation of Sanskrit Poetry using Recurrent Neural Networks

## Scraping
On TITUS, the pages are loaded into frames when the URL is hit. This restricts us from extracting the data directly from the HTML body. To resolve this, we used Selenium and WebDriver that opens the page in a firefox browser and then extracts the content from the loaded frames.

To run the script for scraping:
pip install -r req.txt
python sanskrit_crawl.py