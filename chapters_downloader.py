import requests
from bs4 import BeautifulSoup
import time

urls = [
        "https://cal.huc.edu/get_a_chapter.php?file=71001&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71002&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71003&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71004&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71005&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71006&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71007&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71008&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71010&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71011&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71012&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71013&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71014&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71015&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71016&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71017&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71018&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71019&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71020&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71021&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71022&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71023&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71024&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71025&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71026&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71027&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71028&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71029&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71030&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71031&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71032&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71033&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71034&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71035&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71036&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71037&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71038&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71500&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=01&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=02&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=03&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=11&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=14&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=18&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=19&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=21&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=22&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=24&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=26&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=27&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=30&cset=H&page=all",
        "https://cal.huc.edu/get_a_chapter.php?file=71600&sub=35&cset=H&page=all",
        ]

def getFileNameFromUrl(url:str):
    start_word_file="file="
    start_word_sub="&sub="
    end_word="&cset="
    start_index_file=url.find(start_word_file)
    end_index_file=url.find(start_word_sub)
    if (end_index_file>-1):
        end_index_file=url.find(end_word)
    return f"c_{url[start_index_file+len(start_word_file):end_index_file]}".replace(end_word,"")
    
    


    
def exportHtmlToFile(file_name, url):
    # Only standard HTTP headers belong here (all keys and values must be strings)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Timeout is passed as a direct argument to requests.get(), not inside headers
    response = requests.get(url=url, headers=headers, timeout=30)
    response.raise_for_status()

    with open(f"raw_html_files/{file_name}.html", "w", encoding="utf-8") as file:
        file.write(response.text)

if __name__ == "__main__":
    num_of_chapters=len(urls)
    for index, url in enumerate(urls):
        print(f" exporting chapter number {index+1} out of {num_of_chapters} chapters listed")
        name=getFileNameFromUrl(url=urls[index])
        exportHtmlToFile(file_name=name,url=url)
        time.sleep(3)

    print("done")