# CSV Transform Flask App with MySQL Database
## Overview
- A project demonstrating an extensible architecture for a containerized, full-stack webapp, capable of applying custom transform logic to a csv file.  

- There is a user interface webpage where a user can upload an input csv file, then view & download the transformed output csv. Additionally, the inputs, outputs, and submission events are tracked in a MySQL relational database. This database can be accessed through a second database admin webpage, where the database can be managed and queried with SQL. 
  
- This example simply calculates & adds a "sum" column to a two-column csv (with header columns "x" and "y").

- However, by following the steps below in the section <i>**How To Modify**</i> , this example can be augmented with more complex transformation/calculation logic, and be used to host a wide variety of data transformation solutions.
___
## Project File Structure
```
/csv-xform-flask-mysql-example
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
|-- init.sql
|-- README.md
```
___
## To Install Locally
1. Ensure Docker is installed, or follow [the install instructions found here](https://docs.docker.com/desktop/) to install it
1. Ensure Docker daemon is running locally (by starting Docker Desktop, for example)
1. Clone or download this repo to copy the required files & file structure locally
    - Open a terminal window and run: ```git clone https://github.com/ron-yadin/sv-xform-flask-mysql-example.git```
    - Alternatively, click green ```Code``` button >  ```Download ZIP```, then unzip the file locally
## To Run Locally
1. Open a terminal window
1. Navigate to the project folder ```cd local/path/to/basic-csv-xform-flask-app-example```    
    - update the path to match project folder location in local filesystem 
1. Run the command: ```docker-compose up --build```
1. Open a web browser and visit ```localhost:5001``` for the webapp user interface
1. Open a web browser and visit ```localhost:8080``` for the MySQL database administration interface
    - For example purposes, the user name is ```web_user``` and the password is ```web_password``` 
    - **THIS IS INSECURE AND FOR DEMONSTRATION PURPOSES ONLY. FOR PRODUCTION, A SECRET MANAGER OR ENVIRONMENT VARIABLES SHOULD BE USED**
        - These would need to be updated appropriately in the ```docker-compose.yml``` file, the ```app.py``` file, and for use when signing into the administration web interface
___
## How To Modify
1. Edit the ```init.sql``` file to create the tables to match the new desired data model
1. Change ```csv_transform.py``` file
    - If necessary, update how the file object content is parsed into a pandas dataframe
        - ex: if new csv has a header rows that must be skipped
    - Change assumption check sections in ```try/except``` blocks to match assumptions for new input csv
        - Update any ```error_message_str``` objects to match new assumption checks
    - Change transformation/calculation logic as required to get from new input dataframe to output dataframe
    - Update the database loading section to match the update tables in the new data model
1. Update the ```requirements.txt``` file
    - If new logic uses any additional packages/libraries, add them to the ```requirements.txt``` file to ensure availability in the container environment
1. Add appropriate example files to the ```/data``` folder
    - Replace the ```example_input_file.csv```, ```empty_template_input_file.csv```, ```example_zip_file.zip``` (optional) with relevant example and template files
    - The ```index.html``` references those file names exactly for the example and template download links. If those file names change, update the download links in the ```index.html``` file 