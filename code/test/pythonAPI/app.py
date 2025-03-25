import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_profiling_rules(regulatory_text):
    """Generate data profiling rules using OpenAI"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a regulatory compliance assistant. Generate specific data validation rules based on regulatory instructions."},
                {"role": "user", "content": f"Create precise data validation rules for these regulations:\n{regulatory_text}\n\nReturn only the rules in a format that can be implemented in Python code."}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating rules: {str(e)}"

def validate_data(df, rules):
    """Validate data against generated rules"""
    validation_results = []
    
    # Basic validation based on common rules
    if "Transaction_Amount should match Reported_Amount" in rules:
        df['Validation_Result'] = df.apply(
            lambda row: "Valid" if row['Transaction_Amount'] == row['Reported_Amount'] else "Flagged: Amount mismatch",
            axis=1
        )
    
    # Add more rule implementations as needed
    return df.to_dict(orient='records')

@app.route('/process', methods=['POST'])
def process():
    if 'csv_file' not in request.files or 'regulatory_text' not in request.form:
        return jsonify({"error": "Missing required parameters"}), 400
    
    csv_file = request.files['csv_file']
    regulatory_text = request.form['regulatory_text']
    
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Generate profiling rules
        rules = generate_profiling_rules(regulatory_text)
        
        # Validate data
        validation_results = validate_data(df, rules)
        
        return jsonify({
            "rules": rules,
            "validation_results": validation_results,
            "token_count": len(regulatory_text.split())  # Simple token count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)