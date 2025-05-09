# 🚀 FastAPI CRUD Usuários

Projeto de portfólio com foco em desenvolvimento back-end utilizando **FastAPI**. Esta API realiza operações CRUD (Create, Read, Update, Delete) de usuários, com autenticação via **JWT**, logs de atividades e boas práticas de organização e segurança.

> ⚠️ Projeto em desenvolvimento — novas funcionalidades serão incluídas em breve (paginação avançada, documentação Swagger aprimorada, testes mais robustos, entre outras melhorias).

---

## 🛠 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- SQLite
- SQLAlchemy
- Pydantic
- Pytest (testes automatizados)
- JWT (autenticação)
- Docker
- Logging
- .env (para variáveis de ambiente)

---

## 📌 Funcionalidades Implementadas

- ✅ Cadastro de usuários
- ✅ Login com geração de token JWT
- ✅ Listagem de usuários com autenticação
- ✅ Atualização e exclusão de usuários autenticados
- ✅ Logs de ações (em terminal e arquivo `app.log`)
- ✅ Proteção de rotas com autenticação
- ✅ Criação de perfil admin com permissões restritas
- ✅ Deploy com Docker e Docker Hub

---

## 📦 Como rodar o projeto

### Requisitos

- Python 3.10+
- Docker instalado (opcional, mas recomendado)

### Clonando o projeto

```bash
git clone https://github.com/seu-usuario/fastapi-crud-usuarios.git
cd fastapi-crud-usuarios
```

### Rodando com Docker

```bash
docker build -t fastapi-crud-usuarios .
docker run -d -p 8000:8000 fastapi-crud-usuarios
```

### Acessar API no navegador:

```
http://localhost:8000/docs
```

---

## 🧪 Executar Testes

```bash
pytest
```

---

## 📁 Estrutura do Projeto (resumida)

```
.
├── .db                           # Arquivos de banco de dados, como o `app.db` (geralmente o banco SQLite)
├── .github                       # Diretório com arquivos de configuração do GitHub Actions (CI/CD)
│   └── workflows                 # Fluxos de trabalho (workflow) do GitHub Actions
├── api                            # Diretório para a API
│   └── v1                         # Versão da API (v1 no caso)
│       └── endpoints              # Endpoints da API
│           └── __pycache__        # Arquivos compilados do Python
├── app.db                         # Arquivo de banco de dados (provavelmente SQLite)
├── core                           # Módulo principal do aplicativo
│   └── __pycache__                # Arquivos compilados do Python
├── models                         # Definições de modelos (como a definição de usuários)
│   └── __pycache__                # Arquivos compilados do Python
├── schemas                        # Definições de esquemas para validação (Pydantic)
│   └── __pycache__                # Arquivos compilados do Python
├── scripts                        # Scripts auxiliares (geralmente para migrações ou utilitários)
├── services                       # Lógica de serviços (como a criação de usuários, autenticação etc.)
│   └── __pycache__                # Arquivos compilados do Python
├── tests                          # Testes automatizados
├── utils                          # Funções e utilitários auxiliares
│   └── __pycache__                # Arquivos compilados do Python
└── __pycache__     
```

---

## 📌 Melhorias Futuras

- 🔧 Paginação com filtros e ordenação
- 🔒 Autorização mais avançada (perfis e papéis)
- 📄 Swagger + exemplos de requisição
- 📂 Modularização de pastas
- 🐳 CI com Docker + Testes automatizados
- ✨ Interface Web para interagir com a API (front-end ainda não implementado)

---

## 👨‍💻 Autor

**Iago Alves** — [@IagoAlves1](https://github.com/IagoAlves1)

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
