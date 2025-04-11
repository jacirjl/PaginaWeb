from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para criar a tabela no banco de dados (se não existir)
def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            endereco TEXT,
            data_nascimento TEXT,
            salario REAL
        )
    ''')
    conn.commit()
    conn.close()

# Rota principal (listagem e formulário)
@app.route('/', methods=['GET', 'POST'])
def index():
    create_table()  # Garante que a tabela exista
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        data_nascimento = request.form['data_nascimento']
        salario = request.form['salario']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pessoas (nome, endereco, data_nascimento, salario) VALUES (?, ?, ?, ?)", (nome, endereco, data_nascimento, salario))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas")
    pessoas = cursor.fetchall()
    conn.close()
    return render_template('index.html', pessoas=pessoas)

# Rota para editar os dados
@app.route('/edit/<int:pessoa_id>', methods=['GET', 'POST'])
def edit(pessoa_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        data_nascimento = request.form['data_nascimento']
        salario = request.form['salario']

        cursor.execute("UPDATE pessoas SET nome=?, endereco=?, data_nascimento=?, salario=? WHERE id=?", (nome, endereco, data_nascimento, salario, pessoa_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM pessoas WHERE id=?", (pessoa_id,))
    pessoa = cursor.fetchone()
    conn.close()
    return render_template('edit.html', pessoa=pessoa)

# Rota para deletar os dados
@app.route('/delete/<int:pessoa_id>', methods=['POST'])
def delete(pessoa_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pessoas WHERE id=?", (pessoa_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # app.run()
    # app.run(debug=True)
    # app.run(debug=True)
    app.run(debug=True)