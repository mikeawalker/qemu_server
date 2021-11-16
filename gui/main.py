from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from QemuModel import System, Processor, QemuRun, ProcessorType, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




if __name__ == "__main__":

    db.create_all(app=app)
    team = QemuRun()
    db.session.add(team)
    db.session.commit()
    print("done")
