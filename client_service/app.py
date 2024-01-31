from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def get_data_from_api(api_url, query_params=None):
    try:
        response = requests.get(api_url, params=query_params)
        response.raise_for_status()

        data = response.json()

        if query_params:
            filtered_data = []
            for key, value in query_params.items():
                for books in data:
                    if key in books:
                        if key == "id" or key == "publication_year":
                            value = int(value)
                        if books[key] == value:
                            filtered_data.append(books)
            return filtered_data
        else:
            return data
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

@app.route('/get_data', methods=['GET'])
def get_data():

    api_url = 'http://book-api-server-dns.cye8ahgvh7b6dkea.uksouth.azurecontainer.io:5000/books'

    query_parameters = request.args.to_dict()

    result = get_data_from_api(api_url, query_params=query_parameters)

    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Failed to retrieve data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
