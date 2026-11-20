import requests
from bs4 import BeautifulSoup
import time
import sys
import json
from urllib.parse import urlparse



def main(output_filename,url,append_mode):
    books_urls=[]
    hostname=urlparse(url).hostname
    # Only standard HTTP headers belong here (all keys and values must be strings)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Timeout is passed as a direct argument to requests.get(), not inside headers
    response = requests.get(url=url, headers=headers, timeout=30)
    response.raise_for_status()

    html_soup=BeautifulSoup(response.text,"html.parser")
    books_urls = [f"https://{hostname}/{link.get("href")}" for link in html_soup.find_all(name="a",class_="book-link") if link.get("href")]
    
    if (append_mode):
        with open(output_filename, "r") as file:
            existing_data = json.load(file)
            books_urls=existing_data+books_urls
    
    with open(output_filename,"w") as output_file:
        json.dump(fp=output_file,obj=books_urls,indent=2)
    print("done")




#python (-append)? get_chapters_urls.py output_filename input_url
if __name__ == "__main__":
    argv=sys.argv
    append_tag="-append"
    append_mode=False
    if (append_tag in argv):
        argv.remove(append_tag)
        append_mode=True
    if len(argv)>2:
        
        main(output_filename=argv[1],url=argv[2],append_mode=append_mode)
    
