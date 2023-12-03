from website import create_app
from flask import request,Response
app = create_app()

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000) 
    # app.run() 
