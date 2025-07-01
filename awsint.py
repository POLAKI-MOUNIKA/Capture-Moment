import boto3
from flask import Flask, jsonify

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name = "region-name")
photographers_table = dynamodb.Table('dynamodb_table_name')


@app.route('/photographers', methods = ['GET'])
def get_photographers():
    try:
        response = photographers_table.scan()
        return jsonify(response['Items'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ =='_main_':
    app.run(debug=True)