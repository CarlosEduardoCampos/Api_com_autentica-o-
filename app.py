from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from models import Pessoas, Atividades, Usuarios

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

#USER = {
#    'carlos': '123'
#}
#
#@auth.verify_password
#def verificacao(login, senha):
#    print('Validação do user')
#    print(USER.get(login) == senha)
#
#    if not (login, senha):
#        return False
#
#    return USER.get(login) == senha

@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False

    return Usuarios.query.filter_by(login=login, senha=senha).first()


class Usuario(Resource):
    # Editar um usuario
    @auth.login_required
    def put(self, id):
        user = Usuarios.query.filter_by(id=id).first()
        dados = request.json

        if user.nivel != dados['nivel']:
            user.nivel = dados['nivel']

        elif user.login != dados['login']:
            user.login = dados['login']

        elif user.senha != dados['senha']:
            user.senha = dados['senha']

        user.save()

        response = {
            'id': user.id,
            'nivel': user.nivel,
            'login': user.login,
            'senha': user.senha,
            'pessa_id': user.pessoa.id
        }

        return response

    # Excluir um usuario
    @auth.login_required
    def delete(self, id):
        user = Usuarios.query.filter_by(id=id).first()
        mensagem = f'{user.login} foi deletado(a) com sucesso'
        user.delete()

        return {
            "status": 'sucesso',
            "mensagem": mensagem
        }


class ListaUsuarios(Resource):
    # Lista todos os usuarios cadastrados
    @auth.login_required
    def get(self):
        user = Usuarios.query.all()

        try:
            response = [{
                "id": i.id,
                "nivel": i.nivel,
                "login": i.login,
                "senha": i.senha
            } for i in user]

        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa não encontrada'
            }

        return response

    # Cadastra um novo usuario no banco de dados
    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(id=dados['pessoa_id']).first()

        user = Usuarios(
            nivel=dados['nivel'],
            login=dados['login'],
            senha=dados['senha'],
            pessoa=pessoa
        )
        user.save()

        return {
            "id": user.id,
            "nivel": user.nivel,
            "login": user.login,
            "senha": user.senha,
        }


class Pessoa(Resource):
    # Busca uma unica pessoa no banco de dados a partir do id
    @auth.login_required
    def get(self, id):
        pessoa = Pessoas.query.filter_by(id=id).first()

        try:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }

        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa não encontrada'
            }

        return response

    # Edita o nome ou idade da pessoa que possua o id passado
    @auth.login_required
    def put(self, id):

        pessoa = Pessoas.query.filter_by(id=id).first()
        dados = request.json

        if 'nome' in dados:
            pessoa.nome = dados['nome']

        elif 'idade' in dados:
            pessoa.idade = dados['idade']

        pessoa.save()

        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }

        return response

    # Apaga do banco de dados a pessoa que possua o id passado
    @auth.login_required
    def delete(self, id):
        pessoa = Pessoas.query.filter_by(id=id).first()
        mensagem = f'{pessoa.nome} foi deletado(a) com sucesso'
        pessoa.delete()

        return {
            "status": 'sucesso',
            "mensagem": mensagem
        }


class ListaPessoas(Resource):
    # Devolve uma lista em json com os dados de todas as pessoa cadastradas
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()

        response = [{
            'id': i.id,
            'nome': i.nome,
            'idade': i.idade
        } for i in pessoas]

        return response

    # Faz o cadastro de uma nova pessoa no banco de dados
    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()

        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }

        return response


class Atividade(Resource):
    # Apagda do baco de dados uma tarefa idetificada pelo id
    @auth.login_required
    def delete(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        mensagem = f'{atividade.titulo} foi deletado(a) com sucesso'
        atividade.delete()

        return {
            "status": 'sucesso',
            "mensagem": mensagem
        }


class ListaAtividades(Resource):
    # Lista todas as atividades no formato json
    @auth.login_required
    def get(self):
        atividades = Atividades.query.all()

        response = [{
            'id': i.id,
            'titulo': i.titulo,
            'pessoa_id': i.pessoa_id
        } for i in atividades]

        return response

    # Cadastra uma nova atividade no banco de dados
    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(id=dados['pessoa_id']).first()
        atividade = Atividades(titulo=dados['titulo'], pessoa=pessoa)
        atividade.save()

        response = {
            'pessoa_nome': atividade.pessoa.nome,
            'titulo': atividade.titulo,
            'id': atividade.id
        }

        return response

    # Apagda do baco de dados uma tarefa idetificada pelo id
    @auth.login_required
    def delete(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        mensagem = f'{atividade.titulo} foi deletado(a) com sucesso'
        atividade.delete()

        return {
            "status": 'sucesso',
            "mensagem": mensagem
        }


# Rotas para Usuarios
api.add_resource(Usuario, '/user/<int:id>/')
api.add_resource(ListaUsuarios, '/user/')

# Rotas para PESSOAS
api.add_resource(Pessoa, '/pessoa/<int:id>/')
api.add_resource(ListaPessoas, '/pessoa/')

# Rotas para ATIVIDADES
api.add_resource(ListaAtividades, '/atividades/')
api.add_resource(Atividade, '/atividade/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True)
