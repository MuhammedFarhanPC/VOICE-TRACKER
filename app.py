from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

CSV_FILE = 'data.csv'
EXCEL_FILE = 'data.xlsx'

# Create CSV file with headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=['Timestamp', 'Account Holder', 'Amount'])
    df.to_csv(CSV_FILE, index=False)

@app.route('/')
def index():
    df = pd.read_csv(CSV_FILE)
    data = df.to_dict(orient='records')
    return render_template('index.html', data=data)  # Changed to index.html

@app.route('/save', methods=['POST'])
def save():
    text = request.json.get('text', '')
    parts = text.strip().split()
    if len(parts) >= 2 and parts[-1].replace('.', '', 1).isdigit():
        name = ' '.join(parts[:-1]).title()
        amount = float(parts[-1])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        df = pd.read_csv(CSV_FILE)
        new_entry = {'Timestamp': timestamp, 'Account Holder': name, 'Amount': amount}
        new_df = pd.DataFrame([new_entry])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

        return jsonify({'success': True, 'msg': f"{name} ₹{amount} saved!", 'entry': new_entry})

    return jsonify({'success': False, 'msg': 'Could not extract name or amount. Try again.'})

@app.route('/download')
def download():
    df = pd.read_csv(CSV_FILE)
    df.to_excel(EXCEL_FILE, index=False)
    return send_file(EXCEL_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
