from flask_app import app

#import the controller files here
from flask_app.controllers import users, companions, battles

if __name__ == "__main__":
    app.run(debug=True)
