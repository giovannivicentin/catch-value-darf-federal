# Catch Value DARF Federal

This tool is designed to automate the process of extracting data from PDF files within a specific folder and store them in a MySQL database. The primary focus is on processing DARFs (Federal Tax Documents) which includes taxes such as INSS, IRRF, and other related taxes.

## Features

1. Extracts important information from the PDFs using regex patterns.
2. Connects and interacts with a MySQL database to either insert or update data.
3. Processes the following data points from the PDFs:
  - CNPJ
  - Razão Social
  - Valor
  - Período de Apuração
  - Data de Vencimento
  - Date and time of the data processing

### Utility Script: `show_your_regex.py`

There's an additional script named `show_your_regex.py` provided which can be used to print the content of the PDFs found in the specified directory. This helps in understanding what data is extracted before applying regex patterns.

## Getting Started

Prerequisites
Make sure you have the necessary libraries installed:<br>
`pip install -r requirements.txt` <br>

## Configuration

Environment Variables: Set up your environment variables in a .env file. <br>The tool expects a variable PDF_FOLDER that specifies the directory containing the PDFs to be processed.<br>
Database Parameters: Update main.py with your MySQL database connection parameters.

## Running the Script

After setting up your environment and updating your database parameters, you can run the main tool using:<br>
`python main.py`<br><br>
To simply display the content of the PDFs, you can use:<br>
`python show_your_regex.py`<br><br>
Libraries Used:

1. PyMySQL: MySQL database connector for Python. (Used to connect with the MySQL DB)
2. PyPDF2: A utility to read and extract information from PDFs.
3. python-dotenv: Reads key-value pairs from a .env file and sets them as environment variables.
