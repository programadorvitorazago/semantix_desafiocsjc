#----------------------------------------------
# Biblioteca para interpretação do HTML das Ações da Bolsa
#----------------------------------------------

import re # RegExp

# definindo a classe
class Cotacao:
    def __init__(self, _nome):
        self.nome = _nome
        self.last = 0
        self.high = 0
        self.low = 0
        self.moeda = None
        self.chg = 0
        self.chkP = 0
        self.vol = 0
        self.time = 0
        
        # Para conversão se necessário
        self.moedaDestino = None
        self.last_conv = None
        self.high_conv = None
        self.low_conv = None

    def imprimirCompleto(self):
        print("Nome:", self.nome, "Moeda:", self.moeda, "Última:", self.last, "Teto:", self.high, "Chão:"
              , self.low, "Alteração:", self.chg, "Alteração em porcentual:", self.chgP, "Volume:", self.vol, "Instante:", self.time)
	
    def imprimir(self):
        print("Nome:", self.nome, "Moeda:", self.moeda, "Última:", self.last, "Teto:", self.high, "Chão:", self.low)
        
    def converterMoeda(self, _moedaDestino, _fator):
        self.moedaDestino = _moedaDestino
        self.last_conv = self.last * _fator;
        self.high_conv = self.high * _fator;
        self.low_conv = self.low * _fator;
        
class CotacaoMoeda:
    def __init__(self, _mOrigem, _mDestino,  ):
        self.moedaOrigem = _mOrigem
        self.moedaDestino = _mDestino
        self.cotacao = 0
        self.chg = 0
        self.chkP = 0
        self.time = 0
      
    def imprimirCompleto(self):
        print("Moeda Origem:", self.moedaOrigem, "Moeda destino:", self.moedaDestino, "Cotação:", self.cotacao,
                "Alteração:", self.chg, "Alteração em porcentual:", self.chgP, "Instante:", self.time)
	
    def imprimir(self):
        print("Moeda Origem:", self.moedaOrigem, "Moeda destino:", self.moedaDestino, "Cotação:", self.cotacao)
			  
def procurarParte(conteudoCompleto, padraoParteIni, padraoParteFim, posicaoInicial = 0):
    regexIni = re.compile(padraoParteIni)
    regexFim = re.compile(padraoParteFim)

    matchIni = regexIni.search(conteudoCompleto, pos = posicaoInicial)
    if matchIni is None:
        return None, -1
    else:
        indexMatchIni = matchIni.start()
        matchFim = regexFim.search(conteudoCompleto, pos=indexMatchIni)
        indexMatchFim = 0;
        if matchFim is None:
            indexMatchFim = conteudoCompleto.len()
        else:
            indexMatchFim = matchFim.end()
        return conteudoCompleto[indexMatchIni:indexMatchFim], indexMatchFim  

# Preparando o reconhecimento de padrao
padraoNome = '.*<td.*</td>.*<td.*<a.*>(.*)</a>.*</td>' # GetNome por Grupo nº 1
padraoLast = '.*<td.*>([0-9,]+(\.[0-9]*)?)</td>' # Grupo 2
padraoHigh = '.*<td.*>([0-9,]+(\.[0-9]*)?)</td>' # Grupo 4
padraoLow = '.*<td.*>([0-9,]+(\.[0-9]*)?)</td>' # Grupo 6
padraoChg = '.*<td.*>([+\-]?[0-9,]+(\.[0-9]*)?)</td>' # Grupo 8
padraoChgP = '.*<td.*>([+\-]?[0-9]+(\.[0-9]*%)?)</td>' # Grupo 10
padraoVol = '.*<td.*>([0-9]+(\.[0-9]*)?[A-Z]?)</td>' # Grupo 12
padraoTime = '.*<td.*>([0-9\/:]+)</td>' # Grupo 14

regexValores = re.compile('<tr'
    + padraoNome + padraoLast + padraoHigh + padraoLow
    + padraoChg + padraoChgP + padraoVol + padraoTime
    + '.*</tr>', flags=re.DOTALL)

def converterParaFloat(valorStr):
    novoValorStr = valorStr.replace(',', '')
    return float(novoValorStr)

def getCotacao(parteConteudo):

    matchValor = regexValores.match(parteConteudo)

    if matchValor is None:
        print('Não bateu: ' + parteConteudo)
        return None
    else:
        cotacao = Cotacao(matchValor.group(1))
        cotacao.last = converterParaFloat(matchValor.group(2))
        cotacao.high = converterParaFloat(matchValor.group(4))
        cotacao.low = converterParaFloat(matchValor.group(6))
        cotacao.chg = converterParaFloat(matchValor.group(8))
        cotacao.chgP = matchValor.group(10)
        cotacao.vol = matchValor.group(12)
        cotacao.time = matchValor.group(14)
        
        return cotacao
        
def getCotacaoMoeda(parteConteudo):

    matchValor = regexValores.match(parteConteudo)

    if matchValor is None:
        print('Não bateu: ' + parteConteudo)
        return None
    else:
        cotacao = Cotacao(matchValor.group(1))
        cotacao.last = converterParaFloat(matchValor.group(2))
        cotacao.high = converterParaFloat(matchValor.group(4))
        cotacao.low = converterParaFloat(matchValor.group(6))
        cotacao.chg = converterParaFloat(matchValor.group(8))
        cotacao.chgP = matchValor.group(10)
        cotacao.vol = matchValor.group(12)
        cotacao.time = matchValor.group(14)
        
        return cotacao

def getListaCotacaoPorArquivo(caminhoArquivo):

    leitor = open(caminhoArquivo, 'r')
    
    conteudoCompleto = leitor.read()
    listaCotacao = getListaCotacaoPorConteudo(conteudoCompleto)
    leitor.close()
    
    return listaCotacao
        
def getListaCotacaoPorConteudo(conteudoCompleto):
    
    listaCotacao = []
        
    # resgatar a tabela    
    conteudoTabela,_ = procurarParte(conteudoCompleto, '<table id="cross_rate_markets_stocks_1"','</table>')

    #resgatar a primeira linha da tabela que é o cabeçalho
    #começar a partir da segunda
    _, indexFim = procurarParte(conteudoTabela, '<tr', '</tr>', posicaoInicial = 0)
    linha, indexFim = procurarParte(conteudoTabela, '<tr', '</tr>', posicaoInicial = indexFim)

    while not linha is None and len(linha) > 0:
        cotacao = getCotacao(linha)
        if not cotacao is None:
            listaCotacao.append(cotacao)
        if indexFim >= 0:
            linha, indexFim = procurarParte(conteudoTabela, '<tr', '</tr>', posicaoInicial = indexFim)
        else:
            break;

    return listaCotacao
    

    
    
