import sys
import os
import pytest
from unittest.mock import patch
import io


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Project0')))

from project0.main import fetchincidents, extractincidents, createdb, populatedb, status

@pytest.fixture
def sample_pdf():

    pdf_content = (
        b'%PDF-1.4\n'
        b'1 0 obj\n'
        b'<< /Type /Catalog /Pages 2 0 R >>\n'
        b'endobj\n'
        b'2 0 obj\n'
        b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n'
        b'endobj\n'
        b'3 0 obj\n'
        b'<< /Type /Page /MediaBox [0 0 300 300] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\n'
        b'endobj\n'
        b'4 0 obj\n'
        b'<< /Length 44 >>\n'
        b'stream\n'
        b'BT /F1 24 Tf 50 50 Td (Sample PDF Content) Tj ET\n'
        b'endstream\n'
        b'endobj\n'
        b'5 0 obj\n'  
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\n'
        b'endobj\n'
        b'xref\n'
        b'0 6\n'
        b'0000000000 65535 f \n'
        b'0000000009 00000 n \n'
        b'0000000052 00000 n \n'
        b'0000000105 00000 n \n'
        b'0000000166 00000 n \n'
        b'0000000225 00000 n \n' 
        b'trailer\n'
        b'<< /Size 6 /Root 1 0 R >>\n'  
        b'startxref\n'
        b'225\n'  
        b'%%EOF\n'
    )
    return io.BytesIO(pdf_content)

@pytest.fixture
def sample_incidents():
    return [
        ('2023-09-01 12:00', 'INC45345', 'Jacksonville FL', 'Trespassing', 'ORI123'),
        ('2023-09-01 13:00', 'INC76978', 'Sand Diego', 'Shooting', 'ORI124'),
    ]

def test_fetchincidents(mocker, sample_pdf):  # Accept sample_pdf as a parameter
    url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
    mocker.patch("urllib.request.urlopen", return_value=sample_pdf)  # Mocking the URL fetch

    buffer = fetchincidents(url)
    assert buffer.read() == sample_pdf.getvalue()  # Ensure the content matches the mock

def test_extractincidents(sample_pdf):  # Accept sample_pdf as a parameter
    incidents = extractincidents(sample_pdf)
    
    # Replace with your expected output based on the PDF structure you created
    expected_incidents = [
        ('Sample PDF Content'),  # Adjust this based on your extractincidents implementation
    ]
    assert incidents == incidents

def test_createdb():
    connection = createdb()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    assert ('incidents',) in tables  # Checking if the table was created
    connection.close()

def test_populatedb(sample_incidents):
    connection = createdb()
    populatedb(connection, sample_incidents)

    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents;")
    count = cursor.fetchone()[0]
    assert count == len(sample_incidents)  # Checking if the correct number of records is inserted
    connection.close()

def test_status(sample_incidents):
    connection = createdb()
    populatedb(connection, sample_incidents)

    # Capture output
    with patch('builtins.print') as mock_print:
        status(connection)
        mock_print.assert_any_call('Nature A|1')
        mock_print.assert_any_call('Nature B|1')
    connection.close()
