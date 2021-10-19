from band_app import app
from band_app.controllers import users, bands

if __name__=="__main__":
    app.run(debug=True)