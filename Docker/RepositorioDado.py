#----------------------------------------------
# Biblioteca de acesso ao banco de dados
#----------------------------------------------

import sqlite3
import os


# função de criaças das tabelas
def criarTabela(conexao):
    print('Criando tabelas pela primeira vez:')
    tabelaBolsa = """CREATE TABLE Bolsa(
            ID INTEGER PRIMARY KEY,
            Nome TEXT,
            Moeda TEXT)"""
    tabelaCotacaoAcao = """CREATE TABLE Cotacao(
            ID INTEGER PRIMARY KEY,
            ID_Bolsa INTEGER,
            Nome TEXT,
            last REAL,
            high REAL,
            low REAL,
            chg REAL,
            chgP TEXT, 
            vol TEXT,
            time TEXT,
            instante TEXT,
            FOREIGN KEY(ID_Bolsa) REFERENCES Bolsa(ID))"""
    tabelaCotacaoMoeda = """CREATE TABLE CotacaoMoeda(
            ID INTEGER PRIMARY KEY,
            MoedaOrigem TEXT,
            MoedaDestino TEXT,
            Cotacao REAL,
            chg REAL,
            chgP TEXT,
            time TEXT,
            instante TEXT)"""
    
    cursorSql = conexao.cursor()
    
    cursorSql.execute(tabelaBolsa)
    cursorSql.execute(tabelaCotacaoAcao)
    cursorSql.execute(tabelaCotacaoMoeda)
    
    conexao.commit()
    cursorSql.close()
    
    print('Tabelas criadas!')
        
      
# Classe principal    
class Repositorio:
    """ Classe principal responsável pela gravação de todos os dadso """
    def __init__(self, _arquivoBanco):
    
        print('Prepatando banco de dados:', _arquivoBanco)
        self.arquivoBanco = _arquivoBanco
        
        deveCriarTabela = not os.path.exists(_arquivoBanco)
            
        self.conexao = sqlite3.connect(_arquivoBanco)
        
        if(deveCriarTabela):
            criarTabela(self.conexao)
            
    def getID_Bolsa(self, bolsa): # bolsa = desafio_ProjeoSJC class UrlCotacao 
        cursorSql = self.conexao.cursor()
        
        comandoSQL = 'SELECT ID FROM Bolsa WHERE Nome = ?'
        
        cursorSql.execute(comandoSQL, (bolsa.bolsa,) )
        
        rows = cursorSql.fetchall()
        
        cursorSql.close()
        
        if len(rows) > 0:
            return rows[0][0]
        else:
            return None
            
    def salvarBolsa(self, bolsa): # bolsa = desafio_ProjeoSJC class UrlCotacao 
        cursorSql = self.conexao.cursor()
        
        comandoSQL = 'INSERT INTO Bolsa(Nome, Moeda) VALUES (?, ?)'
        
        cursorSql.execute(comandoSQL, (bolsa.bolsa, bolsa.moeda) )
        
        self.conexao.commit()
        
        cursorSql.close()
        
    def getOrCreateID_Bolsa(self, bolsa): # bolsa = desafio_ProjeoSJC class UrlCotacao 
        idBolsa = self.getID_Bolsa(bolsa)
        if idBolsa is None:
            self.salvarBolsa(bolsa)
            idBolsa = self.getID_Bolsa(bolsa)
        return idBolsa 
        
    def salvarListaCotacaoAcao(self, bolsa, instante): # bolsa = desafio_ProjeoSJC class UrlCotacao
        cursorSql = self.conexao.cursor()
        
        comandoSQL = """INSERT INTO Cotacao(ID_Bolsa,
                Nome,
                last,
                high,
                low,
                chg,
                chgP, 
                vol,
                time,
                instante)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        idBolsaFK = self.getOrCreateID_Bolsa(bolsa)
        
        for cotacaoAcao in bolsa.listaCotacao: # cotacaoAcao = InterpretacaoHTMLBolsa class Cotacao
            cursorSql.execute(comandoSQL, (idBolsaFK, cotacaoAcao.nome, cotacaoAcao.last, cotacaoAcao.high, cotacaoAcao.low, cotacaoAcao.chg, cotacaoAcao.chgP, cotacaoAcao.vol, cotacaoAcao.time, instante) )
        
        self.conexao.commit()
        cursorSql.close()
        
    def salvarCotacaoMoeda(self, cotacaoMoeda, instante): # cotacaoMoeda = desafio_ProjeoSJC class UrlCotacaoMoeda
        cursorSql = self.conexao.cursor()
        
        comandoSQL = """INSERT INTO CotacaoMoeda(
                MoedaOrigem,
                MoedaDestino,
                Cotacao,
                chg,
                chgP,
                time,
                instante)
                VALUES (?, ?, ?, ?, ?, ?, ?)"""
        
        valorCotacao = cotacaoMoeda.cotacaoMoeda # valorCotacao = InterpretacaoHTMLMoeda class CotacaoMoeda
        if not valorCotacao is None:
        
            cursorSql.execute(comandoSQL, ( cotacaoMoeda.moedaOrigem, cotacaoMoeda.moedaDestino, valorCotacao.cotacao,valorCotacao.chg, valorCotacao.chgP, valorCotacao.time, instante) )
            
            self.conexao.commit()
            
        cursorSql.close()

# preparando banco de dados
# conexao = sqlite3.connect('Captura.db')
# 
# def verificarECriarTabela(conexao):
#     cursorSql = conexao.cursor()
#     
#     try:
#         SQLCMD_CriarTabela = """CREATE TABLE Cotacao(Nome text, Valor real)"""
#         cursorSql.execute(SQLCMD_CriarTabela)
#     except :
#         pass # Provavelmente tabela já criada! 
# 
# verificarECriarTabela(conexao)
# 
# SQLCMD_Inserir = """INSERT INTO Cotacao VALUES(?,?)"""
# for cotacao in listaCotacao:
#     cursorSql = conexao.cursor()
#     cursorSql.execute(SQLCMD_Inserir, (cotacao.nome, cotacao.last))
#     
# conexao.commit()






