# Autor: Francisco Thiesen, Email: fthiesen@arpexcapital.com.br/franciscogthiesen@gmail.com
'''
Essa eh uma v0 do parser de multichain.
Coisas que sao essenciais, mas que nao estou me preocupando nessa versao
- Tratamento de erro/excecoes
- Recuperacao de dados Off-chain
- Testes unitarios / Testes de integracao 
- Teste de conexao com a chain
- Criar requirements.txt 
'''

from Savoir import Savoir
import json
import os

rpcuser = 'multichainrpc'
rpcpasswd = '2VNj2nnLGRH9fS8nKa6L8ZUEGsNKv5xv1UwANtykdxa6'
rpchost = 'localhost'
rpcport = '4780'
chainname = 'chain4'

api = Savoir( rpcuser, rpcpasswd, rpchost, rpcport, chainname )

# Acho que seria interessante fazer uma funcao pra testar a conexao com a chain!

def get_last_processed_block_height():
    last_processed_block = -1
    if os.path.isfile('./blocks/block_metadata') == True:
        f = open("./blocks/block_metadata", "r")
        # o arquivo blockmetadata possui todos os blocos completamente processados pelo parser, separados por espaco
        '''
        A organizacao dos arquivos de block_metadata pode ser repensada.
        Podemos colocar todos os blocos processados numa determinada execucao do parser em uma unica linha/varias linhas,
        podemos tambem armazenar apenas um inteiro que eh o do ultimo bloco processador ate agora. Nao fiz
        isso porque nao queria que tivessemos que deletar o numero anterior do arquivo de blockmetadata.
        Achei mais interessante que o arquivo fosse append-only.
        '''
        processed_blocks = []
        for line in f:
            processed_blocks.append( [ int(x) for x in line.split() ] )
        
        print( processed_blocks )
        f.close()
        
        if len(processed_blocks) > 0:
            last_list = processed_blocks[-1]
            last_processed_block = last_list[-1]
    
    return last_processed_block


def get_chain_height():
    chain_metadata = api.getinfo()
    
    try:
        last_block_index = chain_metadata[u'blocks']
    except Exception as e:
        print(e)
        return -1
    
    return last_block_index


def is_height_valid( height ):
    last_block_index = get_chain_height()
    if height >= 0 and height <= last_block_index:
        return True
    else:
        return False


def process_block(block_height):
    if is_height_valid( block_height ) == False:
        print("Trying to parse a block of invalid height = %d" (block_height) )
        return False
    # o parametro 4 indica que queremos o formato mais verboso possivel
    # qualquer duvida olhar: multichain.com/developers/json-rpc-api/ 
    block = api.getblock(block_height, 4) 
    
    block_filename = "./blocks/block" + str( block_height ) + ".json"
    
    with open(block_filename, 'w+') as output:
        json.dump(block, output)
    
    f = open("./blocks/block_metadata.txt", "a+")
    f.write("%d\n" % (block_height) )
    f.close()
    print("Parsed block with height = %d" % ( int(block_height) ) )
    return True


'''
safety_block_space diz respeito a quantos blocos precisam ser validados apos um determinado bloco, para que esse bloco seja processado.
Ex: safety_block_space = 10, so iremos processor o bloco 40 assim que
a altura da chain seja 50.
'''

def parse_chain(safety_block_space, retry_limit):
    last_processed_block = get_last_processed_block_height() 
    current_chain_height = get_chain_height()  
    
    current_block = int(last_processed_block) + 1

    while current_block + safety_block_space <= current_chain_height:
        x = process_block( current_block )
        attempt = 1
        while x == False and attempt + 1 <= retry_limit:
            attempt = attempt + 1
            x = process_block( current_block )
        
        if x == False:
            print("Parsing of block %d failed in all %d attempts" % (current_block, attempt) )
            return False # isso indica que o parsing falhou, nao podemos continuar parseando, pois estamos supondo que os blocos sao parseados de forma consecutiva
        current_block = current_block + 1
    
    return True


# Testing
parse_chain(5, 1)

