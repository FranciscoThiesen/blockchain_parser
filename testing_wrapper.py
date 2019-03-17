# Autor: Francisco Thiesen, Email: fthiesen@arpexcapital.com.br/franciscogthiesen@gmail.com

from Savoir import Savoir
import json

rpcuser = 'multichainrpc'
rpcpasswd = '2VNj2nnLGRH9fS8nKa6L8ZUEGsNKv5xv1UwANtykdxa6'
rpchost = 'localhost'
rpcport = '4780'
chainname = 'chain4'

api = Savoir( rpcuser, rpcpasswd, rpchost, rpcport, chainname )



# vamos extrair das informacoes sobre a chain a quantidade de blocos atual da chain
# ja recebemos no formator json da API
x = api.getinfo()
currentBlock = x[u'blocks']

def process_block( height ):
    block = api.getblock(height, 4)
    try:
        altura = block[u'height']
        print( altura )
    except Exception as e:
        raise
    
cur_height = x[u'blocks']

print( api.getblock( cur_height + 1 ) )
process_block( cur_height )
process_block( cur_height + 1)



