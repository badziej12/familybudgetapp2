from flask import Flask, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://yibymviy:nwztR5-SCou-ZgyEgcgtOHDfIQUk3yb3@abul.db.elephantsql.com/yibymviy"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


