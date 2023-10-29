from datetime import date
from flask import Flask, jsonify
import requests

app = Flask(__name__)
app.json.sort_keys = False


ragi_duties = {}
@app.route('/', methods=['GET'])
def main():
    try:
        # Read data from the JSON file
        

# URL of the GitHub Gist raw JSON file
        gist_url = "https://gist.githubusercontent.com/0xharkirat/587f68228c0a01ccf53d8339008d479f/raw/ca93c4a634f3f0a14f2469053565cdd093b45ee8/ragi_duties.json"

        
        response = requests.get(gist_url)
        if response.status_code == 200:
            # Parse the JSON content
            json_data = response.json()
            ragi_duties.update(json_data)
            
            # Now you can work with the JSON data
            
        else:
            return jsonify({"Failed to fetch data from the Gist. Status code:":response.status_code}), 500
    

                
        return jsonify({
            "routes":{
                "/all-duties": "Get all ragi duties for two weeks.",
                "/today": "Get today's ragi duties."
            }

        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to read data',
            'message': str(e)
            }), 500


# Define an endpoint to read and send data from the JSON file
@app.route('/all-duties', methods=['GET'])
def all_duties():
    try:
        if len(ragi_duties) == 0:
            main()
        return jsonify(ragi_duties), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to get data',
            'message': str(e)
            }), 500

    
    
@app.route('/today', methods=["GET"])
def today():
    today = date.today()
    d1 = today.strftime("%d-%m-%y")
    try:
        if len(ragi_duties) == 0:
            main()
        if d1 in ragi_duties:

            return jsonify({d1:ragi_duties[d1]}), 200
        else:
            return jsonify({
                "error": "The ragi list is not updated on SGPC.NET",
                "message": "Showing the most recent ragi list instead.",
                list(ragi_duties.keys())[-1] :ragi_duties[list(ragi_duties.keys())[-1]]})
    except Exception as e:
        return jsonify({
            'error': 'Failed to get today data',
            'message': str(e)
            }), 500


if __name__ == '__main__':
    app.run(debug=True)
