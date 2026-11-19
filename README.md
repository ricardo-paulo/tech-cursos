# Trabalho - Tech Cursos

A proposta do projeto é com base o protótipo mobile do app Tech Cursos, desenvolvido no Figma, criar a versão para Desktop (Windows e Linux) do Tech Cursos com adaptações e melhorias conforme necessário.

# Integrantes

Lidia Cruz de Araújo e Paulo Ricardo Rodrigues Silva

# Proposta do projeto

O **Tech Cursos** é uma aplicação desktop desenvolvido para atuar como uma plataforma para hospedagem e venda de cursos de informática online.

# Tecnologias utilizadas

| Linguagem de Programação | Python (v3.14) |
| --- | --- |
| Framework/biblioteca de Interface | PySlide6 |
| Arquiterura | MVC |
| Banco de Dados | Supabase (PostgreSQL, autenticação e armazenamento de imagens) |
| Armazenamento (vídeos) | YouTube (não listados) |
| Versionamento | Git + Github |
| Ambiente | venv |

# Estrutura

## Estrutura de Pastas

```
techcursos/
│
├── main.py
│
├── config/
│   └── database.py
│
├── models/
│   ├── usuario.py
│   ├── curso.py
│   ├── aula.py
│   └── matricula.py
│
├── repositories/
│   ├── usuario_repository.py
│   ├── curso_repository.py
│   └── matricula_repository.py
│
├── services/
│   ├── usuario_service.py
│   ├── curso_service.py
│   └── matricula_service.py
│
├── controllers/
│   ├── login_controller.py
│   ├── curso_controller.py
│   └── aluno_controller.py
│
├── views/
│   ├── login/
│   ├── home/
│   ├── cursos/
│   └── aluno/
│
├── resources/
│   ├── icons/
│   └── styles/
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Estruturação do Banco de Dados

### Tabelas

- usuario
    
    
    | Campo | Tipo | Observação |
    | --- | --- | --- |
    | id_usuario | INT | PK |
    | nome | VARCHAR(100) | Nome |
    | email | VARCHAR(150) | Único |
    | senha | VARCHAR(255) | Senha armazenada com hash |
    | tipo | VARCHAR(20) | Aluno ou Admin |
    | data_cadastro | TIMESTAMP | Data do cadastro |
- categoria
    
    
    | Campo | Tipo |
    | --- | --- |
    | id_categoria | INT |
    | nome | VARCHAR(80) |
    | descricao | TEXT |
- curso
    
    
    | Campo | Tipo | Observação |
    | --- | --- | --- |
    | id_curso | INT | PK |
    | id_categoria | INT | FK |
    | nome | VARCHAR(150) | Nome do curso |
    | descricao | TEXT | Descrição |
    | carga_horaria | INT | Horas |
    | nivel | VARCHAR(30) | Básico/Intermediário/Avançado |
    | preco | DECIMAL(10,2) | Valor |
    | ativo | BOOLEAN | Disponível ou não |
- aula
    
    
    | Campo | Tipo |
    | --- | --- |
    | id_aula | INT PK |
    | id_curso | INT FK |
    | titulo | VARCHAR(150) |
    | descricao | TEXT |
    | ordem | INT |
    | duracao_minutos | INT |
- matricula
    
    
    | Campo | Tipo |
    | --- | --- |
    | id_matricula | INT PK |
    | id_usuario | INT FK |
    | id_curso | INT FK |
    | data_matricula | TIMESTAMP |
    | status | VARCHAR(20) |
- progresso
    
    
    | Campo | Tipo |
    | --- | --- |
    | id_progresso | INT PK |
    | id_matricula | INT FK |
    | id_aula | INT FK |
    | concluida | BOOLEAN |
    | data_conclusao | TIMESTAMP |

### Relacionamentos

```
USUARIO 1 ─── N MATRICULA
CURSO   1 ─── N MATRICULA

CATEGORIA 1 ─── N CURSO

CURSO 1 ─── N AULA

MATRICULA 1 ─── N PROGRESSO
AULA       1 ─── N PROGRESSO
```

# Tarefas

- [x]  Criar documentação e planejamento iniciais.
- [x]  Criar repositório.
- [x]  Criar estrutura base de pastas.
- [x]  Criar venv e instalar bibliotecas necessárias.
- [x]  Fazer primeiro commit.
- [ ]  Criar canal no YouTube para hospedagem dos vídeos não listados.
- [ ]  Criar e configurar projeto no Supabase.