import requests
import sys
import os

def test_api_connection():
    """Test if the Flask API is up and running."""
    try:
        response = requests.get('http://localhost:5000/')
        if response.status_code == 200:
            print("✅ API is running!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the Flask server is running.")
        return False

def test_csv_upload():
    """Test the file upload endpoint with a test CSV file."""
    try:
        # Create a simple test CSV file
        with open('test_file.csv', 'w') as f:
            f.write("name,age,city\n")
            f.write("John,25,New York\n")
            f.write("Jane,30,San Francisco\n")
        
        # Attempt to upload the file
        files = {'file': open('test_file.csv', 'rb')}
        response = requests.post('http://localhost:5000/api/upload', files=files)
        
        if response.status_code == 200:
            print("✅ CSV file upload successful!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ CSV file upload failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the Flask server is running.")
        return False
    except Exception as e:
        print(f"❌ Error during CSV file upload test: {str(e)}")
        return False

def create_test_pdf():
    """Create a simple PDF file with tabular data for testing."""
    try:
        # Try to use reportlab to create a simple PDF
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib.units import inch
        
        pdf_filename = 'test_file.pdf'
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        
        # Create table data
        data = [
            ['Product', 'Price', 'Quantity', 'Total'],
            ['Widget A', '$10.00', '5', '$50.00'],
            ['Widget B', '$15.00', '3', '$45.00'],
            ['Widget C', '$8.50', '10', '$85.00'],
            ['Widget D', '$20.00', '2', '$40.00'],
        ]
        
        # Create the table
        table = Table(data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch])
        
        # Add style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)
        
        # Build the PDF
        elements = []
        elements.append(table)
        doc.build(elements)
        
        print(f"✅ Test PDF created: {pdf_filename}")
        return pdf_filename
    
    except ImportError:
        # If reportlab is not available, create a simple text file and rename it to PDF
        # This is not a real PDF but will work for testing the upload mechanism
        pdf_filename = 'test_file.pdf'
        with open(pdf_filename, 'w') as f:
            f.write("This is a test PDF file.\n")
            f.write("It contains some tabular data:\n\n")
            f.write("Product,Price,Quantity,Total\n")
            f.write("Widget A,$10.00,5,$50.00\n")
            f.write("Widget B,$15.00,3,$45.00\n")
            f.write("Widget C,$8.50,10,$85.00\n")
            f.write("Widget D,$20.00,2,$40.00\n")
        
        print(f"⚠️ Created a fake PDF (text file) for testing: {pdf_filename}")
        print("Install reportlab for proper PDF creation: pip install reportlab")
        return pdf_filename
    
    except Exception as e:
        print(f"❌ Error creating test PDF: {str(e)}")
        return None

def test_pdf_upload():
    """Test the file upload endpoint with a test PDF file."""
    try:
        # Create a test PDF file
        pdf_filename = create_test_pdf()
        if not pdf_filename:
            return False
        
        # Attempt to upload the file
        with open(pdf_filename, 'rb') as f:
            files = {'file': f}
            response = requests.post('http://localhost:5000/api/upload', files=files)
        
        if response.status_code == 200:
            print("✅ PDF file upload successful!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ PDF file upload failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the Flask server is running.")
        return False
    except Exception as e:
        print(f"❌ Error during PDF file upload test: {str(e)}")
        return False

if __name__ == "__main__":
    # Test API connection
    api_running = test_api_connection()
    
    # If API is running, test file uploads
    if api_running:
        print("\nTesting CSV file upload...")
        csv_success = test_csv_upload()
        
        print("\nTesting PDF file upload...")
        pdf_success = test_pdf_upload()
        
        # Cleanup test files
        for file in ['test_file.csv', 'test_file.pdf']:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    print(f"✅ Removed test file: {file}")
                except:
                    print(f"⚠️ Could not remove test file: {file}")
        
        # Summary
        print("\n=== TEST SUMMARY ===")
        print(f"API Connection: {'✅ Success' if api_running else '❌ Failed'}")
        print(f"CSV Upload: {'✅ Success' if csv_success else '❌ Failed'}")
        print(f"PDF Upload: {'✅ Success' if pdf_success else '❌ Failed'}")
    else:
        print("Skipping file upload tests as API is not running.")
    
    print("\nTests completed.") 