from datetime import date
from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
app.json.sort_keys = False


ragi_duties = {}
@app.route('/', methods=['GET'])
def main():
    try:
        # Read data from the JSON file
        

# URL of the GitHub Gist raw JSON file
        gist_url = get_raw_url()

        if gist_url == 404:
            return jsonify({
            'error': 'Failed to get raw data',
            'message': str(e)
            }), 500


        
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
            },
            "usage": "ragi-duties-api.onrender.com/all-duties",
            "author": "0xharkirat",
            "email": "info.sandhukirat23@gmail.com",
            "data": "All data sourced from SGPC.NET",
            "disclaimer": "Ragi list and duty timings may not be updated in realtime on SGPC.NET",
            "thanks": "a 0xharkirat (Harkirat Singh) production.",
            "extra": "Add any json viewer extension to your browser to format the response."

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

def get_raw_url():
    try:
        gist_id = "587f68228c0a01ccf53d8339008d479f"

        # The filename you want to update in the Gist
        filename = "ragi_duties.json"

        # Your GitHub Personal Access Token
        access_token = os.environ.get('GIST_ACCESS_KEY')

        # URL of the GitHub Gist API endpoint
        gist_url = f"https://api.github.com/gists/{gist_id}"

        # New content to update the Gist file with
        new_content = {
            filename: {
                "content": "New content goes here"
            }
        }

        headers = {
            "Authorization": f"token {access_token}"
        }

        # Get the current Gist data
        response = requests.get(gist_url, headers=headers)

        if response.status_code == 200:
            gist_data = response.json()
            return gist_data["files"]["ragi_duties.json"]['raw_url']
        else:
            return 404

    except Exception as e:
        return 404

if __name__ == '__main__':
    app.run(debug=True)
