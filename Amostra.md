# Amostra - Banco Distribuído com WebServices

Para testar o sistema de banco distribuido criou-se um script Cliente que executa chamadas assíncronas e concorrentes para cada endpoint dos Servidores de Negócio acessado por meio de um load balancer implementado diretamente no Google Cloud.

## Execução do script Cliente

Ao executar o script as requisições são enviadas ao servidores. Para testar o caso de falta de autenticação criou-se um array de tokens e no meio desses tokens alguns tokens falsos, na imagem é possivel ver as requisições com falha de token pela response "Forbidden".

![Print da execução do script Cliente](https://i.imgur.com/hmjym3b.png)

## Logs de execução

- Servidor de negócio

```{r}
Timestamp:2021-10-31 13:13:45.087371 - OperationNumber: 1 - ClientID: 1 - OperationType: Saldo - Account: 3 - Value: N/A
Timestamp:2021-10-31 13:13:46.223686 - OperationNumber: 2 - ClientID: 1 - OperationType: Saldo - Account: 3 - Value: N/A
Timestamp:2021-10-31 13:13:47.284277 - OperationNumber: 3 - ClientID: 1 - OperationType: Saldo - Account: 3 - Value: N/A
Timestamp:2021-10-31 13:15:11.534692 - OperationNumber: 4 - ClientID: 1 - OperationType: Saldo - Account: 3 - Value: N/A
Timestamp:2021-10-31 13:15:12.722339 - OperationNumber: 5 - ClientID: 1 - OperationType: Saldo - Account: 3 - Value: N/A
Timestamp:2021-10-31 13:16:27.637879 - OperationNumber: 6 - ClientID: 1 - OperationType: Saldo - Account: 3 - Value: N/A
Timestamp:2021-10-31 13:16:35.086740 - OperationNumber: 7 - ClientID: 1 - OperationType: Deposito - Account: 1 - Value: 100
Timestamp:2021-10-31 13:18:18.005728 - OperationNumber: 8 - ClientID: 5 - OperationType: Deposito - Account: 9 - Value: 299
Timestamp:2021-10-31 13:18:18.013317 - OperationNumber: 9 - ClientID: 4 - OperationType: Saldo - Account: 6 - Value: N/A
Timestamp:2021-10-31 13:18:18.014164 - OperationNumber: 10 - ClientID: 3 - OperationType: Saque - Account: 2 - Value: 146
```

- Servidor de dados

```{r}
Timestamp:2021-10-31 16:05:13.640164 - OperationNumber: 1 - BusinessServerID: 1 - OperationType: getlock - Account: 1 - Value: 0
Timestamp:2021-10-31 16:05:13.642598 - OperationNumber: 2 - BusinessServerID: 1 - OperationType: getlock - Account: 1 - Value: 0
Timestamp:2021-10-31 16:05:13.644029 - OperationNumber: 3 - BusinessServerID: 1 - OperationType: getlock - Account: 1 - Value: 0
Timestamp:2021-10-31 16:05:13.644678 - OperationNumber: 4 - BusinessServerID: 1 - OperationType: getlock - Account: 1 - Value: 0
Timestamp:2021-10-31 16:05:13.645480 - OperationNumber: 5 - BusinessServerID: 1 - OperationType: getlock - Account: 1 - Value: 0
Timestamp:2021-10-31 16:05:13.645859 - OperationNumber: 6 - BusinessServerID: 1 - OperationType: getlock - Account: 1 - Value: 0
Timestamp:2021-10-31 16:05:13.646419 - OperationNumber: 7 - BusinessServerID: 1 - OperationType: getlock - Account: 1 - Value: 0
Timestamp:2021-10-31 16:05:13.646450 - OperationNumber: 8 - BusinessServerID: 1 - OperationType: getlock - Account: 1 - Value: 0
Timestamp:2021-10-31 16:05:13.647100 - OperationNumber: 9 - BusinessServerID: 1 - OperationType: getlock - Account: 1 - Value: 0
Timestamp:2021-10-31 16:05:13.647118 - OperationNumber: 10 - BusinessServerID: 1 - OperationType: getlock - Account: 1 - Value: 0
```
