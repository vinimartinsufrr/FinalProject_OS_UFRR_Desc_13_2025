# Nero - Dashboard de Monitoramento de Sistema

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

Nero é um dashboard web para o monitoramento de recursos de sistema operacional em tempo real. Desenvolvido como projeto para a disciplina de Sistemas Operacionais da **Universidade Federal de Roraima (UFRR)**, a aplicação oferece uma interface moderna e intuitiva para visualizar métricas vitais como uso de CPU, RAM, disco e rede.

---

### Preview do Dashboard
*(Sugestão: Adicione aqui um screenshot da tela principal do seu dashboard)*
![Dashboard Preview](https-placeholder-for-your-image.png)

---

## ✨ Funcionalidades

-   **Dashboard em Tempo Real:** Gráficos e cartões que exibem o uso de CPU, memória RAM e tráfego de rede, atualizados automaticamente.
-   **Monitoramento de Disco:** Visualização do espaço utilizado para todos os discos montados no sistema.
-   **Histórico Detalhado:** Uma página dedicada ao histórico de métricas, com gráficos e uma tabela detalhada que pode ser filtrada por data e hora.
-   **Alertas Configuráveis:** Sistema de alerta visual que notifica o usuário quando o uso de CPU ultrapassa um limite definido na página de configurações.
-   **Configurações Personalizadas:** Permite ao usuário escolher quais discos devem ser exibidos no dashboard principal.
-   **Interface Responsiva:** Design limpo e adaptável a diferentes tamanhos de tela.
-   **Sistema de Login:** Uma tela de login estilizada para proteger o acesso ao dashboard.

---

## 🛠️ Tecnologias Utilizadas

-   **Backend:**
    -   **Python:** Linguagem principal para a lógica do servidor.
    -   **Flask:** Micro-framework web para gerenciar as rotas, servir as páginas e fornecer os dados das métricas.
    -   **psutil:** Biblioteca para acessar informações e métricas do sistema operacional.
-   **Frontend:**
    -   **HTML5:** Estrutura das páginas.
    -   **CSS3:** Estilização e design responsivo.
    -   **JavaScript (Vanilla):** Manipulação dinâmica do DOM, requisições (Fetch API) e atualização dos dados da interface.
    -   **Chart.js:** Biblioteca para a criação dos gráficos interativos.
-   **Templates:**
    -   **Jinja2:** Motor de templates do Flask, usado para renderizar as páginas HTML dinamicamente.

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar o Nero em sua máquina local.

**1. Clone o Repositório**
```bash
git clone https://github.com/vinimartinsufrr/nero-dashboard.git # (Sugestão de nome para o repo)
cd nero-dashboard
```

**2. Crie e Ative um Ambiente Virtual (Recomendado)**
```bash
# Para Windows
python -m venv venv
.\venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as Dependências**

As dependências estão listadas no arquivo `requirements.txt`. Instale-as com o pip:
```bash
pip install -r requirements.txt
```

**4. Execute a Aplicação**

Supondo que seu arquivo principal Python se chame `app.py`, execute o comando:
```bash
flask run
# ou
python app.py
```

**5. Acesse no Navegador**

Abra seu navegador e acesse [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 📂 Estrutura do Projeto

```
.
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
│       ├── logo-nero.png
│       └── login-bg.png
├── templates/
│   ├── base.html         # Template base com a estrutura principal
│   ├── login.html        # Página de login
│   ├── index.html        # Dashboard principal
│   ├── historico.html    # Página de histórico
│   ├── config.html       # Página de configurações
│   └── sobre.html        # Página "Sobre o Projeto"
├── app.py                # Lógica do backend com Flask (arquivo principal)
└── requirements.txt      # Lista de dependências Python
```

---

## 👥 Créditos

Este projeto foi desenvolvido por:

-   **Desenvolvedores:** Vinícius Martins ([@vinimartinsufrr](https://github.com/vinimartinsufrr)) e Jasmim Sabini ([@jasmimsabini](https://github.com/jasmimsabini)).
-   **Professor:** Hebert Rocha

**Universidade Federal de Roraima (UFRR) — 2025**
