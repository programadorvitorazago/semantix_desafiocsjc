#----------------------------------------------
# Biblioteca para interpretação do HTML da cotação da Moeda
#----------------------------------------------

import re # RegExp

# definindo a classe
class CotacaoMoeda:
    def __init__(self, _cotacao):
        self.cotacao = _cotacao
        self.chg = 0
        self.chkP = 0
        self.time = 0
      
    def imprimirCompleto(self):
        print("Cotação:", self.cotacao,
                "Alteração:", self.chg, "Alteração em porcentual:", self.chgP, "Instante:", self.time)
	
    def imprimir(self):
        print("Cotação:", self.cotacao, "Instante:", self.time)
			  
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
padraoCotacao = '.*<span.*class=.*pid-2103-last.*>\s*([0-9]+(\.[0-9]*)?)\s*</span>' # GetNome por Grupo nº 1
padraoChg = '.*<i.*class=.*pid-2103-pc.*>\s*([+\-]?[0-9]+(\.[0-9]*)?)\s*</i>' # Grupo 3
padraoChgP = '.*<i.*class=.*pid-2103-pcp.*>\s*([+\-]?[0-9]+(\.[0-9]*)?)%?\s*</i>' # Grupo 5
padraoTime = '.*<i.*class=.*pid-2103-time.*>\s*([0-9\/:]*)\s*</i>' # Grupo 6

regexValores = re.compile('<div.*>' + padraoCotacao
    + padraoChg + padraoChgP + padraoTime + '.*</div>'
    , flags=re.DOTALL)

def converterParaFloat(valorStr):
    novoValorStr = valorStr.replace(',', '')
    valorConvertido = float(novoValorStr)
    return valorConvertido

def getCotacaoMoeda(parteConteudo):

    matchValor = regexValores.search(parteConteudo)

    if matchValor is None:
        print('Não bateu: ' + parteConteudo)
        return None
    else:
        cotacao = CotacaoMoeda(converterParaFloat(matchValor.group(1)))
        cotacao.chg = converterParaFloat(matchValor.group(3))
        cotacao.chgP = converterParaFloat(matchValor.group(5))
        cotacao.time = converterParaFloat(matchValor.group(6))
        
        return cotacao

def getCotacaoMoedaPorArquivo(caminhoArquivo):

    leitor = open(caminhoArquivo, 'r')
    
    conteudoCompleto = leitor.read()
    listaCotacao = getListaCotacaoPorConteudo(conteudoCompleto)
    leitor.close()
    
    return listaCotacao
        
def getCotacaoMoedaPorConteudo(conteudoCompleto):
    
    parteConteudo,_ = procurarParte(conteudoCompleto, '<section class="boxItemInstrument boxItem', '</section>')
    
    cotacao = getCotacaoMoeda(parteConteudo)
    
    return cotacao

    
    
