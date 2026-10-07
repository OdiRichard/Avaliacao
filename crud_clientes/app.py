from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clientes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Modelo Cliente
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)

    def __repr__(self):
        return f"<Cliente {self.nome}>"


# Criar o banco de dados
with app.app_context():
    db.create_all()


# LISTAR CLIENTES


@app.route("/")
def index():
    clientes = Cliente.query.all()
    return render_template("index.html", clientes=clientes)


# ADICIONAR CLIENTE


@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():

    if request.method == "POST":

        try:
            nome = request.form["nome"]
            email = request.form["email"]
            cpf = request.form["cpf"]

            # Validação dos campos
            if not nome or not email or not cpf:
                return render_template(
                    "adicionar.html",
                    erro="Todos os campos são obrigatórios."
                )

            novo_cliente = Cliente(
                nome=nome,
                email=email,
                cpf=cpf
            )

            db.session.add(novo_cliente)
            db.session.commit()

            return redirect(url_for("index"))

        except Exception as erro:
            db.session.rollback()

            return render_template(
                "adicionar.html",
                erro=f"Erro ao adicionar cliente: {erro}"
            )

    return render_template("adicionar.html")


# EDITAR CLIENTE


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    cliente = Cliente.query.get_or_404(id)

    if request.method == "POST":

        try:
            nome = request.form["nome"]
            email = request.form["email"]
            cpf = request.form["cpf"]

            # Validação dos campos
            if not nome or not email or not cpf:
                return render_template(
                    "editar.html",
                    cliente=cliente,
                    erro="Todos os campos são obrigatórios."
                )

            cliente.nome = nome
            cliente.email = email
            cliente.cpf = cpf

            db.session.commit()

            return redirect(url_for("index"))

        except Exception as erro:
            db.session.rollback()

            return render_template(
                "editar.html",
                cliente=cliente,
                erro=f"Erro ao editar cliente: {erro}"
            )

    return render_template(
        "editar.html",
        cliente=cliente
    )


# EXCLUIR CLIENTE


@app.route("/deletar/<int:id>")
def deletar(id):

    cliente = Cliente.query.get_or_404(id)

    try:
        db.session.delete(cliente)
        db.session.commit()

    except Exception:
        db.session.rollback()

    return redirect(url_for("index"))


# EXECUTAR A APLICAÇÃO


if __name__ == "__main__":
    app.run(debug=True)