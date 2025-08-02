# GPROG API Documentation

## Visão Geral

A API do GPROG oferece endpoints RESTful para gerenciamento completo do sistema de programação musical. Todas as respostas são em formato JSON e seguem padrões REST.

## Base URL

```
http://localhost:5000/api
```

## Autenticação

Atualmente a API não requer autenticação. Em versões futuras será implementado sistema de tokens JWT.

## Formato de Resposta

### Sucesso
```json
{
  "success": true,
  "data": {...},
  "message": "Operação realizada com sucesso"
}
```

### Erro
```json
{
  "success": false,
  "error": "Descrição do erro",
  "code": 400
}
```

## Endpoints

### Categorias Musicais

#### Listar Categorias
```http
GET /api/categorias
```

**Resposta:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "codigo": "01",
      "nome": "Pop Nacional",
      "descricao": "Música pop brasileira"
    }
  ]
}
```

#### Criar Categoria
```http
POST /api/categorias
Content-Type: application/json

{
  "codigo": "06",
  "nome": "Funk Carioca",
  "descricao": "Funk carioca atual"
}
```

#### Obter Categoria
```http
GET /api/categorias/{id}
```

#### Atualizar Categoria
```http
PUT /api/categorias/{id}
Content-Type: application/json

{
  "nome": "Pop Nacional Atualizado",
  "descricao": "Nova descrição"
}
```

#### Deletar Categoria
```http
DELETE /api/categorias/{id}
```

### Estilos Musicais

#### Listar Estilos
```http
GET /api/estilos
```

#### Criar Estilo
```http
POST /api/estilos
Content-Type: application/json

{
  "nome": "Sertanejo Universitário",
  "descricao": "Estilo sertanejo moderno"
}
```

### Músicas

#### Listar Músicas
```http
GET /api/musicas?page=1&per_page=20&categoria_id=1&interprete=Anitta
```

**Parâmetros de Query:**
- `page`: Número da página (padrão: 1)
- `per_page`: Itens por página (padrão: 20, máximo: 100)
- `categoria_id`: Filtrar por categoria
- `estilo_id`: Filtrar por estilo
- `interprete`: Buscar por intérprete
- `nome_musica`: Buscar por nome da música
- `ano_lancamento`: Filtrar por ano

#### Criar Música
```http
POST /api/musicas
Content-Type: application/json

{
  "interprete1": "Anitta",
  "interprete2": "Maluma",
  "nome_musica": "Envolver",
  "tipo": "ER",
  "categoria_id": 1,
  "velocidade": 3,
  "estilo_id": 2,
  "ano_lancamento": 2022,
  "complemento": "Hit internacional",
  "tempo": "00:03:15"
}
```

**Campos obrigatórios:**
- `interprete1`: Nome do intérprete principal
- `nome_musica`: Nome da música
- `ano_lancamento`: Ano de lançamento
- `categoria_id`: ID da categoria

**Campos opcionais:**
- `interprete2`, `interprete3`: Intérpretes adicionais
- `tipo`: AC, AV, ER, RMX
- `velocidade`: 1 (lenta), 2 (média), 3 (rápida)
- `estilo_id`: ID do estilo musical
- `complemento`: Informações adicionais
- `tempo`: Duração no formato HH:MM:SS
- `data_aniversario_interprete1`, `data_aniversario_interprete2`, `data_aniversario_interprete3`: Datas de aniversário
- `rip_interprete1`, `rip_interprete2`, `rip_interprete3`: Datas de falecimento

#### Autocompletar

##### Intérpretes
```http
GET /api/musicas/autocomplete/interpretes?q=Ani
```

##### Nomes de Músicas
```http
GET /api/musicas/autocomplete/nomes?q=Envo
```

##### Complementos
```http
GET /api/musicas/autocomplete/complementos?q=Hit
```

### Locutores

#### Listar Locutores
```http
GET /api/locutores
```

#### Criar Locutor
```http
POST /api/locutores
Content-Type: application/json

{
  "codigo": "LOC001",
  "nome": "João Silva",
  "status": "Ativo",
  "observacoes": "Locutor principal do matutino"
}
```

### Emissoras

#### Listar Emissoras
```http
GET /api/emissoras
```

#### Criar Emissora
```http
POST /api/emissoras
Content-Type: application/json

{
  "codigo": "RN001",
  "nome": "Rádio Nativa FM",
  "frequencia": "105.7",
  "cidade": "São Paulo",
  "estado": "SP",
  "status": "Ativa",
  "observacoes": "Emissora principal"
}
```

### Relacionamento Locutor-Emissora

#### Listar Relacionamentos
```http
GET /api/locutor-emissora
```

#### Criar Relacionamento
```http
POST /api/locutor-emissora
Content-Type: application/json

{
  "locutor_id": 1,
  "emissora_id": 1,
  "data_inicio": "2025-01-01",
  "data_fim": null,
  "observacoes": "Contrato principal"
}
```

#### Emissoras de um Locutor
```http
GET /api/locutores/{id}/emissoras
```

#### Locutores de uma Emissora
```http
GET /api/emissoras/{id}/locutores
```

### Banco de Locuções

#### Listar Locuções
```http
GET /api/banco-locucoes
```

#### Criar Locução
```http
POST /api/banco-locucoes
Content-Type: application/json

{
  "emissora_id": 1,
  "locutor_id": 1,
  "interprete": "Anitta",
  "velocidade": 3,
  "texto_locucao": "Agora você vai ouvir Anitta na Rádio Nativa FM",
  "observacoes": "Locução para horário nobre"
}
```

#### Endpoints Auxiliares

##### Emissoras Disponíveis
```http
GET /api/banco-locucoes/emissoras
```

##### Locutores de uma Emissora
```http
GET /api/banco-locucoes/emissoras/{id}/locutores
```

##### Intérpretes (ordem alfabética)
```http
GET /api/banco-locucoes/interpretes
```

##### Buscar Intérpretes
```http
GET /api/banco-locucoes/interpretes/search?q=Ani
```

##### Velocidades Disponíveis
```http
GET /api/banco-locucoes/velocidades
```

**Resposta:**
```json
{
  "success": true,
  "data": [
    {"id": 1, "nome": "Muito Lenta"},
    {"id": 2, "nome": "Lenta"},
    {"id": 3, "nome": "Normal"},
    {"id": 4, "nome": "Rápida"},
    {"id": 5, "nome": "Muito Rápida"}
  ]
}
```

## Códigos de Status HTTP

- `200 OK`: Operação bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `400 Bad Request`: Dados inválidos
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro interno do servidor

## Paginação

Para endpoints que retornam listas, a paginação é suportada:

```http
GET /api/musicas?page=2&per_page=50
```

**Resposta com paginação:**
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 2,
    "per_page": 50,
    "total": 1250,
    "pages": 25,
    "has_next": true,
    "has_prev": true
  }
}
```

## Filtros e Busca

Muitos endpoints suportam filtros via parâmetros de query:

```http
GET /api/musicas?categoria_id=1&ano_lancamento=2022&interprete=Anitta
```

## Exemplos de Uso com cURL

### Criar uma categoria
```bash
curl -X POST http://localhost:5000/api/categorias \
  -H "Content-Type: application/json" \
  -d '{"codigo": "06", "nome": "Funk Carioca", "descricao": "Funk carioca atual"}'
```

### Buscar músicas por intérprete
```bash
curl "http://localhost:5000/api/musicas?interprete=Anitta&page=1&per_page=10"
```

### Criar uma locução
```bash
curl -X POST http://localhost:5000/api/banco-locucoes \
  -H "Content-Type: application/json" \
  -d '{
    "emissora_id": 1,
    "locutor_id": 1,
    "interprete": "Anitta",
    "velocidade": 3,
    "texto_locucao": "Agora você vai ouvir Anitta na Rádio Nativa FM"
  }'
```

## Versionamento

A API atual é a versão 1.0. Futuras versões serão versionadas na URL:

```
/api/v2/categorias
```

## Rate Limiting

Atualmente não há limitação de taxa. Em produção será implementado rate limiting para proteger a API.

## Suporte

Para dúvidas sobre a API, consulte a documentação completa ou abra uma issue no repositório GitHub.

