import os
import json
import pandas as pd
import io
import PyPDF2
import tabula
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
# Enable CORS for all routes with all options
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuration
UPLOAD_FOLDER = tempfile.mkdtemp()
print(f"Upload folder created at: {UPLOAD_FOLDER}")
ALLOWED_EXTENSIONS = {'csv', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB max upload

# Store uploaded files in memory
uploaded_files = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add a root route to confirm the API is working
@app.route('/')
def home():
    return jsonify({
        "status": "API is running",
        "endpoints": {
            "POST /api/upload": "Upload a CSV or PDF file",
            "POST /api/analyze": "Analyze a file with a query",
            "GET /api/files": "List all uploaded files"
        }
    })

def extract_tables_from_pdf(pdf_path):
    """Extract tables from a PDF file using tabula-py"""
    try:
        # Extract tables using tabula
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        
        if not tables:
            # If tabula doesn't find tables, try a different approach with PyPDF2 for text
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = ""
                for page_num in range(len(pdf_reader.pages)):
                    text_content += pdf_reader.pages[page_num].extract_text() + "\n"
                
                # Create a simple DataFrame from text (simplified approach)
                lines = [line for line in text_content.split('\n') if line.strip()]
                if lines:
                    # Try to split by common delimiters and create a DataFrame
                    data = []
                    for line in lines:
                        # Try different delimiters
                        for delimiter in [',', '\t', '|', ';']:
                            if delimiter in line:
                                data.append(line.split(delimiter))
                                break
                        else:
                            # No delimiter found, treat as single column
                            data.append([line])
                    
                    # Determine the maximum columns
                    max_cols = max(len(row) for row in data)
                    # Pad rows with fewer columns
                    for i in range(len(data)):
                        data[i] = data[i] + [''] * (max_cols - len(data[i]))
                    
                    # Create column names
                    columns = [f'Column_{i+1}' for i in range(max_cols)]
                    
                    # Create DataFrame
                    df = pd.DataFrame(data, columns=columns)
                    return df
            
            # If all else fails, return an empty DataFrame with a message column
            return pd.DataFrame({'Message': ['No structured data found in PDF']})
        
        # Combine all tables into one DataFrame if multiple tables found
        if len(tables) > 1:
            # Check if tables have compatible schemas
            columns = set()
            for table in tables:
                columns.update(table.columns)
            
            # Create a combined DataFrame with all columns
            combined_df = pd.DataFrame(columns=list(columns))
            
            # Append each table
            for table in tables:
                # Make sure all columns exist
                for col in columns:
                    if col not in table.columns:
                        table[col] = None
                combined_df = pd.concat([combined_df, table], ignore_index=True)
            
            return combined_df
        else:
            return tables[0]  # Return the single table found
    
    except Exception as e:
        print(f"Error extracting tables from PDF: {str(e)}")
        # Return a DataFrame with error information
        return pd.DataFrame({'Error': [f'Failed to extract data: {str(e)}']})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    print("\n======= UPLOAD REQUEST RECEIVED =======")
    print(f"Request method: {request.method}")
    print(f"Request content type: {request.content_type}")
    print(f"Request files: {request.files}")
    print(f"Request form: {request.form}")
    
    if 'file' not in request.files:
        print("ERROR: No file part in request")
        return jsonify({"error": "No file part in request"}), 400
    
    file = request.files['file']
    print(f"File object: {file}")
    print(f"File name: {file.filename}")
    
    if file.filename == '':
        print("ERROR: No selected file")
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        print(f"Saving file to: {file_path}")
        file.save(file_path)
        print(f"File saved successfully at: {file_path}")
        
        try:
            # Check if it's a PDF file
            if filename.lower().endswith('.pdf'):
                print("Processing PDF file...")
                # Extract tables from PDF
                df = extract_tables_from_pdf(file_path)
                file_type = 'pdf'
            else:
                print("Processing CSV file...")
                # Load the CSV into a pandas DataFrame
                df = pd.read_csv(file_path)
                file_type = 'csv'
            
            print(f"DataFrame shape: {df.shape}")
            print(f"DataFrame columns: {df.columns.tolist()}")
            
            # Store file data
            file_id = str(hash(filename + str(os.path.getmtime(file_path))))
            uploaded_files[file_id] = {
                "filename": filename,
                "path": file_path,
                "columns": list(df.columns),
                "sample": df.head(5).to_dict(orient='records'),
                "shape": df.shape,
                "type": file_type
            }
            
            print(f"File processed successfully. ID: {file_id}")
            return jsonify({
                "fileId": file_id,
                "filename": filename,
                "columns": uploaded_files[file_id]["columns"],
                "sample": uploaded_files[file_id]["sample"],
                "rows": df.shape[0],
                "columns_count": df.shape[1],
                "type": file_type
            }), 200
            
        except Exception as e:
            print(f"ERROR processing file: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
    
    print(f"ERROR: File type not allowed for {file.filename}")
    return jsonify({"error": f"File type not allowed. Please upload a CSV or PDF file."}), 400

@app.route('/api/analyze', methods=['POST'])
def analyze_file():
    data = request.json
    file_id = data.get('fileId')
    query = data.get('query')
    
    if not file_id or not query:
        return jsonify({"error": "Missing fileId or query"}), 400
    
    if file_id not in uploaded_files:
        return jsonify({"error": "File not found"}), 404
    
    try:
        file_info = uploaded_files[file_id]
        
        # Load the file based on its type
        if file_info.get("type") == "pdf":
            # For PDF files that were already processed
            df = pd.DataFrame(file_info["sample"])
        else:
            # For CSV files
            df = pd.read_csv(file_info["path"])
        
        # Generate SQL-like query using LLM
        sql_query = generate_sql_query(query, file_info["columns"], file_info["sample"])
        
        # Execute the query
        result = execute_query(sql_query, df)
        
        return jsonify({
            "sql_query": sql_query,
            "result": result
        }), 200
        
    except Exception as e:
        print(f"Error analyzing file: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

def generate_sql_query(query, columns, sample_data):
    """Generate a SQL query using Google's Gemini API"""
    try:
        prompt = f"""
        You are an AI assistant that translates natural language queries into SQL queries.
        
        Database Table: csv_data
        Columns: {', '.join(columns)}
        
        Sample data:
        {json.dumps(sample_data, indent=2)}
        
        User Query: {query}
        
        Translate the user query into a SQL query that can be executed against the CSV data.
        Return ONLY the SQL query without any explanation or formatting.
        """
        
        # Set up the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate the SQL query
        response = model.generate_content(prompt)
        
        # Extract the text from the response
        sql_query = response.text.strip()
        return sql_query
    
    except Exception as e:
        print(f"Error generating SQL query: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def execute_query(sql_query, df):
    """Execute a SQL-like query on the DataFrame"""
    try:
        import sqlite3
        from pandas.io import sql
        
        # Create a temporary in-memory database
        conn = sqlite3.connect(':memory:')
        
        # Write the dataframe into the database
        df.to_sql('csv_data', conn, index=False)
        
        # Execute the query
        result_df = pd.read_sql_query(sql_query, conn)
        
        # Close the connection
        conn.close()
        
        # Convert to list of dictionaries for JSON serialization
        result = result_df.to_dict(orient='records')
        
        return result
    
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.route('/api/files', methods=['GET'])
def get_files():
    files = []
    for file_id, file_info in uploaded_files.items():
        files.append({
            "fileId": file_id,
            "filename": file_info["filename"],
            "columns": file_info["columns"],
            "rows": file_info["shape"][0],
            "columns_count": file_info["shape"][1],
            "type": file_info.get("type", "csv")  # Default to csv for backwards compatibility
        })
    return jsonify({"files": files}), 200

if __name__ == '__main__':
    print(f"Starting Flask app, upload folder: {UPLOAD_FOLDER}")
    app.run(debug=True, port=5000) 