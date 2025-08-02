from flask import Blueprint, request, jsonify
from src.models.programacao import db, Musica, Categoria, Estilo, Interprete, NomeMusica, ComplementoMusica
from datetime import datetime

musicas_bp = Blueprint('musicas', __name__)

@musicas_bp.route('/musicas', methods=['GET'])
def get_musicas():
    """Listar todas as músicas"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Filtros opcionais
        categoria_id = request.args.get('categoria_id', type=int)
        estilo_id = request.args.get('estilo_id', type=int)
        velocidade = request.args.get('velocidade', type=int)
        ano = request.args.get('ano', type=int)
        
        query = Musica.query
        
        if categoria_id:
            query = query.filter_by(categoria_id=categoria_id)
        if estilo_id:
            query = query.filter_by(estilo_id=estilo_id)
        if velocidade:
            query = query.filter_by(velocidade=velocidade)
        if ano:
            query = query.filter_by(ano_lancamento=ano)
        
        musicas = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'musicas': [musica.to_dict() for musica in musicas.items],
            'total': musicas.total,
            'pages': musicas.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@musicas_bp.route('/musicas/<int:musica_id>', methods=['GET'])
def get_musica(musica_id):
    """Obter uma música específica"""
    try:
        musica = Musica.query.get_or_404(musica_id)
        return jsonify(musica.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@musicas_bp.route('/musicas', methods=['POST'])
def create_musica():
    """Criar uma nova música"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['interprete1', 'nome_musica', 'ano_lancamento', 'categoria_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se a categoria existe
        categoria = Categoria.query.get(data['categoria_id'])
        if not categoria:
            return jsonify({'error': 'Categoria não encontrada'}), 404
        
        # Verificar se o estilo existe (se fornecido)
        if data.get('estilo_id'):
            estilo = Estilo.query.get(data['estilo_id'])
            if not estilo:
                return jsonify({'error': 'Estilo não encontrado'}), 404
        
        musica = Musica(
            interprete1=data['interprete1'],
            interprete2=data.get('interprete2'),
            interprete3=data.get('interprete3'),
            nome_musica=data['nome_musica'],
            tipo=data.get('tipo'),
            categoria_id=data['categoria_id'],
            velocidade=data.get('velocidade'),
            estilo_id=data.get('estilo_id'),
            ano_lancamento=data['ano_lancamento'],
            complemento=data.get('complemento')
        )
        
        # Processar datas de aniversário se fornecidas
        if data.get('data_aniversario_interprete1'):
            try:
                musica.data_aniversario_interprete1 = datetime.strptime(
                    data['data_aniversario_interprete1'], '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido para intérprete 1 (use YYYY-MM-DD)'}), 400
        
        if data.get('data_aniversario_interprete2'):
            try:
                musica.data_aniversario_interprete2 = datetime.strptime(
                    data['data_aniversario_interprete2'], '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido para intérprete 2 (use YYYY-MM-DD)'}), 400
        
        if data.get('data_aniversario_interprete3'):
            try:
                musica.data_aniversario_interprete3 = datetime.strptime(
                    data['data_aniversario_interprete3'], '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido para intérprete 3 (use YYYY-MM-DD)'}), 400
        
        db.session.add(musica)
        
        # Memorizar intérpretes para autocompletar
        _memorizar_interprete(data['interprete1'])
        if data.get('interprete2'):
            _memorizar_interprete(data['interprete2'])
        if data.get('interprete3'):
            _memorizar_interprete(data['interprete3'])
        
        # Memorizar nome da música
        _memorizar_nome_musica(data['nome_musica'])
        
        # Memorizar complemento
        if data.get('complemento'):
            _memorizar_complemento(data['complemento'])
        
        db.session.commit()
        
        return jsonify(musica.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@musicas_bp.route('/musicas/<int:musica_id>', methods=['PUT'])
def update_musica(musica_id):
    """Atualizar uma música"""
    try:
        musica = Musica.query.get_or_404(musica_id)
        data = request.get_json()
        
        # Verificar se a categoria existe (se fornecida)
        if data.get('categoria_id'):
            categoria = Categoria.query.get(data['categoria_id'])
            if not categoria:
                return jsonify({'error': 'Categoria não encontrada'}), 404
        
        # Verificar se o estilo existe (se fornecido)
        if data.get('estilo_id'):
            estilo = Estilo.query.get(data['estilo_id'])
            if not estilo:
                return jsonify({'error': 'Estilo não encontrado'}), 404
        
        # Atualizar campos
        musica.interprete1 = data.get('interprete1', musica.interprete1)
        musica.interprete2 = data.get('interprete2', musica.interprete2)
        musica.interprete3 = data.get('interprete3', musica.interprete3)
        musica.nome_musica = data.get('nome_musica', musica.nome_musica)
        musica.tipo = data.get('tipo', musica.tipo)
        musica.categoria_id = data.get('categoria_id', musica.categoria_id)
        musica.velocidade = data.get('velocidade', musica.velocidade)
        musica.estilo_id = data.get('estilo_id', musica.estilo_id)
        musica.ano_lancamento = data.get('ano_lancamento', musica.ano_lancamento)
        musica.complemento = data.get('complemento', musica.complemento)
        
        # Atualizar datas de aniversário se fornecidas
        if data.get('data_aniversario_interprete1'):
            try:
                musica.data_aniversario_interprete1 = datetime.strptime(
                    data['data_aniversario_interprete1'], '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido para intérprete 1 (use YYYY-MM-DD)'}), 400
        
        if data.get('data_aniversario_interprete2'):
            try:
                musica.data_aniversario_interprete2 = datetime.strptime(
                    data['data_aniversario_interprete2'], '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido para intérprete 2 (use YYYY-MM-DD)'}), 400
        
        if data.get('data_aniversario_interprete3'):
            try:
                musica.data_aniversario_interprete3 = datetime.strptime(
                    data['data_aniversario_interprete3'], '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido para intérprete 3 (use YYYY-MM-DD)'}), 400
        
        db.session.commit()
        
        return jsonify(musica.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@musicas_bp.route('/musicas/<int:musica_id>', methods=['DELETE'])
def delete_musica(musica_id):
    """Deletar uma música"""
    try:
        musica = Musica.query.get_or_404(musica_id)
        
        db.session.delete(musica)
        db.session.commit()
        
        return jsonify({'message': 'Música deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Rotas para autocompletar
@musicas_bp.route('/musicas/autocomplete/interpretes', methods=['GET'])
def autocomplete_interpretes():
    """Buscar intérpretes para autocompletar"""
    try:
        query = request.args.get('q', '').strip()
        if len(query) < 2:
            return jsonify([]), 200
        
        interpretes = Interprete.query.filter(
            Interprete.nome.ilike(f'%{query}%')
        ).order_by(Interprete.usado_count.desc()).limit(10).all()
        
        return jsonify([interprete.to_dict() for interprete in interpretes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@musicas_bp.route('/musicas/autocomplete/nomes', methods=['GET'])
def autocomplete_nomes():
    """Buscar nomes de músicas para autocompletar"""
    try:
        query = request.args.get('q', '').strip()
        if len(query) < 2:
            return jsonify([]), 200
        
        nomes = NomeMusica.query.filter(
            NomeMusica.nome.ilike(f'%{query}%')
        ).order_by(NomeMusica.usado_count.desc()).limit(10).all()
        
        return jsonify([nome.to_dict() for nome in nomes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@musicas_bp.route('/musicas/autocomplete/complementos', methods=['GET'])
def autocomplete_complementos():
    """Buscar complementos para autocompletar"""
    try:
        query = request.args.get('q', '').strip()
        if len(query) < 2:
            return jsonify([]), 200
        
        complementos = ComplementoMusica.query.filter(
            ComplementoMusica.complemento.ilike(f'%{query}%')
        ).order_by(ComplementoMusica.usado_count.desc()).limit(10).all()
        
        return jsonify([complemento.to_dict() for complemento in complementos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Funções auxiliares
def _memorizar_interprete(nome):
    """Memorizar intérprete para autocompletar futuras digitações"""
    interprete = Interprete.query.filter_by(nome=nome).first()
    if interprete:
        interprete.usado_count += 1
    else:
        interprete = Interprete(nome=nome)
        db.session.add(interprete)

def _memorizar_nome_musica(nome):
    """Memorizar nome da música para autocompletar futuras digitações"""
    nome_musica = NomeMusica.query.filter_by(nome=nome).first()
    if nome_musica:
        nome_musica.usado_count += 1
    else:
        nome_musica = NomeMusica(nome=nome)
        db.session.add(nome_musica)

def _memorizar_complemento(complemento):
    """Memorizar complemento para autocompletar futuras digitações"""
    comp = ComplementoMusica.query.filter_by(complemento=complemento).first()
    if comp:
        comp.usado_count += 1
    else:
        comp = ComplementoMusica(complemento=complemento)
        db.session.add(comp)

