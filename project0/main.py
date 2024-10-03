import argparse
import urllib.request
import sqlite3
import pypdf
from pypdf import PdfReader
import os
import re
import io 

def fetchincidents(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    }
    response = urllib.request.urlopen(urllib.request.Request(url, headers=headers))
    data = response.read()

    # Creating an in-memory bytes buffer
    pdf_buffer = io.BytesIO(data)
    return pdf_buffer 

def extractincidents(pdf_buffer):
    reader = PdfReader(pdf_buffer)  # Reading from the in-memory buffer
    incidents = []

    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout")
        lines = text.split('\n')  # Spliting the text into lines

        for line in lines:
            # Strip leading/trailing whitespace
            stripped_line = line.strip()

            fields = re.split(r'\s{2,}', stripped_line)

            if ':' in stripped_line:
                if len(fields) >= 3:  
                    date_time = fields[0]
                    incident_number = fields[1]
                    location = fields[2]
                    nature = fields[3]
                    incident_ori = fields[4]

                    incidents.append((date_time, incident_number, location, nature, incident_ori))

    return incidents

#Function to create a database
def createdb():
    db_path = "resources/normanpd.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS incidents (
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
    )
    ''')
    
    connection.commit()
    return connection

#Function to add data into the database
def populatedb(db_connection, incidents):
    cursor = db_connection.cursor()

    # Clear existing records before inserting new data
    cursor.execute('DELETE FROM incidents')
    
    cursor.executemany('''
    INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
    VALUES (?, ?, ?, ?, ?)
    ''', incidents)
    
    db_connection.commit()

#Function to print the nature of incident in ascending order from the database
def status(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('''
    SELECT nature, COUNT(*)
    FROM incidents
    GROUP BY nature
    ORDER BY nature ASC
    ''')
    
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"{row[0]}|{row[1]}")

def main(url):
    # Download data
    incident_data = fetchincidents(url)

    # Extract data
    incidents = extractincidents(incident_data)
	
    # Create new database
    db = createdb()
	
    # Insert data
    populatedb(db, incidents)
	
    # Print incident counts
    status(db)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download, parse, and store incident data from Norman PD website.")
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary PDF URL.")
    
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
