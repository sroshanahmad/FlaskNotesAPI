from website import create_app

app = create_app()


if __name__ == '__main__': #gave this line so that anything inside it,executes only if we run the main.py and not when we import this file
    app.run(debug=True) # with debug=TRUE, everytime we make changes to our code, it is going to rerun the flask server, dont have to manually rerun

