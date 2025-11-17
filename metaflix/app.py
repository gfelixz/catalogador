from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # Filme ou Série
    nota = db.Column(db.Float, nullable=False)
    critica = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    medias = Media.query.all()
    return render_template("index.html", medias=medias)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        titulo = request.form["titulo"]
        tipo = request.form["tipo"]
        nota = float(request.form["nota"])
        critica = request.form["critica"]

        novo = Media(titulo=titulo, tipo=tipo, nota=nota, critica=critica)
        db.session.add(novo)
        db.session.commit()

        return redirect("/")
    return render_template("add.html")

@app.route("/details/<int:id>")
def details(id):
    item = Media.query.get(id)
    return render_template("details.html", item=item)

if __name__ == "__main__":
    app.run(debug=True)
