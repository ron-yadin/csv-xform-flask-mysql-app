from flask import Flask, render_template, request, send_from_directory
import mysql.connector
from datetime import datetime
from zoneinfo import ZoneInfo
from io import BytesIO
import zipfile

import csv_transform  # custom csv_transform module

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    """
    Flask route handler for the home page.

    Supports both GET and POST requests. For GET requests, renders the home page.
    For POST requests, processes the uploaded CSV file, creates a zip file containing
    input and output CSVs, and renders the home page with relevant information.

    Returns:
    - GET request: Rendered HTML template for the home page.
    - POST request:
        - Rendered HTML template with error message if file extension is not .csv or
          if the CSV processing encounters an error.
        - Rendered HTML template with processed input and output DataFrames if successful.
    """
    if request.method == "POST":
        # get file object from html form
        submitter = request.form.get("submitter")
        file = request.files["file"]
        if file:
            # get filename, separate name & extension
            filename = file.filename
            filename_no_ext, file_ext = tuple(filename.split("."))

            # verify file extension type
            try:
                assert file_ext.lower() == "csv"
            except:
                error_message_str = (
                    f"Exptected .csv file extension, but .{file_ext} detected"
                )
                return render_template("error.html", message=error_message_str)

            # get current time (US/Pacific) & format for output names
            current_time = datetime.now(ZoneInfo("America/Los_Angeles"))
            formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
            # create zip file name and path variables
            zip_file_name = f"{formatted_time}_{filename_no_ext}.zip"
            zip_file_path = f"/app/data/{zip_file_name}"

            # process csv file object, return both input and output dfs
            input_valid, input_df, output_df = csv_transform.process_csv(file)

            # handle cases of invalid input, direct user to the error message page
            if input_valid == False:
                # in this case, error_message_str stored in input_df variable
                return render_template("error.html", message=input_df)
            
            # add submission to MySQL database
            mydb = mysql.connector.connect(
                host="mysql",
                user="web_user",
                password="web_password",
                database="web_database"
            )
            mycursor = mydb.cursor()
            sql = "INSERT INTO submissions (submitter, submission_name) VALUES (%s, %s)"
            val = (submitter, filename_no_ext)
            mycursor.execute(sql, val)
            mydb.commit()

            # create BytesIO object to store the zip file in memory
            zip_buffer = BytesIO()

            # create a ZipFile object
            with zipfile.ZipFile(
                zip_buffer, "a", zipfile.ZIP_DEFLATED, False
            ) as zip_file:
                # write input CSV to the zip file
                zip_file.writestr(
                    f"{formatted_time}_{filename_no_ext}_input.csv",
                    input_df.to_csv(index=False),
                )
                # write output CSV to the zip file
                zip_file.writestr(
                    f"{formatted_time}_{filename_no_ext}_output.csv",
                    output_df.to_csv(index=False),
                )

            # move buffer position to the beginning to prepare for reading
            zip_buffer.seek(0)
            # write the zip file to the Docker volume
            with open(zip_file_path, "wb") as zip_file:
                zip_file.write(zip_buffer.read())
            # render index.html file, sending all relevant outputs and variables
            return render_template(
                "index.html",
                tables=[output_df.to_html(classes="data")],
                file_created=True,
                file_path=zip_file_path,
                result_file_name=zip_file_name,
            )

    return render_template("index.html")


@app.route("/download/<filename>")
def download_file(filename):
    """
    Flask route handler for downloading files from the '/app/data/' directory.

    Parameters:
    - filename (str): The name of the file to be downloaded.

    Returns:
    - File download response: Downloads the specified file as an attachment.
    """
    return send_from_directory("/app/data/", filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
