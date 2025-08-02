-- Sistema de Programação Musical
-- Esquema do Banco de Dados

-- Tabela de Categorias
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Estilos (pré-cadastrados)
CREATE TABLE estilos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Músicas
CREATE TABLE musicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    interprete1 VARCHAR(255) NOT NULL,
    interprete2 VARCHAR(255),
    interprete3 VARCHAR(255),
    nome_musica VARCHAR(255) NOT NULL,
    tipo VARCHAR(10) CHECK (tipo IN ('AC', 'AV', 'ER', 'RMX')),
    categoria_id INTEGER REFERENCES categorias(id),
    velocidade INTEGER CHECK (velocidade IN (1, 2, 3)), -- 1=lenta, 2=media, 3=rapida
    estilo_id INTEGER REFERENCES estilos(id),
    ano_lancamento INTEGER CHECK (ano_lancamento >= 1900 AND ano_lancamento <= 2100),
    complemento TEXT,
    data_aniversario_interprete1 DATE,
    data_aniversario_interprete2 DATE,
    data_aniversario_interprete3 DATE,
    duracao_padrao TIME DEFAULT '00:03:30', -- duração padrão para quando não especificada
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Grades de Programação
CREATE TABLE grades_programacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    todos_dias BOOLEAN DEFAULT FALSE,
    segunda_sexta BOOLEAN DEFAULT FALSE,
    terca BOOLEAN DEFAULT FALSE,
    quarta BOOLEAN DEFAULT FALSE,
    quinta BOOLEAN DEFAULT FALSE,
    sexta BOOLEAN DEFAULT FALSE,
    sabado BOOLEAN DEFAULT FALSE,
    domingo BOOLEAN DEFAULT FALSE,
    fim_semana BOOLEAN DEFAULT FALSE,
    ativa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Sequência de Categorias na Grade
CREATE TABLE grade_sequencia_categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade_id INTEGER REFERENCES grades_programacao(id) ON DELETE CASCADE,
    categoria_id INTEGER REFERENCES categorias(id),
    ordem INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Horários de Intervalos (Blocos)
CREATE TABLE horarios_intervalos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade_id INTEGER REFERENCES grades_programacao(id) ON DELETE CASCADE,
    hora TIME NOT NULL,
    tipo VARCHAR(2) CHECK (tipo IN ('BC', 'BM')), -- BC=Break Comercial, BM=Bloco Musical
    duracao TIME NOT NULL,
    ordem INTEGER NOT NULL, -- ordem dentro da mesma hora
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Vinhetas
CREATE TABLE vinhetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(10) DEFAULT 'VH',
    nome VARCHAR(255) NOT NULL,
    tipo VARCHAR(100),
    tempo TIME,
    tempo_digitado TIME, -- caso o tempo seja digitado manualmente
    arquivo_audio VARCHAR(500), -- caminho do arquivo (para futuro uso)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Trilhas
CREATE TABLE trilhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(10) DEFAULT 'TR',
    nome VARCHAR(255) NOT NULL,
    tipo VARCHAR(100),
    tempo TIME,
    tempo_digitado TIME, -- caso o tempo seja digitado manualmente
    arquivo_audio VARCHAR(500), -- caminho do arquivo (para futuro uso)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Comerciais
CREATE TABLE comerciais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(10) DEFAULT 'COM',
    titulo VARCHAR(255) NOT NULL,
    cliente VARCHAR(255) NOT NULL,
    tempo TIME,
    tempo_digitado TIME, -- caso o tempo seja digitado manualmente
    arquivo_audio VARCHAR(500), -- caminho do arquivo (para futuro uso)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Complementos para Músicas (para memorizar digitações futuras)
CREATE TABLE complementos_musicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complemento VARCHAR(255) NOT NULL UNIQUE,
    usado_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Intérpretes (para memorizar digitações futuras)
CREATE TABLE interpretes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL UNIQUE,
    usado_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Nomes de Músicas (para memorizar digitações futuras)
CREATE TABLE nomes_musicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL UNIQUE,
    usado_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Programação Gerada (histórico das programações)
CREATE TABLE programacao_gerada (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_programacao DATE NOT NULL,
    grade_id INTEGER REFERENCES grades_programacao(id),
    conteudo_json TEXT, -- JSON com a programação completa do dia
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhor performance
CREATE INDEX idx_musicas_categoria ON musicas(categoria_id);
CREATE INDEX idx_musicas_estilo ON musicas(estilo_id);
CREATE INDEX idx_musicas_velocidade ON musicas(velocidade);
CREATE INDEX idx_musicas_ano ON musicas(ano_lancamento);
CREATE INDEX idx_grade_sequencia_grade ON grade_sequencia_categorias(grade_id);
CREATE INDEX idx_horarios_grade ON horarios_intervalos(grade_id);
CREATE INDEX idx_horarios_hora ON horarios_intervalos(hora);
CREATE INDEX idx_programacao_data ON programacao_gerada(data_programacao);

-- Inserção de dados iniciais
INSERT INTO estilos (nome) VALUES 
('Pop'), ('Rock'), ('MPB'), ('Sertanejo'), ('Funk'), ('Eletrônica'), 
('Jazz'), ('Blues'), ('Reggae'), ('Hip Hop'), ('R&B'), ('Country'),
('Folk'), ('Classical'), ('Gospel'), ('Forró'), ('Axé'), ('Pagode'),
('Samba'), ('Bossa Nova');

-- Exemplo de categoria inicial
INSERT INTO categorias (codigo, nome, descricao) VALUES 
('01', 'Internacional Lenta FB', 'Músicas internacionais lentas para Facebook');

