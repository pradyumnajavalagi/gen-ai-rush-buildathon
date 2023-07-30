from flask import Flask, render_template, jsonify, request
import pandas as pd
import model  # Replace with the module that contains your AI model

app = Flask(__name__, template_folder="templates")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['file']
        file_extension = file.filename.split('.')[-1]

        # Check if the file extension is CSV or Excel
        if file_extension.lower() in ['csv', 'xls', 'xlsx']:
            # Read the CSV or Excel file using pandas
            df = pd.read_csv(file) if file_extension.lower() == 'csv' else pd.read_excel(file)

            # Perform data preprocessing (if required)
            # ...

            # Make predictions using your AI model
            prediction = model.predict(df)  # Replace with your prediction function

            return jsonify({'result': prediction}), 200
        else:
            return jsonify({'error': 'Invalid file format. Only CSV and Excel files are allowed.'}), 400

    except Exception as e:
        return jsonify({'error': 'Error processing the file. ' + str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
