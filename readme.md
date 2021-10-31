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

# Servidor de negócio
Assim como o servidor de dados, o servidor de negócio é uma API  RESTful, desenvolvida em Python, que utiliza o framework Flask.
Para realizar o deploy da API é necessário configurar uma maquina com NGINX e WSGI. No ambiente de testes foi utilizada a nuvem Google Cloud com instâncias de Compute Engine.

 - Métodos da API
 
     \*Todas as requisições precisam do header auth-token com o token de acesso do cliente.
     \*Todas as requisições precisam do header client-id com o id do cliente.

	**POST - /deposito/<acnt>/<amnt>**
    Acrescenta o valor definido por `amnt` na conta definida por `acnt`.
	 
	**POST - /saque/<acnt>/<amnt>**
    Deduz o valor definido por `amnt` da conta definida por `acnt`.
	
	**GET - /saldo/<acnt>**
	Verifica se a conta esta bloqueada, ou seja, algum outro servidor está lendo alguma informação da mesma conta ao mesmo tempo.
	
	**POST - /transferencia/<acnt_orig>/<acnt_dest>/<amnt>**
    Deduz o valor definido por `amnt` da conta definida por `acnt_orig` e acrescenta o mesmo valor a conta definida por `acnt_dest`.

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