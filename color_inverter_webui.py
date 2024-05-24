import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import tempfile
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if file is present in the request
        if 'file' not in request.files:
            app.logger.error('No file uploaded')
            return 'No file uploaded', 400
        
        file = request.files['file']
        
        # Check if the file has a valid filename
        if file.filename == '':
            app.logger.error('No file selected')
            return 'No file selected', 400
        
        # Save the uploaded file to a temporary location
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, secure_filename(file.filename))
        try:
            file.save(file_path)
        except Exception as e:
            app.logger.error(f'Error saving uploaded file: {str(e)}')
            return 'Error saving uploaded file', 500
        
        try:
            # Read the .col file
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Extract the color values from each line
            colors = []
            for line in lines:
                if line.strip() == '' or line.startswith('#') or line.startswith('INFO') or line.startswith('BaseColorsTableStored'):
                    continue
                
                values = line.split()
                if len(values) == 3:
                    r, g, b = map(int, values)
                    colors.append((r, g, b))
            
            # Reverse the order of colors
            reversed_colors = colors[::-1]
            
            # Create a temporary file for the inverted color palette
            with tempfile.NamedTemporaryFile(delete=False, suffix='.COL') as inverted_file:
                inverted_file_path = inverted_file.name
                
                # Write the reversed colors to the temporary file
                inverted_file.write(f"{len(reversed_colors)}\n\n".encode())
                
                for color in reversed_colors:
                    r, g, b = color
                    inverted_file.write(f"{r} {g} {b}\n".encode())
            
            # Send the inverted color palette file as a download
            try:
                return send_file(inverted_file_path, as_attachment=True, download_name='Inverted_' + file.filename)
            except Exception as e:
                app.logger.error(f'Error sending file: {str(e)}')
                return 'Error sending file', 500
        
        except Exception as e:
            app.logger.error(f'Error processing file: {str(e)}')
            return f"An error occurred: {str(e)}", 500
        
        finally:
            # Clean up the uploaded file
            try:
                os.remove(file_path)
            except Exception as e:
                app.logger.warning(f'Error removing uploaded file: {str(e)}')
            
            # Clean up the inverted file
            try:
                os.remove(inverted_file_path)
            except Exception as e:
                app.logger.warning(f'Error removing inverted file: {str(e)}')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)