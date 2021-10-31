# Projeto - Banco Distribuído com WebServices

Objetivo: implementar um Sistema de Banco Distribuído que consistirá  em:  
- Servidor de dados (banco de dados)
- Três (ou mais) servidores de negócio (responsáveis  pela conexão com o cliente e com o servidor de dados)
- Vários clientes, implementados em Python (e opcionalmente,  em mais uma linguagem de programação diferente)

![Distribuição das maquinas do Sistema de Banco Distribuido](https://i.imgur.com/yRPn2zh.png)

## Descrição do projeto
- O intuito do projeto é criar um sistema bancário simples baseado em microsserviços, que conta com um servidor de dados que lida com o banco de dados num sistema de `lock`, onde uma conta fica bloqueada assim que algum servidor começa a alterá-la, e apenas esse mesmo servidor pode remover a trava.
- Para se comunicar com o servidor de dados, o projeto também conta com **três** servidores de negócio, que vão ser o intermediador entre os clientes e o servidor de dados. Para isso, deve-se autenticar a conexão com os headers `auth-token` e `business-id`. Esses servidores lidam com a lógica de negócio de `filas`, chamadas na api do servidor de dados e retorno para os clientes.
- Por último, os clientes representam pessoas tentando acessar e modificar dados das contas bancárias. Para que os clientes possam interagir com as contas, devem se autenticar com os headers `auth-token` e `client-id`. Dependendo do estado de lock da conta que se deseja alterar, o cliente receberá um erro, ao invés do estado desejado.

## Funcionamento

#### Servidor de dados
Recebe as requisições dos servidores de negócio, trata os dados e os headers para autenticação, verifica o estado de lock da conta atuante e aplica modificações em caso de sucesso. Envia erro em caso de falha.
  
#### Servidores de negócios
Recebem as requisições dos clientes, trata os dados e os headers para autenticação e envia as instruções para o servidor de dados. Envia os dados em caso de sucesso e erro em caso de falha.

#### Cientes
Simplesmente definem um pedido (como por exemplo transferir X valor da conta Y para a conta Z), envia a solicitação para o load balancer que replica a requisição para os servidores de negócio.


## Possíveis extensões
- Implementação de um banco de dados com atomicidade nativa, como o Redis, MongoDB etc num servidor separado, para que o sistema de lock se resolva mais facilmente e os dados deixem de ser `inmemory` e se tornem `permanentes`.