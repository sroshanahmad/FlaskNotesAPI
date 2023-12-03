from website import create_app
from flask import request,Response
app = create_app()

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res

if __name__ == '__main__': #gave this line so that anything inside it,executes only if we run the main.py and not when we import this file
    app.run() # with debug=TRUE, everytime we make changes to our code, it is going to rerun the flask server, dont have to manually rerun

