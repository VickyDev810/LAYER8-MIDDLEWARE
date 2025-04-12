# Data Analyzer with LLMs

This application allows users to upload CSV and PDF files and analyze them using Google's Gemini language models. The system converts user queries to SQL-like operations to extract information from the data.

## Setup

1. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

   Note: If you encounter issues with `tabula-py`, you may need to install Java separately as it's a requirement for tabula.

3. Create a `.env` file in the root directory with your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

   You can get a Gemini API key by:
   - Go to https://makersuite.google.com/app/apikey
   - Sign in with your Google account
   - Create an API key 

4. Start the backend server:
   ```
   python app.py
   ```

5. In a new terminal, navigate to the frontend directory and install dependencies:
   ```
   cd frontend
   npm install
   ```

6. Start the frontend development server:
   ```
   npm run dev
   ```

7. Open your browser and go to `http://localhost:5173`

## Features

- Upload CSV and PDF files
- Extract tabular data from PDFs automatically
- Query the data using natural language
- View the results in a structured format
- Download the analysis results

## Supported File Types

### CSV Files
The application supports standard CSV files with proper formatting. Large files (>16MB) may take longer to process.

### PDF Files
PDF support includes:
- Table extraction: The system will attempt to detect and extract tables from your PDF documents.
- Text extraction: If tables can't be detected, the system will extract text and attempt to convert it to tabular format.
- Multi-page support: Tables from all pages will be combined when possible.

## Technology Stack

- **Backend**: Flask, Pandas, SQLite, Google Gemini AI, Tabula, PyPDF2
- **Frontend**: React, Styled Components, React Table, React Dropzone
- **Data Processing**: SQL queries generated from natural language

## Troubleshooting

If you encounter issues, please see the `TROUBLESHOOTING.md` file for common problems and solutions. 