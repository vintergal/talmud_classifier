## Installation & Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
   *(Note 1: On Linux/macOS, you may need to use `python3` instead of `python`)*  
   *(Note 2: On Windows, if `python` is not recognized, try using `py` instead)*

2. **Activate the virtual environment:**
   * **Windows (PowerShell):**
     ```powershell
     venv\Scripts\Activate.ps1
     ```
   * **Windows (CMD):**
     ```cmd
     venv\Scripts\activate.bat
     ```
   * **Linux / macOS:**
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```


## the process
1.  **python (-append)? get_chapters_urls.py output_filename input_url**

	output_filename = the json file to export the urls of the html pages to download.
	
	input_url=the url to the page that contain the links of the output urls
	
	-append=for appending another urls the the existing list in an existing output_filename
	

2.  **python chapters_downloaders.py input_filename output_folder_path**

	input_filename - the output_file from the previous stage that contains a list of urls to html pages.

	output_folder_path- the path to download the html files to.


3. python get_html_files_list.py output_filename folder_path (might in the future combined in stage 4)

	output_filename= the json file that will contain a list of the paths to all the  raw html files from the previous stage.

	folderpath= the path to the folder contain all those files


4. **python chapters_parser.py input_filepath output_folder_path**

	input_filepath = the path to the file contains the paths to all the raw html files from the previous stage

	output_folder_path= the path to the folder that will contain all the json files with the rows dictionaries.
	


