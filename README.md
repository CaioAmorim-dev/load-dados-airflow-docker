# Desafio Tecnico - LIGHT HOUSE

## 1Introdução

Este projeto consiste em um **pipeline de dados automatizado** para o Banco Vitória (BanVic), cujo objetivo é centralizar dados de diferentes fontes (CSV e SQL) em um **Data Warehouse PostgreSQL**, utilizando **Docker e Apache Airflow**, se tornando totalmente replicável.

Este ***README*** tem como foco auxiliar o analista a inicializar o projeto e subir os containers necessários para que tudo ocorra como esperado. um README mais completo esta presente dentro da raiz da pasta ***Banvic***

### Inicialmente verá dois arquivos nesta pasta:


**Banvic** é o arquivo principal, onde estará a maior parte da solução, além de um READ.md mais completo sobre todo o projeto.

**Banvic-source** è um arquivo separado contendo o banco fonte fornecido pelo desafio, a única mudança feita foi a adição de uma rede externa para conectar com as outras ferramentas 

# Pré-requisitos

1. Docker (versão 20.10 ou superior recomendada)

2. Docker Compose (já vem integrado no Docker Desktop ou pode ser instalado separado em Linux)


# Sistemas operacionais suportados:

1. Linux nativo (Ubuntu, Debian, Fedora, etc.)

2. Windows 10/11 com Docker Desktop e WSL

3. MacOS (com Docker Desktop instalado)


# Guia de Execução inicial

### 1. Subir o banco fonte
**Entre em `banvic-source`**  
Execute:

```bash
docker-compose up -d
```
Assim estará iniciado: \
***postgres:*** banco fonte fornecido pelo propro desafio

---

### 1.2 Subir o Airflow e DataWarehouse:

**Entre em `banvic/`**
 
 Execute:

```bash
docker-compose up  -d
```


Assim serão iniciados:

**dw-postgres:** Data Wherehouse  
**airflow-webserve:** Interface do Airflow \
**airflow-scheduler:** Dispara DAGs automaticamente \
**airflow-worker:** Executa tarefas do pipeline

---
### 1.3 Criar network para comunicação entre continers

execute:
```bash
docker network create banvic_network
```

Assim será criado:

***banvic_network:*** rede externa para comunicação do ***DW*** e ***airflow*** com o ***banco fonte***



