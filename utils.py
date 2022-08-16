from models import Pessoas, db_session


def create_pessoas():
    pessoa = Pessoas(nome=str(input('Nome: ')), idade=int(input('Idade: ')))
    pessoa.save()


def read_pessoas():
    pessoas = Pessoas.query.all()

    for i in pessoas:
        print(f'....... Pessoa {i.id}º .......')
        print(f'\t Nome -> {i.nome}')
        print(f'\t Idade -> {i.idade} \n')


def read_nome_pessoa(nome):
    pessoa = Pessoas.query.filter_by(nome=nome).first()

    print(f'....... Pessoa {pessoa.id}º .......')
    print(f'\t Nome -> {pessoa.nome}')
    print(f'\t Idade -> {pessoa.idade} \n')


def read_id_pessoa(id):
    pessoa = Pessoas.query.filter_by(id=id).first()

    print(f'....... Pessoa {pessoa.id}º .......')
    print(f'\t Nome -> {pessoa.nome}')
    print(f'\t Idade -> {pessoa.idade} \n')


def update_pessoas(id):
    pessoa = Pessoas.query.filter_by(id=id).first()
    pessoa.idade = int(input('Idade: '))
    pessoa.save()


def delete_pessoas(id):
    pessoa = Pessoas.query.filter_by(id=id).first()
    pessoa.delete()


if __name__ == '__main__':
    """ 
        create_pessoas()
        read_pessoas()
        read_nome_pessoa(str(input('Nome: ')))
        read_id_pessoa(int(input('ID Pessoa: ')))
        update_pessoas(int(input('ID Pessoa: ')))
        delete_pessoas(int(input('ID Pessoa: ')))
    """

    read_pessoas()

