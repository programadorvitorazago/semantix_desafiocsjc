#----------------------------------------------
# Programa DESAFIO SJC para Semantix - Arquivo principal
# Programador: Vitor Zago
# Data: 08/04/2020
# Versão 1.2
#----------------------------------------------

import datetime
import time
import csv
import os
import requests
import InterpretacaoHTMLBolsa as ParseHTMLBolsa
import InterpretacaoHTMLMoeda as ParseHTMLMoeda
import sys
import RepositorioDado

# Parâmetros Gerais
# nome do arquivo com os endereços para importação das ações
arquivoListaUrlCotacao = 'Config/listaUrlCotacaoBolsa.csv'
arquivoListaUrlCotacaoMoeda = 'Config/listaUrlCotacaoMoeda.csv'
arquivoBaseDado = 'BancoDado.db'

subPastaArquivoConversao = 'Arquivo'
intervaloRequisicao = 2 * 60 # 2 minutos - Tempo em segundos

# Enganar o site fingindo a requisição ser do Mozila Firefox
# Sem isso, o servidor recusava a requisição
user_agent = {'User-agent': 'Mozilla/5.0'}

#Definição da classe padrão de Url de Cotação
class UrlCotacao:
    def __init__(self, _bolsa, _url, _moeda):
        self.bolsa = _bolsa  # Nome da Bolsa
        self.url = _url
        self.moeda = _moeda
        
        # Contem a lista de Cotacao
        self.listaCotacao = None
            
    def __repr__(self):
        return 'Url: ' + self.url + ' Moeda: ' + self.moeda + ' Bolsa: ' + self.bolsa
        
    def redefinir(self):
        self.listaCotacao = None
        

class UrlCotacaoMoeda:
    def __init__(self, _mOrigem, _mDestino, _url):
        self.moedaOrigem = _mOrigem
        self.moedaDestino = _mDestino
        self.url = _url
        
        # Cotacao Referente
        self.cotacaoMoeda = None
            
    def __repr__(self):
        return 'Url: ' + self.url + ' Moeda Origem: ' + self.moedaOrigem + ' Moeda Destino: ' + self.moedaDestino
        
    def redefinir(self):
        self.cotacaoMoeda = None

# Verifica se a subPasta Existe e cria se necessário
def verificarSubpasta(nomeCaminho):
    if not os.path.exists(nomeCaminho):
        os.mkdir(nomeCaminho)

# --------------------------------------- 
# Função de gravação de Cotação de Ações convertidas
# --------------------------------------- 
def gravarCotacaoConvertido(listaCotacaoConvertido, nomeArquivo):
    
    verificarSubpasta(subPastaArquivoConversao)
        
    caminhoArquivoSaida = os.path.join(subPastaArquivoConversao, nomeArquivo)
    
    with open(caminhoArquivoSaida, 'w', newline='') as csvfile:
        gravadorCSV = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Cabeçalho
        gravadorCSV.writerow(['name','last_rs','high_rs','low_rs','last_usd','high_usd', 'low_usd','chg','chg_perc','vol','time']) 
        
        # Dados
        for cotacao in listaCotacaoConvertido:
            gravadorCSV.writerow([cotacao.nome, cotacao.last_conv, cotacao.high_conv, cotacao.low_conv, cotacao.last, cotacao.high, cotacao.low, cotacao.chg, cotacao.chgP, cotacao.vol, cotacao.time])

# --------------------------------------- 
# Função de requisição de endereço da internet
# --------------------------------------- 
def requisitarEndereco(enderecoUrl, caminhoSaida = ''):
    
    # Resgatando informação do SITE
    req = requests.get(enderecoUrl, headers = user_agent)
    print("Url: ", req.url, " Código retorno:", req.status_code)
    
    if not caminhoSaida is None and len(caminhoSaida) > 0:
        with open(caminhoSaida,'wb') as gravadorArquivo:
            gravadorArquivo.write(req.content)
            print('Arquivo salvo em ', caminhoSaida)

    return req

# --------------------------------------- 
# Função de importação de conteudo de bolsa
# --------------------------------------- 
def importarConteudoSiteBolsa(urlCotacao, caminhoSaida = ''):
    
    # Requisitando URL
    req = requisitarEndereco(urlCotacao.url, caminhoSaida)
    
    # Criado objetos de Cotação / Ação
    listaCotacaoParcial = ParseHTMLBolsa.getListaCotacaoPorConteudo(req.text)
    for cotacao in listaCotacaoParcial:
        cotacao.moeda = urlCotacao.moeda
    print('Encontrado', len(listaCotacaoParcial), 'cotações.')
    urlCotacao.listaCotacao = listaCotacaoParcial 
       
    return listaCotacaoParcial
    
# --------------------------------------- 
# Função de importação de conteudo de Moeda
# --------------------------------------- 
def importarConteudoSiteMoeda(urlCotacaoMoeda, caminhoSaida = ''):
    # Requisitando URL
    req = requisitarEndereco(urlCotacaoMoeda.url, caminhoSaida)
    
    # Criado objetos de Cotação de moeda
    cotacaoMoeda = ParseHTMLMoeda.getCotacaoMoedaPorConteudo(req.text)
    urlCotacaoMoeda.cotacaoMoeda = cotacaoMoeda

    return cotacaoMoeda
    
# --------------------------------------- 
# Função de conversão de Cotação da Bolsa
# --------------------------------------- 
def converterCotacao(urlCotacao, moedaDestino, nomeArquivoConvertido = ''):
    print('Necessário conversão:')
    mOrigem = urlCotacao.moeda
    mDestino = moedaDestino

    cotacaoConversao = next( (x for x in iter(listaUrlCotacaoMoeda) if x.moedaOrigem == mOrigem and x.moedaDestino == mDestino), None)
    if cotacaoConversao is None:
        print('Não convertido. Não definido cotação para conversão de', mOrigem, 'para', mDestino, '!')
    else:
        fatorConversao = cotacaoConversao.cotacaoMoeda.cotacao
        print('Fator de conversão:', fatorConversao)
        for cotacaoBolsa in urlCotacao.listaCotacao:
            cotacaoBolsa.converterMoeda('R$', fatorConversao)
   
        if not nomeArquivoConvertido is None and nomeArquivoConvertido != '':
            gravarCotacaoConvertido(urlCotacao.listaCotacao, nomeArquivoConvertido)

#------------------------------------------
# MAIN - LOOP Principal
#------------------------------------------

# Preparando url de resgate
listaUrlCotacao = []
listaUrlCotacaoMoeda = []
with open(arquivoListaUrlCotacao, 'r') as arquivoCsv:
    leitorCSV = csv.reader(arquivoCsv, delimiter=';', quotechar='"')
    for linha in leitorCSV:
        if len(linha) >= 3:
            urlCotacao = UrlCotacao(linha[0], linha[1], linha[2]) # Nome Bolsa;URL;Moeda
            listaUrlCotacao.append(urlCotacao)

with open(arquivoListaUrlCotacaoMoeda, 'r') as arquivoCsv:
    leitorCSV = csv.reader(arquivoCsv, delimiter=';', quotechar='"')
    for linha in leitorCSV:
        if len(linha) >= 3:
            urlCotacaoMoeda = UrlCotacaoMoeda(linha[0], linha[1], linha[2]) # Moeda Origem; Moeda Destino; Url
            listaUrlCotacaoMoeda.append(urlCotacaoMoeda)

if len(listaUrlCotacao) == 0:
    raise Exception('Nenhuma Url de cotação definida.')

# LOOP Principal
rep = RepositorioDado.Repositorio(arquivoBaseDado)
numRequisicao = 0    
print('Iniciando LOOP principal')
while True:
    try:
        # Redefinindo lista de cotação na bolsa
        for enderecoUrl in listaUrlCotacao:
            enderecoUrl.redefinir()
         
        # Redefinindo conversao de moeda
        for enderecoUrl in listaUrlCotacaoMoeda:
            enderecoUrl.redefinir()
            
        exatoInstante = datetime.datetime.now()
        print('Requisição nº', (numRequisicao + 1), exatoInstante)
        
        # Fazendo e atualizado as cotações
        contador = 1
        for enderecoUrl in listaUrlCotacao:
            importarConteudoSiteBolsa(enderecoUrl, 'Site' + str(contador) + '.HTML')
            rep.salvarListaCotacaoAcao(enderecoUrl, exatoInstante)
            contador += 1
        
        for enderecoUrlMoeda in listaUrlCotacaoMoeda:
            importarConteudoSiteMoeda(enderecoUrlMoeda, 'CotacaoMoeda.HTML')
            rep.salvarCotacaoMoeda(enderecoUrlMoeda, exatoInstante)
        
        # Verificando necessidade de conversão
        for bolsaValor in listaUrlCotacao:
            if bolsaValor.moeda != 'R$':
                nomeArquivoConvertido = exatoInstante.strftime("%Y%m%dT%H%M%S") + '_' + urlCotacao.bolsa + '.csv'
                converterCotacao(bolsaValor, 'R$', nomeArquivoConvertido)
    except:
        print('Ocorreu algum erro nesta requisição. Verifique o acesso a internet e tente novamente', sys.exc_info()[0])
            
    print('Fim da requisição nº', (numRequisicao + 1), '. Aguardando para próxima requisição.')
    time.sleep(intervaloRequisicao) 
    numRequisicao += 1 ## Imcrementar para p´roxima requisição

# Obrigado pela oportunidade 



