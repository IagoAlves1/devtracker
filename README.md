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
git clone https://github.com/IagoAlves1/fastapi-crud-usuarios.git
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
├── .github                       # Diretório com arquivos de configuração do GitHub Actions (CI/CD)
│   └── workflows                 # Fluxos de trabalho (workflow) do GitHub Actions
├── api                            # Diretório para a API
│   └── v1                         # Versão da API
│       └── endpoints              # Endpoints da API
│           └── __pycache__        # Arquivos compilados do Python
├── core                           # Módulo principal do aplicativo
├── models                         # Definições de modelos (definição de usuários)
├── schemas                        # Definições de esquemas para validação (Pydantic)
├── scripts                        # Scripts auxiliares (geralmente para migrações ou utilitários)
├── services                       # Lógica de serviços (como a criação de usuários, autenticação etc.)
├── tests                          # Testes automatizados
├── utils                          # Funções e utilitários auxiliares
```

---

## 📌 Melhorias Futuras

- 🔧 Paginação com filtros e ordenação
- 🔒 Autorização mais avançada (perfis e papéis)
- 📄 Swagger + exemplos de requisição
- ✨ Interface Web para interagir com a API (front-end ainda não implementado)

---

## 👨‍💻 Autor

**Iago Alves** — [@IagoAlves1](https://github.com/IagoAlves1)

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
