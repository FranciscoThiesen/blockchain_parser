# Autor: Francisco Thiesen, Email: fthiesen@arpexcapital.com.br/franciscogthiesen@gmail.com
'''
Essa eh uma v0 do parser de multichain.
Coisas que sao essenciais que nao estou me preocupando nessa versao
- Tratamento de erro/excecoes
- Recuperacao de dados Off-chain
- Testes dos metodos / Testes de integracao 
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

def get_last_processed_block_index():
    last_processed_block = -1
    if os.find.isfile('./blocks/block_metadata') == True:
        f = open("./blocks/block_metadata", "w+")
        # o arquivo blockmetadata possui todos os blocos completamente processados pelo parser, separados por espaco
        '''
        A organizacao dos arquivos de block_metadata pode ser repensada.
        Podemos colocar todos os blocos processados numa determinada execucao do parser em uma unica linha/varias linhas,
        podemos tambem armazenar apenas um inteiro que eh o do ultimo bloco processador ate agora. Nao fiz
        isso porque nao queria que tivessemos que deletar o numero anterior do arquivo de blockmetadata.
        Achei mais interessante que o arquivo fosse append-only.
        '''
        processedBlocks = []
        for line in f:
            processedBlocks.append( [ int(x) for x in line.split() ] )

        if len(processedBlocks) > 0:
            last_processed_block = processedBlocks[-1] 
    return last_processed_block

def is_height_valid( height ):
    chain_metadata = api.getinfo()
    last_block_index = chain_metadata[u'blocks']
    if height >= 0 and height <= last_block_index:
        return True
    else:
        return False

def process_block(block_height):
    if is_height_valid( block_height ) == False:
        print("Foi solicitado que um bloco de altura invalida fosse parseado " )
        return False
    # o parametro 4 indica que queremos o formato mais verboso possivel
    # qualquer duvida olhar: multichain.com/developers/json-rpc-api/ 
    block = api.getblock(block_index, 4) 
    
    block_file_name = "block" + str( block_height ) + ".json"
    
    with open(block_filename, 'w+') as output:
        json.dump(block, output)
   
    
chain_metadata= api.getinfo()
last_block_index = chain_metadata[u'blocks']

print( x[u'blocks'])


