# semantix_desafiocsjc
Repositório do código fonte para o Desafio SJC da Semantix

Programa: Semantix_Desafiosjc
Programador: Vitor Zago
Data: 08/04/2020
Versão 1.2
O código fonte da aplicação em Python está disponível na pasta src junto com todas as bibliotecas criadas.
O arquivo principal é o 'Desafio_ProjetoSJC.py'.
Para executa-lo basta digitar: 'python3 Desafio_ProjetoSJC.py'
O aplicativo irá requisitar a cotação das ações das respectivas bolsas conforme configurado no arquivo CSV 'listaUrlCotacaoBolsa.csv' dentro da subpasta 'Config'.
O aplicativo irá requisitar a cotação para conversões de moeda nos respectivos endereços definidos no arquivo CSV 'listaUrlCotacaoMoeda.csv' dentro da subpasta 'Config'.
O arquivo listaUrlCotacaoBolsa.csv deverá obedecer a seguinte estrutura:
  •	Sem cabeçalho
  •	Nome da bolsa;Url;Moeda
    o	Exemplo de moedas: [U$, R$, E$]

O arquivo listaUrlCotacaoMoeda.csv deverá obedecer a seguinte estrutura:
  •	Sem cabeçalho
  •	Moeda de Origem; Moeda de destino; Url
    o	Exemplo de moedas: [U$, R$, E$]
A subpasta Config deve estar na mesma pasta de trabalho do processo principal.
Toda ação da bolsa cuja moeda seja diferente de “R$” irá ser convertida se existir uma Url de Cotação de conversão correspondente. A conversão irá criar um arquivo CVS cujo nome será timeStamp_nomebolsa.csv dentro da subpasta Arquivo com a seguinte estrutura:
  •	Com cabeçalho: 
  •	Valores para cada ação: ['name','last_rs','high_rs','low_rs','last_usd','high_usd', 'low_usd','chg','chg_perc','vol','time']

A aplicação irá gravar em um banco SQLite no arquivo BancoDado.db todas as requisições das URLs seguindo a seguinte estrutura.

(Vide LEIAME/LEIAME.PDF)
 
Para criação de uma imagem para um container docker o arquivo DockerFile esta na pasta Docker.
Acesse a pasta e proceda com o comando docker build –-tag tagName . para efetuar o build.
A imagem gerada poderá ser acessada no repositório do docker hub no seguinte endereço:
https://hub.docker.com/r/programadorvitorzago/semantix_desafiosjc
Os arquivos de código fonte poderão ser acessados no endereço:
https://github.com/programadorvitorazago/semantix_desafiosjc

