from bs4 import BeautifulSoup
import json
import re
import sys
from pathlib import Path



def parse_chapter(input_file, output_folder_path):
    with open(input_file, "r", encoding="utf-8") as file_to_read:
        
        file_html_soup=BeautifulSoup(file_to_read.read(),"html.parser")
        book_name=file_html_soup.find("a", target="info").text
        book_name=re.sub(r'[<>:"/\\|?*]+', "_", book_name).strip()
        
        sub_title="sub="
        sub_index=input_file.find(sub_title)
        if (sub_index>-1):
            sub_num=input_file[sub_index+len(sub_title):].replace(".html","")
            book_name+=sub_num
        rows_soup :BeautifulSoup=file_html_soup.find("table", class_="text-display").find_all("tr")

        rows={}

        for row in rows_soup:
            childs:BeautifulSoup=row.find_all("td")
            name=childs[0].find("span").text
            words=[]
            if (len(childs)>1):
                words=childs[1].get_text(separator=" ").split()
            rows[name]=words
        Path(output_folder_path).mkdir(parents=True, exist_ok=True)
        with open(f"{output_folder_path}/{book_name}.json", "w", encoding="utf-8") as file_to_write:
            json.dump(rows, file_to_write, ensure_ascii=False, indent=2)

def main(input_filepath,output_folder_path):

    raw_html_files_paths=[]
    with open(input_filepath,"r")as input_file:
        raw_html_files_paths=json.load(fp=input_file)
    num_of_input_files=len(raw_html_files_paths)
    for index,raw_html_file_path in enumerate(raw_html_files_paths):
        print(f" exporting chapter number {index+1} out of {num_of_input_files} chapters listed")
        parse_chapter(input_file=raw_html_file_path,output_folder_path=output_folder_path)
    print("done")

#python chapters_parser.py input_filepath output_file_path
if __name__ == "__main__":
    if (len(sys.argv)>2):
        main(input_filepath=sys.argv[1],output_folder_path=sys.argv[2])
    
