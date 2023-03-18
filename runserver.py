from api import create_app
# from api.utils import db

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)