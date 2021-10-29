# Projeto - Banco Distribuído com WebServices

Objetivo: implementar um Sistema de Banco Distribuído que consistirá  em:  
- Servidor de dados (banco de dados)
- Três (ou mais) servidores de negócio (responsáveis  pela conexão com o cliente e com o servidor de dados)
- Vários clientes, implementados em Python (e opcionalmente,  em mais uma linguagem de programação diferente)

![Distribuição das maquinas do Sistema de Banco Distribuido](https://i.imgur.com/yRPn2zh.png)

# Servidor de dados /data_server
Implementado em Python o servidor de dados é uma API  RESTful que utiliza o framework Flask.
Para realizar o deploy da API é necessário configurar uma maquina com NGINX e WSGI. No ambiente de testes foi utilizada a nuvem Google Cloud com instâncias de Compute Engine.

 - Métodos da API
 
     \*Todas as requisições precisam do header auth-token com o token de acesso do servidor de negócio.
     \*Toda operação bloqueia temporáriamente o acesso a uma conta até que a operação seja concluida.

	**GET - /getbalance/<business_id>/<account_id>**
	 Retorna o saldo de uma determinada conta.
	 
	**POST - /setBalance**
	Soma ou subtrai o valor recebido pelo body da requisição do saldo da conta.
	Body: { "business_id": ID do servidor de negócio, "account_id": ID da conta, "value": valor a adicionar }
	
	**GET - /getLock/<business_id>/<account_id>**
	Verifica se a conta esta bloqueada, ou seja, algum outro servidor está lendo alguma informação da mesma conta ao mesmo tempo.
	
	**POST - /unLock**
	Body: { "account_id": ID da conta, "value": valor a adicionar }

- Configuração do NGINX
    ```
    server {
    	listen 80 default_server;
    	listen [::]:80 default_server;
    	root /var/www/html;
    	index index.html index.htm index.nginx-debian.html;
    	server_name _;
    	location / {
    		include uwsgi_params;
    		uwsgi_pass unix:/home/rafael/currency/app.sock;
    	}
    }
    ```
- Configuração do serviço do WSGI
    ```
    [Unit]
    Description=uWSGI instance to serve app
    After=network.target
    
    [Service]
    User=rafael
    Group=www-data
    WorkingDirectory=/home/rafael/currency
    Environment="PATH=/home/rafael/currency/venv/bin"
    ExecStart=/home/rafael/currency/venv/bin/uwsgi --ini app.ini
    
    [Install]
    WantedBy=multi-user.target
    ```