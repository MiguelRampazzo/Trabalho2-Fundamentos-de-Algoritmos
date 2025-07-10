from dataclasses import dataclass
from enum import Enum
import sys


class Medalha(Enum):
    BRONZE = '3'
    PRATA = '2'
    OURO = '1'


@dataclass
class Pais:
    nome: str
    quant_bronze: int = 0
    quant_prata: int = 0
    quant_ouro: int = 0
    quant_total: int = 0
    generos: list = None 


def main():
    if len(sys.argv) < 2:
        print('Nenhum nome de arquivo informado.')
        sys.exit(1)

    if len(sys.argv) > 2:
        print('Muitos parâmetros. Informe apenas um nome de arquivo.')
        sys.exit(1)

    tabela = le_arquivo(sys.argv[1])
    tabela_filtrada = filtro_tabela(tabela)
    tabela_enumerada = quadro(tabela_filtrada)
    quadro_organizado = ordena(tabela_enumerada)
    paises_genero = filtrar_paises_genero_unico(tabela_enumerada)
    exibir_quadro(quadro_organizado) 
    exibir_paises_formatado(paises_genero)
    

def le_arquivo(nome: str) -> list[list[str]]:
    '''
    Lê o conteúdo do arquivo *nome* e devolve uma lista onde cada elemento é
    uma lista com os valores das colunas de uma linha (valores separados por
    vírgula). A primeira linha do arquivo, que deve conter o nome das
    colunas, é descartado.

    Por exemplo, se o conteúdo do arquivo for
    tipo,cor,ano
    carro,verde,2010
    moto,branca,1995

    a resposta produzida é
    [['carro', 'verde', '2010'], ['moto', 'branca', '1995']]
    '''
    try:
        with open(nome) as f:
            tabela = []
            linhas = f.readlines()
            for i in range(1, len(linhas)):
                tabela.append(linhas[i].split(','))
            return tabela
    except IOError as e:
        print(f'Erro na leitura do arquivo "{nome}": {e.errno} - {e.strerror}.');
        sys.exit(1)

def filtro_tabela(tabela: list[list[str]]) -> list[list[str]]:
    '''
    Filtra a tabela para manter apenas código de medalha, nome do país e gênero.

    >>> tabela = [['1', 'BRA', 'M'], ['2', 'USA', 'F'], ['3', 'BRA', 'M'], ['1', 'FRA', 'M']]
    >>> filtro_tabela(tabela)
    [('1', 'BRA', 'M'), ('2', USA', 'F'), ('3', BRA', 'M'), ('1', FRA', 'M')]
    '''
    nova_tabela = []
    for item in tabela:
        filtra = item[1], item[4], item[5]
        nova_tabela.append(filtra)
    return nova_tabela

def quadro(tabela: list[list[str]]) -> list[Pais]:
    '''
    Constrói uma lista de objetos do class `Pais` a partir da tabela filtrada.

    >>> tabela = [['1', 'BRA', 'M'], ['2', 'USA', 'F'], ['3', 'BRA', 'M'], ['1', 'FRA', 'M']]
    >>> quadro(tabela)
    [Pais(nome='BRA', quant_bronze=1, quant_prata=0, quant_ouro=1, quant_total=2, generos=['M']), Pais(nome='USA', quant_bronze=0, quant_prata=1, quant_ouro=0, quant_total=1, generos=['F']), Pais(nome='FRA', quant_bronze=0, quant_prata=0, quant_ouro=1, quant_total=1, generos=['M'])]
    '''
    paises_list = []

    for linha in tabela:
        medal_code = linha[0]
        nome_pais = linha[1]
        genero_atleta = linha[2]  

        pais_encontrado = False
        for item in paises_list:
            if item.nome == nome_pais:
                pais_encontrado = True
                if medal_code == Medalha.BRONZE.value:
                    item.quant_bronze += 1
                elif medal_code == Medalha.PRATA.value:
                    item.quant_prata += 1
                elif medal_code == Medalha.OURO.value:
                    item.quant_ouro += 1
                item.quant_total = item.quant_bronze + item.quant_prata + item.quant_ouro

                if item.generos is None:
                    item.generos = []
                if genero_atleta not in item.generos:
                    item.generos.append(genero_atleta)
                break  

       
        if not pais_encontrado:
            novo_pais = Pais(nome=nome_pais, generos=[genero_atleta])
            if medal_code == Medalha.BRONZE.value:
                novo_pais.quant_bronze = 1
            elif medal_code == Medalha.PRATA.value:
                novo_pais.quant_prata = 1
            elif medal_code == Medalha.OURO.value:
                novo_pais.quant_ouro = 1
            novo_pais.quant_total = novo_pais.quant_bronze + novo_pais.quant_prata + novo_pais.quant_ouro
            paises_list.append(novo_pais)
    return paises_list

def ordena(paises: list[Pais]) -> list[Pais]:
    """
    Ordena o quadro de medalhas de acordo com a quantidade de medalhas de ouro , prata e bronze.

    >>> paises = [Pais('BRA', 0, 0, 1, 1), Pais('USA', 0, 1, 0, 1), Pais('FRA', 0, 0, 1, 1)]
    >>> ordena(paises)
    [Pais(nome='BRA', quant_bronze=0, quant_prata=0, quant_ouro=1, quant_total=1, generos=None), Pais(nome='FRA', quant_bronze=0, quant_prata=0, quant_ouro=1, quant_total=1, generos=None), Pais(nome='USA', quant_bronze=0, quant_prata=1, quant_ouro=0, quant_total=1, generos=None)]
    """
    for i in range(1, len(paises)):
        chave = paises[i]
        j = i - 1

        while j >= 0:
            if paises[j].quant_ouro < chave.quant_ouro:
                paises[j + 1] = paises[j]   
            elif paises[j].quant_ouro == chave.quant_ouro:
                if paises[j].quant_prata < chave.quant_prata:
                    paises[j + 1] = paises[j]
                elif paises[j].quant_prata == chave.quant_prata:
                    if paises[j].quant_bronze < chave.quant_bronze:
                        paises[j + 1] = paises[j]
                    else:
                        break
                else:
                    break
            else:
                break
            j -= 1
        paises[j + 1] = chave
    return paises

def exibir_quadro(paises: list[Pais]):
    '''
    Exibe o quadro de classificação dos países.
    '''
    print(f'{"País":<15} {"Ouro":<5} {"Prata":<5} {"Bronze":<6} {"Total":<5}')
    for pais in paises:
        print(f'{pais.nome:<15} {pais.quant_ouro:<5} {pais.quant_prata:<5} {pais.quant_bronze:<6} {pais.quant_total:<5}')

def filtrar_paises_genero_unico(paises: list[Pais], index: int = 0) -> list[Pais]:
    '''
    Retorna uma lista de países que têm apenas atletas de um único gênero premiados.
    >>> paises = [Pais(nome='BOT', quant_bronze=0, quant_prata=1, quant_ouro=1, quant_total=2, generos=['M']),Pais(nome='QAT', quant_bronze=1, quant_prata=0, quant_ouro=0, quant_total=1, generos=['M']), Pais(nome='BEL', quant_bronze=5, quant_prata=1, quant_ouro=2, quant_total=8, generos=['M', 'W'])]
    >>> filtrar_paises_genero_unico(paises)
    [Pais(nome='BOT', quant_bronze=0, quant_prata=1, quant_ouro=1, quant_total=2, generos=['M']), Pais(nome='QAT', quant_bronze=1, quant_prata=0, quant_ouro=0, quant_total=1, generos=['M'])]
    '''
    if index >= len(paises):
        return []
    
    if len(paises[index].generos) == 1:
        return [paises[index]] + filtrar_paises_genero_unico(paises, index + 1)
    
    return filtrar_paises_genero_unico(paises, index + 1)

def exibir_paises_formatado(paises: list[Pais]):
    '''
    Exibe os países que tiveram apenas atletas de um único gênero premiados
    '''
    print("Países com atletas de um único gênero premiados:")
    for pais in paises:
        print(f'{pais.nome:<15}')  


if __name__ == '__main__':
    main()

