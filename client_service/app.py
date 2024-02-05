from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__)

api_url = os.getenv('BOOK_API_URL', 'http://book-api-server-dns.cye8ahgvh7b6dkea.uksouth.azurecontainer.io:5000/books')

def get_data_from_api(api_url, query_params=None):
    try:
        response = requests.get(api_url, params=query_params)
        response.raise_for_status()

        data = response.json()

        return data

        '''
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
        '''

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

@app.route('/get_data', methods=['GET'])
def get_data():
    query_parameters = request.args.to_dict()

    result = get_data_from_api(query_params=query_parameters)

    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Failed to retrieve data'}), 500

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/search_result", methods=["POST"])
def search_result():

    query_params = {key: value for key, value in {
        "author": request.form.get("author"),
        "genre": request.form.get("genre"),
        "id": request.form.get("id"),
        "publication_year": request.form.get("publication_year"),
        "title": request.form.get("title")
    }.items() if value is not ''}

    print(query_params)
    
    try:
        result = get_data_from_api(api_url, query_params=query_params)
        
        if len(result) > 1 or result == []: return "Invalid search input. Please try again." 

        else: return render_template("search_result.html", author=result[0]["author"],
                        genre=result[0]["genre"], id=result[0]["id"],
                        publication_year=result[0]["publication_year"],
                        title=result[0]["title"])
    
    except Exception as e:
        return "Unknown Error. Please try again."
      


