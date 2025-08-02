# GPROG - Sistema de Programação Musical

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3+-green.svg)
![SQLite](https://img.shields.io/badge/sqlite-v3+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Sistema completo para gerenciamento e geração de programação musical para rádios, desenvolvido com Flask e interface web amigável. O GPROG oferece uma solução robusta para emissoras de rádio que precisam organizar, catalogar e gerar programações musicais de forma automatizada e eficiente.

## 🎵 Visão Geral

O GPROG (Sistema de Programação Musical) é uma aplicação web desenvolvida especificamente para atender às necessidades das emissoras de rádio modernas. Com uma arquitetura baseada em APIs REST e uma interface intuitiva, o sistema permite o gerenciamento completo do acervo musical, locutores, emissoras e a geração automatizada de programações.

### Principais Características

- **Gestão Completa de Acervo Musical**: Cadastro detalhado de músicas com múltiplos intérpretes, categorias, estilos e metadados
- **Gerenciamento de Locutores e Emissoras**: Sistema completo para cadastro e relacionamento entre locutores e emissoras
- **Banco de Locuções Personalizadas**: Criação e organização de locuções específicas por emissora e locutor
- **APIs REST Completas**: Interface programática para integração com outros sistemas
- **Interface Web Responsiva**: Frontend moderno e intuitivo para operação diária
- **Sistema de Autocompletar**: Facilita a entrada de dados com sugestões inteligentes

## 🚀 Funcionalidades Implementadas

### 1. Cadastro de Categorias Musicais
O sistema oferece um módulo completo para gerenciamento de categorias musicais, permitindo a classificação organizada do acervo. Cada categoria possui código único e nome obrigatórios, facilitando a organização e busca posterior.

**Características:**
- CRUD completo (Create, Read, Update, Delete)
- Código único para identificação
- Descrição opcional para detalhamento
- API REST disponível em `/api/categorias`

### 2. Gestão de Estilos Musicais
Sistema robusto para catalogação de estilos musicais, permitindo uma classificação mais granular do acervo musical da emissora.

**Características:**
- Cadastro de estilos pré-definidos
- Associação com músicas do acervo
- API REST em `/api/estilos`
- Interface de busca e filtros

### 3. Cadastro Avançado de Músicas
Módulo principal do sistema, oferecendo cadastro detalhado de músicas com múltiplos campos e funcionalidades avançadas.

**Campos Obrigatórios:**
- Nome do Intérprete Principal
- Nome da Música
- Ano de Lançamento
- Categoria Musical

**Campos Opcionais:**
- Intérprete 2 e Intérprete 3
- Tipo de Gravação (AC-Acústico, AV-Ao Vivo, ER-Edit Radio, RMX-Remix)
- Velocidade da Música (1-Lenta, 2-Média, 3-Rápida)
- Estilo Musical
- Complemento (campo livre com memorização)
- Tempo de Duração
- Datas de Aniversário dos Intérpretes
- Data RIP (se aplicável)

**Funcionalidades Especiais:**
- Sistema de autocompletar para intérpretes, nomes de músicas e complementos
- Paginação inteligente para grandes acervos
- Filtros avançados de busca
- API REST completa em `/api/musicas`

### 4. Gerenciamento de Locutores
Sistema completo para cadastro e gerenciamento de locutores da emissora.

**Características:**
- Código único de identificação
- Nome completo
- Status (Ativo/Inativo)
- Campo de observações
- Histórico de atividades
- API REST em `/api/locutores`

### 5. Cadastro de Emissoras
Módulo para gerenciamento de múltiplas emissoras no sistema.

**Informações Cadastrais:**
- Código único da emissora
- Nome/Razão social
- Frequência de transmissão
- Cidade e Estado
- Status operacional (Ativa/Inativa)
- Observações gerais
- API REST em `/api/emissoras`

### 6. Relacionamento Locutor-Emissora
Sistema avançado para associação entre locutores e emissoras, permitindo controle temporal das associações.

**Funcionalidades:**
- Associação múltipla (um locutor pode trabalhar em várias emissoras)
- Controle de período (data início/fim)
- Histórico de relacionamentos
- Consultas específicas por locutor ou emissora
- API REST em `/api/locutor-emissora`

### 7. Banco de Locuções Personalizadas
Sistema inovador para criação e organização de locuções específicas por emissora e locutor.

**Fluxo de Trabalho:**
1. Seleção da Emissora
2. Escolha do Locutor (baseado na associação)
3. Seleção do Intérprete (ordem alfabética do acervo)
4. Definição da Velocidade de Locução (1-5)
5. Criação do texto da locução

**Características:**
- Intérpretes listados em ordem alfabética
- Controle de velocidade (1=Muito Lenta a 5=Muito Rápida)
- Campo livre para texto da locução
- Sistema de busca de intérpretes
- API REST completa em `/api/banco-locucoes`

## 🏗️ Arquitetura do Sistema

### Estrutura de Diretórios

```
gprog/
├── src/                          # Código fonte principal
│   ├── models/                   # Modelos de dados SQLAlchemy
│   │   ├── user.py              # Modelo de usuário
│   │   └── programacao.py       # Modelos do sistema musical
│   ├── routes/                   # Rotas da API REST
│   │   ├── user.py              # Rotas de usuário
│   │   ├── categorias.py        # API de categorias
│   │   ├── estilos.py           # API de estilos
│   │   ├── musicas.py           # API de músicas
│   │   ├── locutores.py         # API de locutores
│   │   ├── emissoras.py         # API de emissoras
│   │   ├── locutor_emissora.py  # API de relacionamentos
│   │   └── banco_locucoes.py    # API de locuções
│   ├── static/                   # Arquivos estáticos (frontend)
│   │   ├── index.html           # Interface principal
│   │   └── favicon.ico          # Ícone da aplicação
│   ├── database/                 # Banco de dados
│   │   └── app.db              # Banco SQLite
│   └── main.py                  # Aplicação Flask principal
├── docs/                        # Documentação
├── scripts/                     # Scripts utilitários
├── tests/                       # Testes automatizados
├── init_data.py                 # Script de inicialização
├── database_schema.sql          # Schema do banco de dados
├── requirements.txt             # Dependências Python
└── README.md                    # Esta documentação
```

### Tecnologias Utilizadas

**Backend:**
- **Flask 2.3+**: Framework web principal
- **SQLAlchemy**: ORM para banco de dados
- **Flask-CORS**: Suporte a Cross-Origin Resource Sharing
- **Python 3.11+**: Linguagem de programação

**Banco de Dados:**
- **SQLite**: Banco de dados para desenvolvimento
- **Suporte futuro**: PostgreSQL/MySQL para produção

**Frontend:**
- **HTML5/CSS3**: Interface web responsiva
- **JavaScript**: Interatividade e consumo de APIs
- **Bootstrap**: Framework CSS (planejado)

**APIs:**
- **REST JSON**: Padrão de comunicação
- **Swagger/OpenAPI**: Documentação (planejado)

## 📋 APIs Disponíveis

### Categorias Musicais
- `GET /api/categorias` - Listar todas as categorias
- `POST /api/categorias` - Criar nova categoria
- `GET /api/categorias/{id}` - Obter categoria específica
- `PUT /api/categorias/{id}` - Atualizar categoria
- `DELETE /api/categorias/{id}` - Deletar categoria

### Estilos Musicais
- `GET /api/estilos` - Listar todos os estilos
- `POST /api/estilos` - Criar novo estilo
- `GET /api/estilos/{id}` - Obter estilo específico
- `PUT /api/estilos/{id}` - Atualizar estilo
- `DELETE /api/estilos/{id}` - Deletar estilo

### Músicas
- `GET /api/musicas` - Listar músicas (com paginação e filtros)
- `POST /api/musicas` - Criar nova música
- `GET /api/musicas/{id}` - Obter música específica
- `PUT /api/musicas/{id}` - Atualizar música
- `DELETE /api/musicas/{id}` - Deletar música

### Autocompletar
- `GET /api/musicas/autocomplete/interpretes?q={query}` - Buscar intérpretes
- `GET /api/musicas/autocomplete/nomes?q={query}` - Buscar nomes de músicas
- `GET /api/musicas/autocomplete/complementos?q={query}` - Buscar complementos

### Locutores
- `GET /api/locutores` - Listar todos os locutores
- `POST /api/locutores` - Criar novo locutor
- `GET /api/locutores/{id}` - Obter locutor específico
- `PUT /api/locutores/{id}` - Atualizar locutor
- `DELETE /api/locutores/{id}` - Deletar locutor

### Emissoras
- `GET /api/emissoras` - Listar todas as emissoras
- `POST /api/emissoras` - Criar nova emissora
- `GET /api/emissoras/{id}` - Obter emissora específica
- `PUT /api/emissoras/{id}` - Atualizar emissora
- `DELETE /api/emissoras/{id}` - Deletar emissora

### Relacionamento Locutor-Emissora
- `GET /api/locutor-emissora` - Listar todos os relacionamentos
- `POST /api/locutor-emissora` - Criar novo relacionamento
- `GET /api/locutor-emissora/{id}` - Obter relacionamento específico
- `PUT /api/locutor-emissora/{id}` - Atualizar relacionamento
- `DELETE /api/locutor-emissora/{id}` - Deletar relacionamento
- `GET /api/locutores/{id}/emissoras` - Emissoras de um locutor
- `GET /api/emissoras/{id}/locutores` - Locutores de uma emissora

### Banco de Locuções
- `GET /api/banco-locucoes` - Listar todas as locuções
- `POST /api/banco-locucoes` - Criar nova locução
- `GET /api/banco-locucoes/{id}` - Obter locução específica
- `PUT /api/banco-locucoes/{id}` - Atualizar locução
- `DELETE /api/banco-locucoes/{id}` - Deletar locução
- `GET /api/banco-locucoes/emissoras` - Emissoras disponíveis
- `GET /api/banco-locucoes/emissoras/{id}/locutores` - Locutores da emissora
- `GET /api/banco-locucoes/interpretes` - Intérpretes em ordem alfabética
- `GET /api/banco-locucoes/interpretes/search?q={query}` - Buscar intérpretes
- `GET /api/banco-locucoes/velocidades` - Velocidades disponíveis (1-5)

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git (para clonagem do repositório)

### Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/GP857/gprog.git
cd gprog
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Inicialize o banco de dados:**
```bash
python init_data.py
```

5. **Execute a aplicação:**
```bash
python src/main.py
```

A aplicação estará disponível em: http://localhost:5000

### Configuração de Desenvolvimento

Para desenvolvimento, recomenda-se:

1. **Configurar variáveis de ambiente:**
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

2. **Executar em modo debug:**
```bash
python src/main.py
```

## 📖 Exemplos de Uso

### Criar uma Categoria Musical
```bash
curl -X POST http://localhost:5000/api/categorias \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "06",
    "nome": "Funk Carioca",
    "descricao": "Funk carioca atual e clássico"
  }'
```

### Cadastrar uma Música
```bash
curl -X POST http://localhost:5000/api/musicas \
  -H "Content-Type: application/json" \
  -d '{
    "interprete1": "Anitta",
    "nome_musica": "Envolver",
    "ano_lancamento": 2022,
    "categoria_id": 1,
    "tipo": "ER",
    "velocidade": 3,
    "estilo_id": 2
  }'
```

### Criar um Locutor
```bash
curl -X POST http://localhost:5000/api/locutores \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "LOC001",
    "nome": "João Silva",
    "status": "Ativo",
    "observacoes": "Locutor principal do matutino"
  }'
```

### Cadastrar uma Emissora
```bash
curl -X POST http://localhost:5000/api/emissoras \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "RN001",
    "nome": "Rádio Nativa FM",
    "frequencia": "105.7",
    "cidade": "São Paulo",
    "estado": "SP",
    "status": "Ativa"
  }'
```

### Criar uma Locução
```bash
curl -X POST http://localhost:5000/api/banco-locucoes \
  -H "Content-Type: application/json" \
  -d '{
    "emissora_id": 1,
    "locutor_id": 1,
    "interprete": "Anitta",
    "velocidade": 3,
    "texto_locucao": "Agora você vai ouvir Anitta na Rádio Nativa FM",
    "observacoes": "Locução para horário nobre"
  }'
```

## 🔮 Roadmap de Desenvolvimento

### Funcionalidades Planejadas

#### Fase 1 - Programação Automatizada
- **Grades de Programação**: Sistema para definir sequência de categorias por dia da semana
- **Horários de Intervalos**: Configuração de blocos comerciais e musicais
- **Algoritmo de Geração**: Motor inteligente para gerar programação diária
- **Regras de Repetição**: Controle de intervalo entre repetições de músicas

#### Fase 2 - Conteúdo Adicional
- **Vinhetas e Trilhas**: Cadastro e gerenciamento de vinhetas institucionais
- **Comerciais**: Sistema para inserção de blocos comerciais
- **Spots Promocionais**: Gerenciamento de conteúdo promocional
- **Integração de Áudio**: Suporte a arquivos de áudio

#### Fase 3 - Interface e Usabilidade
- **Interface Web Avançada**: Frontend moderno com React/Vue.js
- **Calendário Interativo**: Seleção visual de datas para programação
- **Dashboard Executivo**: Painéis com métricas e estatísticas
- **Sistema de Usuários**: Controle de acesso e permissões

#### Fase 4 - Relatórios e Analytics
- **Relatórios Detalhados**: Análises de programação e performance
- **Estatísticas de Execução**: Métricas de reprodução por música/artista
- **Exportação de Dados**: Relatórios em PDF, Excel e outros formatos
- **Integração com Analytics**: Conexão com ferramentas de análise

#### Fase 5 - Integração e Automação
- **API de Automação**: Integração com sistemas de automação de rádio
- **Sincronização em Tempo Real**: Atualizações automáticas de programação
- **Backup Automático**: Sistema de backup e recuperação
- **Notificações**: Alertas e notificações por email/SMS

## 🧪 Testes

### Executar Testes
```bash
# Instalar dependências de teste
pip install pytest pytest-cov

# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=src
```

### Estrutura de Testes
```
tests/
├── test_models.py           # Testes dos modelos
├── test_routes.py           # Testes das rotas
├── test_api.py              # Testes de integração da API
└── conftest.py              # Configurações de teste
```

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes de Contribuição
- Siga o padrão PEP 8 para código Python
- Adicione testes para novas funcionalidades
- Atualize a documentação quando necessário
- Use mensagens de commit descritivas

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Equipe

- **Desenvolvedor Principal**: GP857
- **Arquitetura**: Sistema modular baseado em Flask
- **Banco de Dados**: SQLAlchemy ORM

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Entre em contato através do perfil do desenvolvedor

## 🔄 Changelog

### Versão Atual (v1.0.0)
- ✅ Sistema completo de cadastro de músicas
- ✅ Gerenciamento de categorias e estilos
- ✅ Cadastro de locutores e emissoras
- ✅ Sistema de relacionamento locutor-emissora
- ✅ Banco de locuções personalizadas
- ✅ APIs REST completas
- ✅ Sistema de autocompletar
- ✅ Interface web básica

### Próximas Versões
- 🔄 Interface web avançada
- 🔄 Sistema de programação automatizada
- 🔄 Relatórios e analytics
- 🔄 Sistema de usuários e permissões

---

**GPROG** - Transformando a gestão de programação musical para rádios modernas.

