import streamlit as st
import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('equipamentos.db')
c = conn.cursor()


# Função para criar as tabelas
def criar_tabelas():
    c.execute('''CREATE TABLE IF NOT EXISTS tipo_equipamento
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS local
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cod_sistema TEXT NOT NULL,
                observacao TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS equipamento
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                numero_serie TEXT NOT NULL,
                tipo_equipamento_id INTEGER,
                local_id INTEGER,
                observacao TEXT,
                FOREIGN KEY(tipo_equipamento_id) REFERENCES tipo_equipamento(id),
                FOREIGN KEY(local_id) REFERENCES local(id))''')

    conn.commit()


# Função para inserção em cada tabela
def inserir_tipo_equipamento(nome, descricao):
    c.execute('INSERT INTO tipo_equipamento (nome, descricao) VALUES (?, ?)', (nome, descricao))
    conn.commit()


def inserir_local(nome, cod_sistema, observacao):
    c.execute('INSERT INTO local (nome, cod_sistema, observacao) VALUES (?, ?, ?)', (nome, cod_sistema, observacao))
    conn.commit()


def inserir_equipamento(nome, numero_serie, tipo_equipamento_id, local_id, observacao):
    c.execute(
        'INSERT INTO equipamento (nome, numero_serie, tipo_equipamento_id, local_id, observacao) VALUES (?, ?, ?, ?, ?)',
        (nome, numero_serie, tipo_equipamento_id, local_id, observacao))
    conn.commit()


# Função para listar dados das tabelas
def listar_tipo_equipamento():
    c.execute('SELECT * FROM tipo_equipamento')
    return c.fetchall()


def listar_local():
    c.execute('SELECT * FROM local')
    return c.fetchall()


def listar_equipamento():
    c.execute(
        'SELECT e.id, e.nome, e.numero_serie, t.nome as tipo_nome, l.nome as local_nome, e.observacao FROM equipamento e JOIN tipo_equipamento t ON e.tipo_equipamento_id = t.id JOIN local l ON e.local_id = l.id')
    return c.fetchall()


# Função para atualizar dados
def atualizar_tipo_equipamento(id, nome, descricao):
    c.execute('UPDATE tipo_equipamento SET nome = ?, descricao = ? WHERE id = ?', (nome, descricao, id))
    conn.commit()


def atualizar_local(id, nome, cod_sistema, observacao):
    c.execute('UPDATE local SET nome = ?, cod_sistema = ?, observacao = ? WHERE id = ?',
              (nome, cod_sistema, observacao, id))
    conn.commit()


def atualizar_equipamento(id, nome, numero_serie, tipo_equipamento_id, local_id, observacao):
    c.execute(
        'UPDATE equipamento SET nome = ?, numero_serie = ?, tipo_equipamento_id = ?, local_id = ?, observacao = ? WHERE id = ?',
        (nome, numero_serie, tipo_equipamento_id, local_id, observacao, id))
    conn.commit()


# Função para deletar dados
def deletar_tipo_equipamento(id):
    c.execute('DELETE FROM tipo_equipamento WHERE id = ?', (id,))
    conn.commit()


def deletar_local(id):
    c.execute('DELETE FROM local WHERE id = ?', (id,))
    conn.commit()


def deletar_equipamento(id):
    c.execute('DELETE FROM equipamento WHERE id = ?', (id,))
    conn.commit()


# Função para estilizar as listas com cores alternadas
def estilo_tabela(lista_dados, headers, editar_callback, deletar_callback):
    st.markdown("""
        <style>
        .tabela-dados {
            width: 100%;
            border-collapse: collapse;
        }
        .tabela-dados th, .tabela-dados td {
            padding: 10px;
            text-align: left;
        }
        .tabela-dados tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .tabela-dados tr:nth-child(odd) {
            background-color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)

    # Exibe cabeçalhos
    tabela_html = "<table class='tabela-dados'><tr>"
    for header in headers:
        tabela_html += f"<th>{header}</th>"
    tabela_html += "<th>Ações</th></tr>"

    # Exibe dados com cores alternadas
    for linha in lista_dados:
        tabela_html += "<tr>"
        for valor in linha:
            tabela_html += f"<td>{valor}</td>"
        tabela_html += f"""
            <td>
                <button onclick="editar({linha[0]})">Editar</button>
                <button onclick="deletar({linha[0]})">Excluir</button>
            </td>
        </tr>"""

    tabela_html += "</table>"
    st.markdown(tabela_html, unsafe_allow_html=True)


# Criar tabelas no banco
criar_tabelas()

# Barra lateral para o menu
menu = st.sidebar.selectbox("Menu", ["Tipos de Equipamento", "Locais", "Equipamentos"])

# CRUD para Tipos de Equipamento
if menu == "Tipos de Equipamento":
    st.title("Tipos de Equipamento")

    # Formulário de inserção
    with st.form(key='inserir_tipo_equipamento'):
        nome = st.text_input('Nome')
        descricao = st.text_area('Descrição')
        submit_button = st.form_submit_button('Inserir Tipo de Equipamento')

        if submit_button:
            inserir_tipo_equipamento(nome, descricao)
            st.success('Tipo de Equipamento inserido com sucesso!')

    # Listar tipos de equipamento com estilização
    tipos = listar_tipo_equipamento()
    st.subheader("Tipos de Equipamento Cadastrados")
    estilo_tabela(tipos, ["ID", "Nome", "Descrição"], atualizar_tipo_equipamento, deletar_tipo_equipamento)

# CRUD para Locais
elif menu == "Locais":
    st.title("Locais")

    # Formulário de inserção
    with st.form(key='inserir_local'):
        nome = st.text_input('Nome')
        cod_sistema = st.text_input('Código do Sistema')
        observacao = st.text_area('Observação')
        submit_button = st.form_submit_button('Inserir Local')

        if submit_button:
            inserir_local(nome, cod_sistema, observacao)
            st.success('Local inserido com sucesso!')

    # Listar locais com estilização
    locais = listar_local()
    st.subheader("Locais Cadastrados")
    estilo_tabela(locais, ["ID", "Nome", "Código do Sistema", "Observação"], atualizar_local, deletar_local)

# CRUD para Equipamentos
elif menu == "Equipamentos":
    st.title("Equipamentos")

    # Formulário de inserção
    with st.form(key='inserir_equipamento'):
        nome = st.text_input('Nome do Equipamento')
        numero_serie = st.text_input('Número de Série')

        # Selecionar tipo de equipamento e local como chaves estrangeiras
        tipos = listar_tipo_equipamento()
        locais = listar_local()

        tipo_equipamento_id = st.selectbox('Tipo de Equipamento', [t[0] for t in tipos])
        local_id = st.selectbox('Local', [l[0] for l in locais])

        observacao = st.text_area('Observação')
        submit_button = st.form_submit_button('Inserir Equipamento')

        if submit_button:
            inserir_equipamento(nome, numero_serie, tipo_equipamento_id, local_id, observacao)
            st.success('Equipamento inserido com sucesso!')

    # Listar equipamentos com estilização
    equipamentos = listar_equipamento()
    st.subheader("Equipamentos Cadastrados")
    estilo_tabela(equipamentos, ["ID", "Nome", "Número de Série", "Tipo de Equipamento", "Local", "Observação"],
                  atualizar_equipamento, deletar_equipamento)
