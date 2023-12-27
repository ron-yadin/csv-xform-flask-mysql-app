# Basic CSV Transform Flask App Example
## Project Overview
A project demonstrating a basic, extensible architecture for a containerized, full-stack webapp, capable of applying custom transform logic to a csv file.
  
This example simply calculates & adds a "sum" column to a two-column csv (with header columns "x" and "y").

However, by following the steps below in the section <i>**How To Modify**</i> , this example can be augmented with more complex transformation/calculation logic, and be used to host a wide variety of data transformation solutions.
___
## Project File Structure
```
/basic-csv-xform-flask-app-example
|-- data (for example files & output zip files)
|   |-- empty_template_input_file.csv
|   |-- example_input_file.csv
|   |-- 2023-12-25_15-41-15_example_input_file.zip 
        (format: YYYY-MM-DD_HH-MM-SS_<filename>.zip)
|-- webapp
|   |-- templates
|       |-- error.html
|       |-- index.html
|   |-- app.py
|   |-- csv_transform.py
|   |-- Dockerfile
|   |-- requirements.txt
|-- .gitignore
|-- docker-compose.yml
|-- README.md
```
___
## To Install Locally
1. Ensure Docker is installed, or follow [the install instructions found here](https://docs.docker.com/desktop/) to install it
1. Ensure Docker is running locally (by starting Docker Desktop)
1. Clone or download this repo to copy the required files & file structure locally
    - Open a terminal window and run: ```git clone https://github.com/ron-yadin/basic-csv-xform-flask-app-example.git```
    - Alternatively, click green ```Code``` button >  ```Download ZIP```, then unzip the file locally
## To Run Locally
1. Open a terminal window
1. CD into the project folder "/basic-csv-xform-flask-app-example"
1. Run the command: ```docker-compose up --build```
1. Open a web browser and visit ```localhost:5001```
___
## How To Modify
1. Change ```csv_transform.py``` file
    - If necessary, update how the file object content is parsed into a pandas dataframe
    - Change assumption check sections in ```try/except``` blocks to match assumptions for new input csv
        - Update any ```error_message_str``` objects to match new assumption checks
    - Change transformation/calculation logic as required to get from new input dataframe to output dataframe
1. Update the ```requirements.txt``` file
    - If new logic uses any additional packages/libraries, add them to the ```requirements.txt``` file to ensure availability in the container environment
1. Add appropriate example files to the ```/data``` folder
    - Replace the ```example_input_file.csv```, ```empty_template_input_file.csv```, ```example_zip_file.zip``` (optional) with relevant example and template files
    - The ```index.html``` references those file names exactly for the example and template download links. If those file names change, update the download links in the ```index.html``` file 