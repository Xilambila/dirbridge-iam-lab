from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_FORM = '''
    <h2>Formulário de Criação de Usuário</h2>
    <form method="post">
        ID Colaborador: <input name="id_colaborador"><br><br>
        Nome: <input name="nome"><br><br>
        Sobrenome: <input name="sobrenome"><br><br>
        Criar email? <input type="checkbox" name="criar_email"><br><br>
        <input type="submit" value="Criar Usuário">
    </form>
'''

@app.route('/', methods=['GET', 'POST'])
def criar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        id_colab = request.form['id_colaborador']
        criar_email = 'criar_email' in request.form

        nome_usuario = f"{nome.lower()}.{sobrenome.lower()}"
        email = f"{nome_usuario}@dominioprincipal.com.br"
        senha = f"{nome[0]}{sobrenome[0]}{id_colab}"

        return f"""
            <h3>Usuário Processado:</h3>
            Nome: {nome} {sobrenome}<br>
            ID: {id_colab}<br>
            Nome de Usuário: {nome_usuario}<br>
            Email: {email if criar_email else "NÃO CRIAR"}<br>
            Senha: {senha}<br>
            <hr>
            <code>Powershell script gerado aqui futuramente</code>
            <br><br>
            <a href="/">← Voltar</a>
        """

    return render_template_string(HTML_FORM)
