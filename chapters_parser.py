from bs4 import BeautifulSoup
import json
import re

input_files = ['raw_html_files/c_71001H&page=al.html',
 'raw_html_files/c_71002H&page=al.html',
 'raw_html_files/c_71003H&page=al.html',
 'raw_html_files/c_71004H&page=al.html',
 'raw_html_files/c_71005H&page=al.html',
 'raw_html_files/c_71006H&page=al.html',
 'raw_html_files/c_71007H&page=al.html',
 'raw_html_files/c_71008H&page=al.html',
 'raw_html_files/c_71010H&page=al.html',
 'raw_html_files/c_71011H&page=al.html',
 'raw_html_files/c_71012H&page=al.html',
 'raw_html_files/c_71013H&page=al.html',
 'raw_html_files/c_71014H&page=al.html',
 'raw_html_files/c_71015H&page=al.html',
 'raw_html_files/c_71016H&page=al.html',
 'raw_html_files/c_71017H&page=al.html',
 'raw_html_files/c_71018H&page=al.html',
 'raw_html_files/c_71019H&page=al.html',
 'raw_html_files/c_71020H&page=al.html',
 'raw_html_files/c_71021H&page=al.html',
 'raw_html_files/c_71022H&page=al.html',
 'raw_html_files/c_71023H&page=al.html',
 'raw_html_files/c_71024H&page=al.html',
 'raw_html_files/c_71025H&page=al.html',
 'raw_html_files/c_71026H&page=al.html',
 'raw_html_files/c_71027H&page=al.html',
 'raw_html_files/c_71028H&page=al.html',
 'raw_html_files/c_71029H&page=al.html',
 'raw_html_files/c_71030H&page=al.html',
 'raw_html_files/c_71031H&page=al.html',
 'raw_html_files/c_71032H&page=al.html',
 'raw_html_files/c_71033H&page=al.html',
 'raw_html_files/c_71034H&page=al.html',
 'raw_html_files/c_71035H&page=al.html',
 'raw_html_files/c_71036H&page=al.html',
 'raw_html_files/c_71037H&page=al.html',
 'raw_html_files/c_71038H&page=al.html',
 'raw_html_files/c_71500H&page=al.html',
 'raw_html_files/c_71600&sub=01.html',
 'raw_html_files/c_71600&sub=02.html',
 'raw_html_files/c_71600&sub=03.html',
 'raw_html_files/c_71600&sub=11.html',
 'raw_html_files/c_71600&sub=14.html',
 'raw_html_files/c_71600&sub=18.html',
 'raw_html_files/c_71600&sub=19.html',
 'raw_html_files/c_71600&sub=21.html',
 'raw_html_files/c_71600&sub=22.html',
 'raw_html_files/c_71600&sub=24.html',
 'raw_html_files/c_71600&sub=26.html',
 'raw_html_files/c_71600&sub=27.html',
 'raw_html_files/c_71600&sub=30.html',
 'raw_html_files/c_71600&sub=35.html']

def parse_chapter(input_file, output_folder="chapters_rows"):
    with open(input_file, "r", encoding="utf-8") as file_to_read:
        
        file_html_soup=BeautifulSoup(file_to_read.read(),"html.parser")
        book_name=file_html_soup.find("a", target="info").text
        book_name=re.sub(r'[<>:"/\\|?*]+', "_", book_name).strip()
        rows_soup :BeautifulSoup=file_html_soup.find("table", class_="text-display").find_all("tr")

        rows={}

        for row in rows_soup:
            childs:BeautifulSoup=row.find_all("td")
            name=childs[0].find("span").text
            words=[]
            if (len(childs)>1):
                words=childs[1].get_text(separator=" ").split()
            rows[name]=words
        with open(f"{output_folder}/{book_name}.json", "w", encoding="utf-8") as file_to_write:
            json.dump(rows, file_to_write, ensure_ascii=False, indent=2)
    
if __name__ == "__main__":
    num_of_input_files=len(input_files)
    for index,input_file in enumerate(input_files):
        print(f" exporting chapter number {index+1} out of {num_of_input_files} chapters listed")
        parse_chapter(input_file)


    print("done")
