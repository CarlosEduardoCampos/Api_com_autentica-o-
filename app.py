from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades

app = Flask(__name__)
api = Api(app)


class Pessoa(Resource):
    # Busca uma unica pessoa no banco de dados a partir do id
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
    def get(self):
        pessoas = Pessoas.query.all()

        response = [{
            'id': i.id,
            'nome': i.nome,
            'idade': i.idade
        } for i in pessoas]

        return response

    # Faz o cadastro de uma nova pessoa no banco de dados
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
    def get(self):
        atividades = Atividades.query.all()

        response = [{
            'id': i.id,
            'titulo': i.titulo,
            'pessoa_id': i.pessoa_id
        } for i in atividades]

        return response

    # Cadastra uma nova atividade no banco de dados
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(id=dados['pessoa_id']).first()
        atividade = Atividades(titulo=dados['titulo'], pessoa=pessoa)
        atividade.save()

        response = {
            'pessoa_id': atividade.pessoa.nome,
            'titulo': atividade.titulo,
            'id': atividade.id
        }

        return response

    # Apagda do baco de dados uma tarefa idetificada pelo id
    def delete(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        mensagem = f'{atividade.titulo} foi deletado(a) com sucesso'
        atividade.delete()

        return {
            "status": 'sucesso',
            "mensagem": mensagem
        }


api.add_resource(Pessoa, '/pessoa/<int:id>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')
api.add_resource(Atividade, '/atividade/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True)
