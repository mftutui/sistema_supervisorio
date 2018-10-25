 # Projeto integrador PIJ29006 - IFSC São José

Implementação dos sistemas de supervisão e do robô para o projeto integrador

## Objetivo
Jogo onde robôs devem se locomover à locais pré determinados em um ambiente fechado(tabuleiro) 
a partir de técnicas para localização *indoor*, tendo como desafio principal encontrar o maior número de pontos pré determinados possível.

## Especificações do projeto
A execução do jogo foi dividida em três sistemas diferentes: Sistema de Auditoria (SA), **Sistema Supervisório (SS)** e **Sistema do Robô (SR)**. Para fins de controle de partidas, histórico, cadastro de robôs e controle de captura de caças foi criado do sistema de auditoria, que age como juiz. O sistema supervisório atua como mediador entre os sistemas de auditoria e robô, é responsável por transmitir as informações da partida recebida do SA para os sistemas supervisórios de cada equipe, bem como de receber informações dos SR e retransmiti-las ao SA. O sistema robô fica responsável pela lógica para encontrar os alvos.

![Projeto Integrador](https://github.com/mftutui/sistema_supervisorio/projetointegrador.jpg)

O repositório possui os códigos utilizados para a implementação do **[Sistema Supervisório](https://github.com/mftutui/sistema_supervisorio/tree/master/sistema_supervisorio)** e do **[Sistema do Robô](https://github.com/mftutui/sistema_supervisorio/tree/master/server_python)**

Relatório final do projeto no [Overleaf](https://pt.overleaf.com/read/nfhsskmvbkjb) 
