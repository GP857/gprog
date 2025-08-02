from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
import json

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    musicas = db.relationship('Musica', backref='categoria', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'descricao': self.descricao,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Estilo(db.Model):
    __tablename__ = 'estilos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    musicas = db.relationship('Musica', backref='estilo', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Musica(db.Model):
    __tablename__ = 'musicas'
    
    id = db.Column(db.Integer, primary_key=True)
    interprete1 = db.Column(db.String(255), nullable=False)
    interprete2 = db.Column(db.String(255))
    interprete3 = db.Column(db.String(255))
    nome_musica = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(10))  # AC, AV, ER, RMX
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    velocidade = db.Column(db.Integer)  # 1=lenta, 2=media, 3=rapida
    estilo_id = db.Column(db.Integer, db.ForeignKey('estilos.id'))
    ano_lancamento = db.Column(db.Integer)
    complemento = db.Column(db.Text)
    data_aniversario_interprete1 = db.Column(db.Date)
    data_aniversario_interprete2 = db.Column(db.Date)
    data_aniversario_interprete3 = db.Column(db.Date)
    duracao_padrao = db.Column(db.Time, default=time(0, 3, 30))  # 3:30 padrão
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'interprete1': self.interprete1,
            'interprete2': self.interprete2,
            'interprete3': self.interprete3,
            'nome_musica': self.nome_musica,
            'tipo': self.tipo,
            'categoria_id': self.categoria_id,
            'categoria': self.categoria.to_dict() if self.categoria else None,
            'velocidade': self.velocidade,
            'estilo_id': self.estilo_id,
            'estilo': self.estilo.to_dict() if self.estilo else None,
            'ano_lancamento': self.ano_lancamento,
            'complemento': self.complemento,
            'data_aniversario_interprete1': self.data_aniversario_interprete1.isoformat() if self.data_aniversario_interprete1 else None,
            'data_aniversario_interprete2': self.data_aniversario_interprete2.isoformat() if self.data_aniversario_interprete2 else None,
            'data_aniversario_interprete3': self.data_aniversario_interprete3.isoformat() if self.data_aniversario_interprete3 else None,
            'duracao_padrao': self.duracao_padrao.strftime('%H:%M:%S') if self.duracao_padrao else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class GradeProgramacao(db.Model):
    __tablename__ = 'grades_programacao'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    todos_dias = db.Column(db.Boolean, default=False)
    segunda_sexta = db.Column(db.Boolean, default=False)
    terca = db.Column(db.Boolean, default=False)
    quarta = db.Column(db.Boolean, default=False)
    quinta = db.Column(db.Boolean, default=False)
    sexta = db.Column(db.Boolean, default=False)
    sabado = db.Column(db.Boolean, default=False)
    domingo = db.Column(db.Boolean, default=False)
    fim_semana = db.Column(db.Boolean, default=False)
    ativa = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    sequencia_categorias = db.relationship('GradeSequenciaCategoria', backref='grade', lazy=True, cascade='all, delete-orphan')
    horarios_intervalos = db.relationship('HorarioIntervalo', backref='grade', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'todos_dias': self.todos_dias,
            'segunda_sexta': self.segunda_sexta,
            'terca': self.terca,
            'quarta': self.quarta,
            'quinta': self.quinta,
            'sexta': self.sexta,
            'sabado': self.sabado,
            'domingo': self.domingo,
            'fim_semana': self.fim_semana,
            'ativa': self.ativa,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'sequencia_categorias': [seq.to_dict() for seq in self.sequencia_categorias],
            'horarios_intervalos': [h.to_dict() for h in self.horarios_intervalos]
        }

class GradeSequenciaCategoria(db.Model):
    __tablename__ = 'grade_sequencia_categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades_programacao.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    ordem = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    categoria = db.relationship('Categoria', backref='grade_sequencias')
    
    def to_dict(self):
        return {
            'id': self.id,
            'grade_id': self.grade_id,
            'categoria_id': self.categoria_id,
            'categoria': self.categoria.to_dict() if self.categoria else None,
            'ordem': self.ordem,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class HorarioIntervalo(db.Model):
    __tablename__ = 'horarios_intervalos'
    
    id = db.Column(db.Integer, primary_key=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades_programacao.id'), nullable=False)
    hora = db.Column(db.Time, nullable=False)
    tipo = db.Column(db.String(2), nullable=False)  # BC=Break Comercial, BM=Bloco Musical
    duracao = db.Column(db.Time, nullable=False)
    ordem = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'grade_id': self.grade_id,
            'hora': self.hora.strftime('%H:%M:%S') if self.hora else None,
            'tipo': self.tipo,
            'duracao': self.duracao.strftime('%H:%M:%S') if self.duracao else None,
            'ordem': self.ordem,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Vinheta(db.Model):
    __tablename__ = 'vinhetas'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), default='VH')
    nome = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(100))
    tempo = db.Column(db.Time)
    tempo_digitado = db.Column(db.Time)
    arquivo_audio = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'tipo': self.tipo,
            'tempo': self.tempo.strftime('%H:%M:%S') if self.tempo else None,
            'tempo_digitado': self.tempo_digitado.strftime('%H:%M:%S') if self.tempo_digitado else None,
            'arquivo_audio': self.arquivo_audio,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Trilha(db.Model):
    __tablename__ = 'trilhas'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), default='TR')
    nome = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(100))
    tempo = db.Column(db.Time)
    tempo_digitado = db.Column(db.Time)
    arquivo_audio = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'tipo': self.tipo,
            'tempo': self.tempo.strftime('%H:%M:%S') if self.tempo else None,
            'tempo_digitado': self.tempo_digitado.strftime('%H:%M:%S') if self.tempo_digitado else None,
            'arquivo_audio': self.arquivo_audio,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Comercial(db.Model):
    __tablename__ = 'comerciais'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), default='COM')
    titulo = db.Column(db.String(255), nullable=False)
    cliente = db.Column(db.String(255), nullable=False)
    tempo = db.Column(db.Time)
    tempo_digitado = db.Column(db.Time)
    arquivo_audio = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'titulo': self.titulo,
            'cliente': self.cliente,
            'tempo': self.tempo.strftime('%H:%M:%S') if self.tempo else None,
            'tempo_digitado': self.tempo_digitado.strftime('%H:%M:%S') if self.tempo_digitado else None,
            'arquivo_audio': self.arquivo_audio,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ComplementoMusica(db.Model):
    __tablename__ = 'complementos_musicas'
    
    id = db.Column(db.Integer, primary_key=True)
    complemento = db.Column(db.String(255), unique=True, nullable=False)
    usado_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'complemento': self.complemento,
            'usado_count': self.usado_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Interprete(db.Model):
    __tablename__ = 'interpretes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    usado_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'usado_count': self.usado_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class NomeMusica(db.Model):
    __tablename__ = 'nomes_musicas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    usado_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'usado_count': self.usado_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ProgramacaoGerada(db.Model):
    __tablename__ = 'programacao_gerada'
    
    id = db.Column(db.Integer, primary_key=True)
    data_programacao = db.Column(db.Date, nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades_programacao.id'))
    conteudo_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    grade = db.relationship('GradeProgramacao', backref='programacoes_geradas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'data_programacao': self.data_programacao.isoformat() if self.data_programacao else None,
            'grade_id': self.grade_id,
            'grade': self.grade.to_dict() if self.grade else None,
            'conteudo_json': json.loads(self.conteudo_json) if self.conteudo_json else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }



class Locutor(db.Model):
    __tablename__ = 'locutores'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False)  # Ex: "Locutor 1", "Locutor 2"
    nome = db.Column(db.String(255), nullable=False)  # Ex: "João", "Maria"
    ativo = db.Column(db.Boolean, default=True)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'ativo': self.ativo,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Emissora(db.Model):
    __tablename__ = 'emissoras'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False)  # Ex: "Radio 1", "Radio 2"
    nome = db.Column(db.String(255), nullable=False)  # Ex: "Educadora", "Nativa"
    frequencia = db.Column(db.String(20))  # Ex: "FM 104.9", "AM 1010"
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    ativa = db.Column(db.Boolean, default=True)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'frequencia': self.frequencia,
            'cidade': self.cidade,
            'estado': self.estado,
            'ativa': self.ativa,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class LocutorEmissora(db.Model):
    __tablename__ = 'locutor_emissora'
    
    id = db.Column(db.Integer, primary_key=True)
    locutor_id = db.Column(db.Integer, db.ForeignKey('locutores.id'), nullable=False)
    emissora_id = db.Column(db.Integer, db.ForeignKey('emissoras.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    locutor = db.relationship('Locutor', backref='emissoras_associadas')
    emissora = db.relationship('Emissora', backref='locutores_associados')
    
    # Índice único para evitar duplicatas
    __table_args__ = (db.UniqueConstraint('locutor_id', 'emissora_id', name='unique_locutor_emissora'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'locutor_id': self.locutor_id,
            'locutor': self.locutor.to_dict() if self.locutor else None,
            'emissora_id': self.emissora_id,
            'emissora': self.emissora.to_dict() if self.emissora else None,
            'ativo': self.ativo,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class BancoLocucao(db.Model):
    __tablename__ = 'banco_locucoes'
    
    id = db.Column(db.Integer, primary_key=True)
    emissora_id = db.Column(db.Integer, db.ForeignKey('emissoras.id'), nullable=False)
    locutor_id = db.Column(db.Integer, db.ForeignKey('locutores.id'), nullable=False)
    interprete = db.Column(db.String(255), nullable=False)  # Nome do intérprete selecionado
    velocidade = db.Column(db.Integer, nullable=False)  # 1-5
    texto_locucao = db.Column(db.Text)  # Texto da locução (opcional)
    arquivo_audio = db.Column(db.String(500))  # Caminho do arquivo de áudio (futuro uso)
    ativa = db.Column(db.Boolean, default=True)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    emissora = db.relationship('Emissora', backref='banco_locucoes')
    locutor = db.relationship('Locutor', backref='banco_locucoes')
    
    # Validação para velocidade
    __table_args__ = (
        db.CheckConstraint('velocidade >= 1 AND velocidade <= 5', name='check_velocidade_range'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'emissora_id': self.emissora_id,
            'emissora': self.emissora.to_dict() if self.emissora else None,
            'locutor_id': self.locutor_id,
            'locutor': self.locutor.to_dict() if self.locutor else None,
            'interprete': self.interprete,
            'velocidade': self.velocidade,
            'texto_locucao': self.texto_locucao,
            'arquivo_audio': self.arquivo_audio,
            'ativa': self.ativa,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

