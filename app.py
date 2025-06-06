from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for, flash
import os
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

# Configurar SQLite com caminho absoluto
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'crm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Criar pasta de banco de dados se não existir
os.makedirs(os.path.join(basedir, 'database'), exist_ok=True)

db = SQLAlchemy(app)

# Modelo básico de cliente
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(100))
    whatsapp = db.Column(db.String(20))

# Modelo de contrato que pode ser de evento ou ensaio
class Contrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))  # 'evento' ou 'ensaio'
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Campos comuns
    descricao_servico = db.Column(db.Text)
    valor = db.Column(db.String(20))
    forma_pagamento = db.Column(db.String(100))

    # Campos de ensaio
    data_ensaio = db.Column(db.String(20))
    horario_ensaio = db.Column(db.String(20))
    local_ensaio = db.Column(db.String(100))
    cidade_estado_ensaio = db.Column(db.String(50))
    duracao_ensaio = db.Column(db.String(20))

    # Campos de evento
    nome_evento = db.Column(db.String(100))
    data_evento = db.Column(db.String(20))
    horario_evento = db.Column(db.String(20))
    local_evento = db.Column(db.String(100))
    cidade_estado_evento = db.Column(db.String(50))
    tempo_cobertura = db.Column(db.String(20))
    qtd_fotografos = db.Column(db.Integer)

    cliente = db.relationship('Cliente', backref=db.backref('contratos', lazy=True))

# Rotas e lógica do aplicativo
@app.route("/")
def home():
    return "Sistema iniciado com sucesso!"

@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        email = request.form["email"]
        whatsapp = request.form["whatsapp"]

        if Cliente.query.filter_by(cpf=cpf).first():
            flash("CPF já cadastrado!", "error")
            return redirect(url_for("clientes"))

        cliente = Cliente(nome=nome, cpf=cpf, email=email, whatsapp=whatsapp)
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente cadastrado com sucesso!", "success")
        return redirect(url_for("clientes"))

    clientes = Cliente.query.order_by(Cliente.nome).all()
    return render_template("clientes.html", clientes=clientes)

@app.route("/contratos")
def listar_contratos():
    contratos = Contrato.query.order_by(Contrato.data_criacao.desc()).all()
    return render_template("listar_contratos.html", contratos=contratos)

@app.route("/contrato/novo/<tipo>", methods=["GET", "POST"])
def novo_contrato(tipo):
    if tipo not in ['evento', 'ensaio']:
        return redirect(url_for('home'))

    clientes = Cliente.query.order_by(Cliente.nome).all()

    if request.method == "POST":
        cliente_id = request.form["cliente_id"]

        contrato = Contrato(
            tipo=tipo,
            cliente_id=cliente_id,
            descricao_servico=request.form.get("descricao_servico"),
            valor=request.form.get("valor"),
            forma_pagamento=request.form.get("forma_pagamento")
        )

        if tipo == "ensaio":
            contrato.data_ensaio = request.form.get("data_ensaio")
            contrato.horario_ensaio = request.form.get("horario_ensaio")
            contrato.local_ensaio = request.form.get("local_ensaio")
            contrato.cidade_estado_ensaio = request.form.get("cidade_estado_ensaio")
            contrato.duracao_ensaio = request.form.get("duracao_ensaio")
        else:  # evento
            contrato.nome_evento = request.form.get("nome_evento")
            contrato.data_evento = request.form.get("data_evento")
            contrato.horario_evento = request.form.get("horario_evento")
            contrato.local_evento = request.form.get("local_evento")
            contrato.cidade_estado_evento = request.form.get("cidade_estado_evento")
            contrato.tempo_cobertura = request.form.get("tempo_cobertura")
            contrato.qtd_fotografos = request.form.get("qtd_fotografos")

        db.session.add(contrato)
        db.session.commit()

        flash("Contrato criado com sucesso!", "success")
        return redirect(url_for("visualizar_contrato", id=contrato.id))

    return render_template("contrato_form.html", tipo=tipo, clientes=clientes)

@app.route('/contrato/<int:id>')
def visualizar_contrato(id):
    contrato = Contrato.query.get_or_404(id)
    cliente = contrato.cliente
    template = f'contrato_{contrato.tipo}.html'
    return render_template(template, contrato=contrato, cliente=cliente)

from datetime import datetime

# Filtro para formatar data por extenso 
@app.template_filter('data_por_extenso')
def data_por_extenso(data_str):
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d')
        meses = [
            'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
            'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
        ]
        return f"{data.day} de {meses[data.month - 1]} de {data.year}"
    except:
        return data_str

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)