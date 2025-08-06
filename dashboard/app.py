# -*- coding: utf-8 -*-
"""
Dashboard de Monitoramento de Servidores - Backend Principal

Este script implementa o backend para o dashboard de monitoramento de servidores.
Utiliza Flask para criar um servidor web e uma API RESTful, psutil para coletar
métricas do sistema operacional, e SQLite para armazenar os dados históricos.

O sistema atende aos seguintes requisitos do projeto:
- Coleta de métricas de CPU, RAM, disco e rede.
- Armazenamento em banco de dados SQLite.
- Fornecimento de dados para uma interface web via API.
- Execução de coleta de dados em background.
"""

# --- Importações de Módulos ---
# Flask: Micro-framework web para criar o servidor e as rotas da API.
# psutil: Biblioteca para acessar informações do sistema e processos (chamadas de sistema).
# sqlite3: Módulo para interagir com o banco de dados SQLite.
# time, threading: Para executar a coleta de métricas em intervalos regulares em segundo plano.
# os, json: Utilitários para manipulação de caminhos de arquivo e dados em formato JSON.
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import psutil
import sqlite3
import time
import threading
import os
import json

# --- Configuração Inicial do Flask ---
app = Flask(__name__)
# Chave secreta para gerenciar sessões de usuário (login). Em produção, use um valor mais seguro.
app.secret_key = "SEGREDO_SUPER_SEGURO"

# Define o caminho absoluto para o arquivo do banco de dados, garantindo que funcione em qualquer SO.
DB_PATH = os.path.join(os.path.dirname(__file__), "metrics.db")

# Simula um banco de dados de usuários para o sistema de login.
USUARIOS = {
    "admin": "admin123",
    "vinicius": "senha123"
}

# --- Funções do Banco de Dados e Coleta de Métricas ---


def init_db():
    """
    Inicializa o banco de dados SQLite.
    Cria a tabela 'metrics' se ela ainda não existir.
    Esta função cumpre a Etapa 3: Armazenamento de dados.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # A tabela armazena as métricas com um timestamp como chave primária.
    # O campo 'discos' armazena um JSON com o uso de cada partição.
    c.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            timestamp INTEGER PRIMARY KEY,
            cpu_percent REAL,
            ram_percent REAL,
            discos TEXT,
            net_sent INTEGER,
            net_recv INTEGER,
            net_sent_per_sec INTEGER,
            net_recv_per_sec INTEGER
        )
    ''')
    conn.commit()
    conn.close()


# Variável global para armazenar a última leitura de rede e calcular a taxa por segundo.
_last_net = None


def coletar_metricas():
    """
    Coleta as métricas de desempenho do sistema operacional local.
    Utiliza a biblioteca psutil, que abstrai as chamadas de sistema específicas
    de cada SO (Linux, Windows, etc.).
    Esta função cumpre a Etapa 1: Coleta de métricas locais.
    """
    global _last_net

    # 1. Coleta de uso de Disco
    disco_metrics = {}
    # Itera sobre todas as partições de disco montadas.
    for part in psutil.disk_partitions():
        try:
            # psutil.disk_usage() retorna estatísticas de uso do disco.
            uso = psutil.disk_usage(part.mountpoint).percent
            disco_metrics[part.device] = {
                'percent': uso,
                'mountpoint': part.mountpoint
            }
        except PermissionError:
            # Ignora discos que o usuário atual não tem permissão para ler.
            continue

    # 2. Coleta de uso de CPU e RAM
    # psutil.cpu_percent() mede o uso da CPU em um intervalo.
    cpu_percent = psutil.cpu_percent(interval=0.5)
    # psutil.virtual_memory() retorna o uso da memória RAM.
    ram_percent = psutil.virtual_memory().percent

    # 3. Coleta de dados de Rede
    net = psutil.net_io_counters()
    timestamp = int(time.time())
    net_sent = net.bytes_sent
    net_recv = net.bytes_recv

    # Calcula a taxa de rede (bytes por segundo) desde a última coleta.
    # Isso é importante para exibir dados de "velocidade" em vez de acumulados.
    if _last_net is not None:
        duration = timestamp - _last_net['timestamp']
        if duration > 0:
            net_sent_per_sec = (net_sent - _last_net['net_sent']) // duration
            net_recv_per_sec = (net_recv - _last_net['net_recv']) // duration
        else:
            net_sent_per_sec = 0
            net_recv_per_sec = 0
    else:
        # Na primeira execução, a taxa é zero.
        net_sent_per_sec = 0
        net_recv_per_sec = 0

    # Atualiza a última leitura de rede para o próximo cálculo.
    _last_net = {
        'timestamp': timestamp,
        'net_sent': net_sent,
        'net_recv': net_recv
    }

    # Retorna um dicionário com todas as métricas coletadas.
    return {
        'cpu_percent': cpu_percent,
        'ram_percent': ram_percent,
        'discos': disco_metrics,
        'net_sent': net_sent,
        'net_recv': net_recv,
        'net_sent_per_sec': net_sent_per_sec,
        'net_recv_per_sec': net_recv_per_sec,
        'timestamp': timestamp
    }


def salvar_no_banco(metrics):
    """
    Salva um conjunto de métricas no banco de dados SQLite.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # 'INSERT OR REPLACE' atualiza o registro se o timestamp já existir.
    c.execute('''
        INSERT OR REPLACE INTO metrics (timestamp, cpu_percent, ram_percent, discos, net_sent, net_recv, net_sent_per_sec, net_recv_per_sec)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        metrics['timestamp'], metrics['cpu_percent'], metrics['ram_percent'],
        json.dumps(metrics['discos']
                   ), metrics['net_sent'], metrics['net_recv'],
        metrics['net_sent_per_sec'], metrics['net_recv_per_sec']
    ))
    conn.commit()
    conn.close()


def coleta_periodica():
    """
    Função executada em uma thread separada para coletar e salvar
    métricas periodicamente, sem bloquear o servidor web.
    Isso corresponde ao "Exemplo de Fluxo" do projeto.
    """
    while True:
        metrics = coletar_metricas()
        salvar_no_banco(metrics)
        # Pausa por 5 segundos antes da próxima coleta.
        time.sleep(5)

# --- Rotas da Aplicação Web (Views e API) ---


@app.route('/', methods=['GET'])
def root():
    """ Rota raiz, redireciona para a página de login. """
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Página de login. Verifica as credenciais e cria uma sessão. """
    erro = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            erro = "Usuário ou senha inválidos."
    return render_template('login.html', erro=erro)


@app.route('/logout')
def logout():
    """ Encerra a sessão do usuário. """
    session.pop('usuario', None)
    return redirect(url_for('login'))


def login_required(f):
    """
    Decorator para proteger rotas que exigem autenticação.
    Verifica se o usuário está na sessão antes de permitir o acesso.
    """
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# --- Rotas Protegidas (Dashboard e Páginas) ---


@app.route('/dashboard')
@login_required
def dashboard():
    """ Rota principal do dashboard, que exibe os gráficos em tempo real. """
    return render_template('index.html', usuario=session['usuario'])


@app.route('/historico')
@login_required
def historico():
    """ Página para visualização de dados históricos. """
    return render_template('historico.html', usuario=session['usuario'])


@app.route('/config')
@login_required
def config():
    """ Página de configurações (ex: definir limites de alerta). """
    return render_template('config.html', usuario=session['usuario'])


@app.route('/sobre')
@login_required
def sobre():
    """ Página com informações sobre o projeto. """
    return render_template('sobre.html', usuario=session['usuario'])

# --- API RESTful para o Frontend ---
# Estas rotas cumprem a Etapa 2: Criação de API RESTful.


@app.route('/metrics', methods=['GET'])
@login_required
def metrics():
    """
    Endpoint da API que retorna a métrica mais recente.
    Usado pelo frontend para atualizar os gráficos em tempo real.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Busca o último registro inserido no banco.
    c.execute('SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    if row:
        m = {
            'timestamp': row[0],
            'cpu_percent': row[1],
            'ram_percent': row[2],
            'discos': json.loads(row[3]),  # Desserializa o JSON do disco
            'net_sent': row[4],
            'net_recv': row[5],
            'net_sent_per_sec': row[6],
            'net_recv_per_sec': row[7]
        }
    else:
        # Retorna vazio se o banco ainda não tiver dados.
        m = {}
    return jsonify(m)


@app.route('/history', methods=['GET'])
@login_required
def history():
    """
    Endpoint da API que retorna todo o histórico de métricas.
    Usado pela página de histórico para montar gráficos de longo prazo.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Retorna todos os dados em ordem cronológica para montar os gráficos corretamente.
    c.execute('SELECT * FROM metrics ORDER BY timestamp ASC')
    data = c.fetchall()
    conn.close()
    # Constrói uma lista de dicionários para ser facilmente consumida pelo JavaScript.
    return jsonify([
        {
            'timestamp': row[0],
            'cpu_percent': row[1],
            'ram_percent': row[2],
            'discos': json.loads(row[3]),
            'net_sent': row[4],
            'net_recv': row[5],
            'net_sent_per_sec': row[6],
            'net_recv_per_sec': row[7]
        }
        for row in data
    ])


# --- Ponto de Entrada da Aplicação ---
if __name__ == '__main__':
    # 1. Garante que o banco de dados e a tabela existam.
    init_db()

    # 2. Cria e inicia a thread de coleta de métricas em background.
    # 'daemon=True' garante que a thread será encerrada quando o programa principal terminar.
    t = threading.Thread(target=coleta_periodica, daemon=True)
    t.start()

    # 3. Inicia o servidor web Flask.
    # 'debug=True' ativa o modo de depuração para facilitar o desenvolvimento.
    app.run(debug=True)
