from flask import Flask, render_template, request, redirect, url_for, flash, render_template_string
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from clausulas_padrao import clausulas_por_tipo
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Nome da função de login

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

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
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

# Modelo de usuário para autenticação
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)  # Corrigir aqui

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


# Modelo de contrato que pode ser de evento ou ensaio
class Contrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))  # 'ensaio' ou 'evento'
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
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

class ClausulaPersonalizada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contrato.id'))
    clausula_numero = db.Column(db.String(10))
    conteudo = db.Column(db.Text)

    contrato = db.relationship('Contrato', backref=db.backref('clausulas_personalizadas', lazy=True))

# Rotas e lógica do aplicativo
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("home"))
        else:
            flash("Credenciais inválidas", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sessão.", "info")
    return redirect(url_for("login"))

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        if Usuario.query.filter_by(email=email).first():
            flash("E-mail já cadastrado", "warning")
        else:
            usuario = Usuario(nome=nome, email=email)
            usuario.set_senha(senha)
            db.session.add(usuario)
            db.session.commit()
            flash("Cadastro realizado!", "success")
            return redirect(url_for("login"))
    return render_template("registrar.html")

@app.route("/clientes")
@login_required
def listar_clientes():
    clientes = Cliente.query.filter_by(usuario_id=current_user.id).order_by(Cliente.nome).all()
    return render_template("listar_clientes.html", clientes=clientes)

@app.route("/clientes/novo", methods=["GET", "POST"])
@login_required
def cadastrar_cliente():
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        email = request.form["email"]
        whatsapp = request.form["whatsapp"]
        usuario_id=current_user.id

        if Cliente.query.filter_by(cpf=cpf).first():
            flash("CPF já cadastrado!", "error")
            return redirect(url_for("cadastrar_cliente"))

        cliente = Cliente(nome=nome, cpf=cpf, email=email, whatsapp=whatsapp, usuario_id=current_user.id)
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente cadastrado com sucesso!", "success")
        return redirect(url_for("listar_clientes"))

    return render_template("clientes.html")


@app.route('/cliente/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.cpf = request.form['cpf']
        cliente.email = request.form.get('email')
        cliente.whatsapp = request.form.get('whatsapp')
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('listar_clientes'))

    return render_template('editar_cliente.html', cliente=cliente)


@app.route('/cliente/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    if cliente.contratos:
        flash('Não é possível excluir um cliente com contratos vinculados.', 'danger')
        return redirect(url_for('listar_clientes'))

    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente excluído com sucesso.', 'success')
    return redirect(url_for('listar_clientes'))


@app.route("/contratos")
@login_required
def listar_contratos():
    contratos = Contrato.query.filter_by(usuario_id=current_user.id).order_by(Contrato.data_criacao.desc()).all()
    return render_template("listar_contratos.html", contratos=contratos)

@login_required
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
            usuario_id=current_user.id,
            descricao_servico=request.form.get("descricao_servico"),
            valor=request.form.get("valor"),
            forma_pagamento=request.form.get("forma_pagamento"),
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
@login_required
def visualizar_contrato(id):
    contrato = Contrato.query.get_or_404(id)
    cliente = contrato.cliente
    template = f'contrato_{contrato.tipo}.html'

    # Renderiza o contrato original em string
    html_contrato = render_template(template, contrato=contrato, cliente=cliente)

    # Passa o conteúdo para a nova página de visualização
    return render_template("contrato_visualizacao.html", contrato_conteudo=Markup(html_contrato))

@app.route("/contrato/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_contrato(id):
    contrato = Contrato.query.get_or_404(id)
    clientes = Cliente.query.order_by(Cliente.nome).all()

    if request.method == "POST":
        contrato.cliente_id = request.form.get("cliente_id")
        contrato.descricao_servico = request.form.get("descricao_servico")
        contrato.valor = request.form.get("valor")
        contrato.forma_pagamento = request.form.get("forma_pagamento")

        if contrato.tipo == "ensaio":
            contrato.data_ensaio = request.form.get("data_ensaio")
            contrato.horario_ensaio = request.form.get("horario_ensaio")
            contrato.local_ensaio = request.form.get("local_ensaio")
            contrato.cidade_estado_ensaio = request.form.get("cidade_estado_ensaio")
            contrato.duracao_ensaio = request.form.get("duracao_ensaio")
        else:
            contrato.nome_evento = request.form.get("nome_evento")
            contrato.data_evento = request.form.get("data_evento")
            contrato.horario_evento = request.form.get("horario_evento")
            contrato.local_evento = request.form.get("local_evento")
            contrato.cidade_estado_evento = request.form.get("cidade_estado_evento")
            contrato.tempo_cobertura = request.form.get("tempo_cobertura")
            contrato.qtd_fotografos = request.form.get("qtd_fotografos")

        db.session.commit()
        flash("Contrato atualizado com sucesso!", "success")
        return redirect(url_for("listar_contratos"))

    return render_template("contrato_form.html", contrato=contrato, tipo=contrato.tipo, clientes=clientes)

@app.route("/contrato/<int:id>/excluir", methods=["POST"])
@login_required
def excluir_contrato(id):
    contrato = Contrato.query.get_or_404(id)
    db.session.delete(contrato)
    db.session.commit()
    flash("Contrato excluído com sucesso!", "success")
    return redirect(url_for("listar_contratos"))

@app.route("/contrato/<int:id>/editar_clausulas", methods=["GET", "POST"])
@login_required
def editar_clausulas(id):
    contrato = Contrato.query.get_or_404(id)
    tipo = contrato.tipo
    clausulas = clausulas_por_tipo.get(tipo, {})

    if request.method == "POST":
        for numero in clausulas.keys():
            conteudo = request.form.get(f"clausula_{numero}")
            if conteudo:
                # Buscar cláusula existente
                clausula = ClausulaPersonalizada.query.filter_by(
                    contrato_id=contrato.id,
                    clausula_numero=numero
                ).first()

                if clausula:
                    clausula.conteudo = conteudo
                else:
                    nova = ClausulaPersonalizada(
                        contrato_id=contrato.id,
                        clausula_numero=numero,
                        conteudo=conteudo
                    )
                    db.session.add(nova)

        db.session.commit()
        flash("Cláusulas atualizadas com sucesso!", "success")
        return redirect(url_for("visualizar_contrato", id=contrato.id))

    return render_template("editar_clausulas.html", contrato=contrato, clausulas=clausulas)

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
    
def validar_cpf(cpf):
    return re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf)

def clausula_personalizada(contrato, numero):
    for c in contrato.clausulas_personalizadas:
        if c.clausula_numero == numero:
            return c.conteudo
    return None

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)