from flask import Flask, render_template, request, redirect, url_for, flash, session, redirect
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import JSON
from sqlalchemy.types import TypeDecorator, Date
from decimal import Decimal, InvalidOperation
import os

basedir = os.path.abspath(os.path.dirname(__file__))
CLIENT_SECRETS_FILE = os.path.join(basedir, 'client_secret.json')

app = Flask(__name__)
# Configurar SQLite com caminho absoluto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'crm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = '123456'

# Criar pasta de banco de dados se não existir
os.makedirs(os.path.join(basedir, 'database'), exist_ok=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Nome da função de login

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

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

class SafeDate(TypeDecorator):
    """Um TypeDecorator para o tipo Date que verifica o tipo do valor antes de converter."""
    impl = Date

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        # Se o valor for do tipo bytes, decodifica
        if isinstance(value, bytes):
            try:
                value = value.decode('utf-8')
            except Exception:
                return value
        # Se for string, converte para objeto date
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except Exception:
                return value
        # Se já for um objeto date, retorna como está
        return value

    def process_bind_param(self, value, dialect):
        # Se for None, retorna None
        if value is None:
            return value
        # Se for um objeto date, retorna-o sem alterar
        if isinstance(value, date):
            return value
        return value

class Contrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))  # 'ensaio' ou 'evento'
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Campos comuns
    descricao_servico = db.Column(db.Text)
    valor = db.Column(db.Numeric(10, 2))  # Exemplo ajustado para numérico
    forma_pagamento = db.Column(db.String(100))

    # Campos de ensaio
    data_ensaio = db.Column(SafeDate)      # Utilizando SafeDate
    horario_ensaio = db.Column(db.Time)
    local_ensaio = db.Column(db.String(100))
    cidade_ensaio = db.Column(db.String(50))
    estado_ensaio = db.Column(db.String(2))
    duracao_ensaio = db.Column(db.String(20))

    # Campos de evento
    nome_evento = db.Column(db.String(100))
    data_evento = db.Column(SafeDate)       # Utilizando SafeDate
    horario_evento = db.Column(db.Time)
    # Armazena os locais de evento como lista de objetos JSON
    locais_evento = db.Column(MutableList.as_mutable(JSON), default=[])
    tempo_cobertura = db.Column(db.String(20))
    qtd_fotografos = db.Column(db.Integer)

    cliente = db.relationship('Cliente', backref=db.backref('contratos', lazy=True))

# Rotas e lógica do aplicativo
@app.route("/")
@login_required
def home():
    hoje = date.today()

    # Busca ensaios e eventos futuros
    ensaios = Contrato.query.filter(
        Contrato.usuario_id == current_user.id,
        Contrato.tipo == "ensaio",
        Contrato.data_ensaio >= hoje
    ).order_by(Contrato.data_ensaio).all()

    eventos = Contrato.query.filter(
        Contrato.usuario_id == current_user.id,
        Contrato.tipo == "evento",
        Contrato.data_evento >= hoje
    ).order_by(Contrato.data_evento).all()

    # Converte para um formato adequado para exibição
    agenda = []
    for ensaio in ensaios:
        agenda.append({
            "tipo": "ensaio",
            "obj": ensaio,
            "data": ensaio.data_ensaio,
            "highlight": ensaio.data_ensaio == hoje
        })

    for evento in eventos:
        agenda.append({
            "tipo": "evento",
            "obj": evento,
            "data": evento.data_evento,
            "highlight": evento.data_evento == hoje
        })

    agenda.sort(key=lambda x: x["data"])  # Ordena pela data

    # Informações gerais
    total_contratos = Contrato.query.filter_by(usuario_id=current_user.id).count()
    faturamento = db.session.query(db.func.sum(Contrato.valor)).filter(Contrato.usuario_id == current_user.id).scalar() or 0.00

    return render_template("home.html", agenda=agenda, total_contratos=total_contratos, faturamento=faturamento)

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
    return render_template("login.html", show_sidebar=False)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sessão.", "info")
    return redirect(url_for("login"))

from flask import render_template, request, flash, redirect, url_for

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            serializer = generate_serializer()
            # Gera um token com o e-mail, válido por 3600 segundos (1 hora)
            token = serializer.dumps(email, salt='password-reset-salt')
            reset_url = url_for('reset_password', token=token, _external=True)
            
            # Aqui você deve enviar o e-mail real com o reset_url.
            # Por enquanto, vamos exibir o link como flash para testes.
            flash(f'Link para redefinir a senha: {reset_url}', 'info')
            
            # Em produção, envie este link utilizando Flask-Mail ou outra estratégia.
        else:
            flash('E-mail não encontrado.', 'danger')
        return redirect(url_for('login'))
    return render_template('forgot_password.html', show_sidebar=False)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    serializer = generate_serializer()
    try:
        # Tenta recuperar o e-mail do token com expiração de 3600 segundos (1h)
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception as e:
        flash('O token de redefinição é inválido ou expirou.', 'danger')
        return redirect(url_for('forgot_password'))
        
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        nova_senha = request.form.get('senha')
        confirma_senha = request.form.get('confirma_senha')
        if nova_senha != confirma_senha:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('reset_password', token=token))
            
        # Atualiza a senha com o método que já deve gerar o hash (por exemplo, set_senha)
        usuario.set_senha(nova_senha)
        db.session.commit()
        flash('Senha redefinida com sucesso!', 'success')
        return redirect(url_for('login'))
        
    return render_template('reset_password.html', token=token, show_sidebar=False)

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
    return render_template("registrar.html", show_sidebar=False)

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

@app.route("/contrato/form", methods=["GET", "POST"])
@app.route("/contrato/<int:id>/form", methods=["GET", "POST"])
@login_required
def contrato_form(id=None):
    contrato = Contrato.query.get(id) if id else None
    clientes = Cliente.query.filter_by(usuario_id=current_user.id).order_by(Cliente.nome).all()
    
    if request.method == "POST":
        if not contrato:
            contrato = Contrato(
                tipo=request.form.get("tipo") or "ensaio",
                cliente_id=request.form.get("cliente_id"),
                usuario_id=current_user.id,
                descricao_servico=request.form.get("descricao_servico") or "",
                forma_pagamento=request.form.get("forma_pagamento") or "",
                valor=request.form.get("valor") or 0.00
            )
            db.session.add(contrato)
        
        atualizar_campos_contrato(contrato, request.form)
        
        if contrato.tipo == "evento":
            locais = []
            locais_nome = request.form.getlist("local_evento[]") or []
            cidades = request.form.getlist("cidade_evento[]") or []
            estados = request.form.getlist("estado_evento[]") or []
            
            for i in range(len(locais_nome)):
                if locais_nome[i].strip():
                    locais.append({
                        "local": locais_nome[i],
                        "cidade": cidades[i] if i < len(cidades) else "",
                        "estado": estados[i] if i < len(estados) else ""
                    })
            contrato.locais_evento = locais
        
        try:
            db.session.commit()
            if contrato.id:
                flash("Contrato salvo com sucesso!", "success")
                return redirect(url_for("visualizar_contrato", id=contrato.id))
            else:
                flash("Erro ao salvar contrato. ID não foi gerado.", "danger")
        except Exception as e:
            db.session.rollback()
            flash("Falha ao salvar o contrato.", "danger")
            print(e)
    
    tipo_default = contrato.tipo if contrato else "ensaio"
    return render_template("contrato_form.html", contrato=contrato, tipo=tipo_default, clientes=clientes)

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

@app.route("/contrato/<int:id>/excluir", methods=["POST"])
@login_required
def excluir_contrato(id):
    contrato = Contrato.query.get_or_404(id)
    db.session.delete(contrato)
    db.session.commit()
    flash("Contrato excluído com sucesso!", "success")
    return redirect(url_for("listar_contratos"))

@app.route('/configuracoes', methods=['GET', 'POST'])
@login_required
def configuracoes():
    if request.method == "POST":
        action = request.form.get('action')
        
        # 1. Editar Cadastro (nome e e-mail)
        if action == "editar":
            nome = request.form.get('nome')
            email = request.form.get('email')
            current_user.nome = nome
            current_user.email = email
            try:
                db.session.commit()
                flash("Cadastro atualizado com sucesso.", "success")
            except Exception as e:
                db.session.rollback()
                flash("Erro ao atualizar cadastro.", "danger")
        
        # 2. Alterar Senha
        elif action == "alterar_senha":
            senha_atual = request.form.get('senha_atual')
            nova_senha = request.form.get('nova_senha')
            confirmar_nova = request.form.get('confirmar_nova_senha')
            if not current_user.check_password(senha_atual):
                flash("Senha atual incorreta.", "danger")
            elif nova_senha != confirmar_nova:
                flash("A nova senha e a confirmação não coincidem.", "danger")
            else:
                current_user.set_senha(nova_senha)
                try:
                    db.session.commit()
                    flash("Senha alterada com sucesso.", "success")
                except Exception as e:
                    db.session.rollback()
                    flash("Erro ao alterar senha.", "danger")
        
        # 3. Atualizar Foto de Perfil
        elif action == "upload_foto":
            if 'foto' not in request.files:
                flash("Nenhum arquivo enviado.", "danger")
            else:
                
                foto_file = request.files['foto']
                if foto_file.filename != "":
                    filename = secure_filename(foto_file.filename)
                    upload_path = os.path.join(app.root_path, 'static/uploads')
                    if not os.path.exists(upload_path):
                        os.makedirs(upload_path)
                    foto_path = os.path.join(upload_path, filename)
                    foto_file.save(foto_path)
                    # Armazena o caminho relativo no banco de dados:
                    current_user.foto_perfil_url = 'uploads/' + filename
                    db.session.commit()

                    try:
                        db.session.commit()
                        flash("Foto de perfil atualizada.", "success")
                    except Exception as e:
                        db.session.rollback()
                        flash("Erro ao atualizar foto.", "danger")
                else:
                    flash("Selecione uma foto válida.", "danger")
        
        # 4. Excluir Perfil
        elif action == "excluir_perfil":
            try:
                db.session.delete(current_user)
                db.session.commit()
                flash("Perfil excluído.", "success")
                logout_user()
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash("Erro ao excluir perfil.", "danger")
        
        return redirect(url_for('configuracoes'))
        
    return render_template('configuracoes.html', show_sidebar=True)

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

def criar_evento_google(cal_event):
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    # Exemplo: Criando um evento no Google Agenda
    evento = {
        'summary': cal_event['summary'],
        'location': cal_event.get('location', ''),
        'description': cal_event.get('description', ''),
        'start': {
            'dateTime': cal_event['start'],  # Em formato ISO: '2025-07-01T09:00:00-03:00'
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': cal_event['end'],  # Em formato ISO
            'timeZone': 'America/Sao_Paulo',
        },
    }
    created_event = service.events().insert(calendarId='primary', body=evento).execute()

    # Atualiza as credenciais na sessão, se necessário (caso elas tenham sido refrescadas)
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return created_event

def generate_serializer():
    return URLSafeTimedSerializer(app.config['SECRET_KEY'])

def atualizar_campos_contrato(contrato, form):
    contrato.cliente_id = form.get("cliente_id")
    contrato.tipo = form.get("tipo")
    contrato.descricao_servico = form.get("descricao_servico")
    
    # Converter o valor: substitui vírgula por ponto e converte para Decimal
    valor_str = form.get("valor")
    if valor_str:
        try:
            contrato.valor = Decimal(valor_str.strip().replace(",", "."))
        except InvalidOperation:
            contrato.valor = None
    else:
        contrato.valor = None

    contrato.forma_pagamento = form.get("forma_pagamento")
    
    # Obtém o estado e a cidade (dos selects, via API do IBGE ou outro método)
    estado = form.get("uf")
    cidade = form.get("cidade_estado")
    
    if contrato.tipo == "ensaio":
        # Converte a data de ensaio para um objeto date
        data_ensaio_str = form.get("data_ensaio")
        if data_ensaio_str:
            try:
                contrato.data_ensaio = date.fromisoformat(data_ensaio_str)
            except Exception:
                contrato.data_ensaio = None
        else:
            contrato.data_ensaio = None

        # Converte o horário de ensaio para um objeto time
        horario_ensaio_str = form.get("horario_ensaio")
        if horario_ensaio_str:
            try:
                contrato.horario_ensaio = datetime.strptime(horario_ensaio_str, "%H:%M").time()
            except Exception:
                contrato.horario_ensaio = None
        else:
            contrato.horario_ensaio = None

        contrato.local_ensaio   = form.get("local_ensaio")
        contrato.estado_ensaio  = estado
        contrato.cidade_ensaio  = cidade
        contrato.duracao_ensaio = form.get("duracao_ensaio")
    
    elif contrato.tipo == "evento":
        contrato.nome_evento = form.get("nome_evento")
        
        # Converte a data do evento para um objeto date
        data_evento_str = form.get("data_evento")
        if data_evento_str:
            try:
                contrato.data_evento = date.fromisoformat(data_evento_str)
            except Exception:
                contrato.data_evento = None
        else:
            contrato.data_evento = None

        # Converte o horário do evento para um objeto time
        horario_evento_str = form.get("horario_evento")
        if horario_evento_str:
            try:
                contrato.horario_evento = datetime.strptime(horario_evento_str, "%H:%M").time()
            except Exception:
                contrato.horario_evento = None
        else:
            contrato.horario_evento = None

        contrato.local_evento = form.get("local_evento")
        contrato.estado_evento = estado
        contrato.cidade_evento = cidade
        contrato.tempo_cobertura = form.get("tempo_cobertura")
        contrato.qtd_fotografos = form.get("qtd_fotografos")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
