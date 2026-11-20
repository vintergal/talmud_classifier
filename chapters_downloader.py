import requests
from bs4 import BeautifulSoup
import time
import sys
import json
from pathlib import Path


def getFileNameFromUrl(url:str):
    start_word_file="file="
    start_word_sub="&sub="
    end_word="&cset="
    start_index_file=url.find(start_word_file)
    end_index_file=url.find(start_word_sub)
    if (end_index_file>-1):
        end_index_file=url.find(end_word)
    return f"c_{url[start_index_file+len(start_word_file):end_index_file]}".replace(end_word,"")
    
    


    
def exportHtmlToFile(file_name,output_folder_path, url):
    # Only standard HTTP headers belong here (all keys and values must be strings)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Timeout is passed as a direct argument to requests.get(), not inside headers
    response = requests.get(url=url, headers=headers, timeout=30)
    response.raise_for_status()

    with open(f"{output_folder_path}/{file_name}.html", "w", encoding="utf-8") as file:
        file.write(response.text)

#python chapters_downloaders.py input_filename output_folder_path
if __name__ == "__main__":
    if len(sys.argv)<3:
        print("no filename given")
    else:
        output_folder_path=sys.argv[2]
        Path(output_folder_path).mkdir(parents=True, exist_ok=True)

        urls=""
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            urls=json.load(file)
        num_of_chapters=len(urls)

        for index, url in enumerate(urls):
            print(f" exporting chapter number {index+1} out of {num_of_chapters} chapters listed")
            name=getFileNameFromUrl(url=urls[index])
            exportHtmlToFile(file_name=name,url=url,output_folder_path=output_folder_path)
            time.sleep(3)

        print("done")