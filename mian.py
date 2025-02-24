from bottle import Bottle, request, response, run, static_file, error
import requests
import json

application = Bottle()  # renamed from "app" to "application"

@application.error(404)
def error404(error):
    return static_file('index.html', root='/home/corsproxyIT/mysite')

@application.route('/home')
def home():
    return static_file('cloude-index.html', root='/home/corsproxyIT/mysite')

@application.route('/fetch', method=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
def proxy():
    try:
        # Get the target URL from query parameters
        url = request.query.get("url")
        # print(url)
        if not url:
            response.content_type = 'application/json'
            response.status = 400
            return json.dumps({"error": "Missing 'url' query parameter"})

        # Prepare headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36",
        }

        # Read the request body (if any)
        data = request.body.read()

        # Forward the request to the target URL using the same method
        r = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=data,
            cookies=request.cookies,
        )

        # Set CORS headers on the response
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.content_type = 'application/json'
        response.status = r.status_code

        return json.dumps({"data": r.text})

    except Exception as e:
        response.content_type = 'application/json'
        response.status = 500
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    run(application, host='0.0.0.0', port=5000, debug=True)
