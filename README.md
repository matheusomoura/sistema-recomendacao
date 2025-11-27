![status](https://img.shields.io/badge/status-finalizado-brightgreen)
![python](https://img.shields.io/badge/Python-3.11-blue)
![fastapi](https://img.shields.io/badge/FastAPI-API%20REST-brightgreen)


# 📚 Sistema de Recomendação – MovieLens  
Trabalho Final – Desenvolvimento de Sistemas de IA 

# 👨‍💻 Integrantes
- Matheus de Oliveira Moura
- Andre Aires de Lima
- Pedro H. de Santana Girardi

---

## 🎯 Objetivo do Projeto
Desenvolver um **Sistema de Recomendação funcional**, utilizando:

- Filtragem Colaborativa  
- Similaridade de Cosseno  
- Python + FastAPI  
- Container Docker  
- Dataset MovieLens (ml-latest-small)

O objetivo é entregar uma API funcional, capaz de:

- Recomendação de filmes similares  
- Recomendação personalizada baseada no histórico do usuário  

---

## 🏗️ Arquitetura da Solução

```bash
sistema-recomendacao/
│
├── app/
│   ├── main.py          # API FastAPI
│   ├── model.py         # Modelo de recomendação
│   └── __init__.py
│
├── data/
│   └── ml-latest-small/ # Dataset MovieLens
│
├── tests/
│   ├── test_api.py      # Testes da API
│   └── test_model.py    # Testes do modelo
│
├── check_dataset.py     # Teste rápido de leitura dos dados
├── Dockerfile           # Configuração Docker
├── docker-compose.yml   # Orquestração do container
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação oficial
```

---

## 🤖 Modelo de Recomendação

O sistema utiliza a técnica de **Item-Based Collaborative Filtering (Filtragem Colaborativa Baseada em Itens)**, amplamente utilizada em sistemas reais como Amazon e Netflix.

### **Etapas do modelo:**

1. Carregamento dos dados do MovieLens (`ratings.csv` e `movies.csv`)
2. Criação da matriz usuário x filme 
3. Transposição para obter matriz filme x usuário
4. Calcular **cosine_similarity** entre filmes  
5. Recomendar:  
   - **get_similar_movies(movie_id)**  
   - **recommend_for_user(user_id)**

---

## 🧠 Decisões

### ✦ Por que Filtragem Colaborativa Baseada em Itens?
- Produz recomendações mais explicáveis para o usuário (“filmes parecidos com X”).
- Tem custo computacional menor que filtragem baseada em usuários.
- Funciona bem mesmo em bases mais esparsas.

### ✦ Por que Similaridade do Cosseno?
- Métrica ideal para matrizes esparsas com muitos zeros.
- Resistente a variações na escala de notas.
- Utilizada na literatura e em aplicações reais de recomendação.

### ✦ Por que MovieLens?
- Dataset acadêmico padrão mundial.
- Estruturado, limpo, fácil de testar e validar.
- Representa cenários reais de recomendação.

### ✦ Por que FastAPI?
- Documentação automática no Swagger UI.
- Alta performance.
- Simples integração com Docker e testes automatizados.

### ✦ Estrutura de dados e lógica
- Matrizes e cálculos tratados com `NumPy` e `Pandas`.
- Similaridade pré-computada para melhorar desempenho.
- Recomendações do usuário utilizam média ponderada pelas avaliações.

  ---

## 📦 Instalação e Execução

### 🚀 Executando localmente

### 1. Criar ambiente virtual
```bash
python -m venv .venv
.\.venv\Scripts\activate
```
---

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Rodar a API
```bash
uvicorn app.main:app --reload
```

### Acessar:
➡ http://127.0.0.1:8000

➡ http://127.0.0.1:8000/docs → Documentação automática

---

## 🐳 Executando com Docker

### 1. Construir imagem
```bash
docker build -t sistema-recomendacao .
```

### 2. Rodar container
```bash
docker run -p 8000:8000 sistema-recomendacao
```

### Ou via Docker Compose
```bash
docker-compose up --build
```

### Acessar:
➡ http://127.0.0.1:8000

➡ http://127.0.0.1:8000/docs

---

## 🧪 Testes Automatizados
O projeto possui testes unitários para:

### ✔ Modelo de recomendação
- Similaridade
- Recomendações do Usuário

### API FastAPI
- `/`
- `/similar/{movie_id}`
- `/user/{user_id}`
- `/add/user`
- `/add/item`
- `/update/rating`

### Rodar testes:
```bash
python -m pytest -v
```

---

## 🔌 Endpoints disponíveis

### GET /
Status da API.

### GET /similar/{movie_id}
Recomenda filmes semelhantes ao título informado.

**Exemplo**  
`/similar/1`

### GET /user/{user_id}
Gera recomendações personalizadas para um usuário.

**Exemplo**  
`/user/1`

### POST /add/user
Adiciona novo usuário.

### POST /add/item
Adiciona novo filme.

### PUT /update/rating
Atualiza a nota de um usuário para um filme.

---

## 📦 Tecnologias utilizadas

- Python 3.11
- Pandas
- NumPy
- Scikit-Learn
- FastAPI
- Uvicorn
- Docker

---

## 🏁 Conclusão

Este projeto demonstra:

- ✔ Implementação completa de um sistema de recomendação

- ✔ API funcional em FastAPI

- ✔ Testes automatizados

- ✔ Conteinerização via Docker

- ✔ Organização modular

- ✔ Documentação completa

Este trabalho demonstra domínio prático de sistemas de recomendação e desenvolvimento de APIs modernas.