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

O sistema recomenda:

- Filmes semelhantes a um filme específico  
- Filmes personalizados para um usuário baseado no histórico de avaliações  

---

## 🏗️ Arquitetura da Solução


│ ├── main.py → API FastAPI
│ ├── model.py → Modelo de recomendação
│ └── init.py
│
├── data/
│ └── ml-latest-small/ → Dataset MovieLens
│
├── test_model.py → Testes do modelo
├── check_dataset.py → Teste de leitura do dataset
│
├── Dockerfile → Container Docker
├── requirements.txt → Dependências
└── README.md → Documentação

---

## 🤖 Modelo de Recomendação

Foi utilizada a técnica de **Filtragem Colaborativa Baseada em Itens (Item-Based Collaborative Filtering)**.

### **Etapas do modelo:**

1. Carregar notas dos usuários (`ratings.csv`)  
2. Construir matriz usuário x filme  
3. Transpor matriz (filme x usuário)  
4. Calcular **cosine_similarity** entre filmes  
5. Recomendar:  
   - **similaridade entre filmes**  
   - **filmes para um usuário específico** (somatório ponderado de similaridade)

---

## 🚀 Como rodar o projeto (local)

### 1. Criar ambiente virtual
```bash
python -m venv .venv
.\.venv\Scripts\activate

---

### 2. Instalar dependências
pip install -r requirements.txt

### 3. Rodar a API
uvicorn app.main:app --reload

Acessar:
➡ http://127.0.0.1:8000

➡ http://127.0.0.1:8000/docs

## 🐳 Como rodar o projeto via Docker

1. Construir imagem
docker build -t sistema-recomendacao .

2. Rodar container
docker run -p 8000:8000 sistema-recomendacao


Acessar:
➡ http://127.0.0.1:8000

➡ http://127.0.0.1:8000/docs

🧪 Endpoints
GET /

Status da API

GET /similar/{movie_id}

Recomenda filmes semelhantes.

Exemplo:

/similar/1

GET /user/{user_id}

Recomenda filmes personalizados para um usuário.

Exemplo:

/user/1

📦 Tecnologias utilizadas

Python 3.11

Pandas

NumPy

Scikit-Learn

FastAPI

Uvicorn

Docker

🏁 Conclusão

O projeto entrega:

Modelo de recomendação funcional e eficiente

API totalmente operacional com FastAPI

Container Docker permitindo portabilidade total

Código organizado, comentado e modular

Este trabalho demonstra domínio prático de sistemas de recomendação e desenvolvimento de APIs modernas.