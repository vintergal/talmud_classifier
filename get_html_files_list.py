from pathlib import Path
import pprint
import sys
import json

def main(output_filename,folder_path):
    files_list = [f"{folder_path}/{f.name}" for f in Path(folder_path).iterdir() if f.is_file()]

    # Prints valid Python list syntax formatted neatly
    with open(output_filename,"w") as output_file:
        json.dump(fp=output_file,obj=files_list,indent=2)
        print("done")
    



#python get_html_files_list.py output_filename folder_path
if __name__ == "__main__":
    if len(sys.argv)>2:
        main(output_filename=sys.argv[1],folder_path=sys.argv[2])
    

