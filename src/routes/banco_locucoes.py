from flask import Blueprint, request, jsonify
from src.models.programacao import db, BancoLocucao, Emissora, Locutor, LocutorEmissora, Musica
from sqlalchemy import distinct

banco_locucoes_bp = Blueprint('banco_locucoes', __name__)

@banco_locucoes_bp.route('/banco-locucoes', methods=['GET'])
def get_banco_locucoes():
    """Listar todas as locuções do banco"""
    try:
        ativa = request.args.get('ativa')
        emissora_id = request.args.get('emissora_id', type=int)
        locutor_id = request.args.get('locutor_id', type=int)
        velocidade = request.args.get('velocidade', type=int)
        interprete = request.args.get('interprete')
        
        query = BancoLocucao.query
        
        if ativa is not None:
            query = query.filter_by(ativa=ativa.lower() == 'true')
        if emissora_id:
            query = query.filter_by(emissora_id=emissora_id)
        if locutor_id:
            query = query.filter_by(locutor_id=locutor_id)
        if velocidade:
            query = query.filter_by(velocidade=velocidade)
        if interprete:
            query = query.filter(BancoLocucao.interprete.ilike(f'%{interprete}%'))
        
        locucoes = query.order_by(BancoLocucao.created_at.desc()).all()
        return jsonify([locucao.to_dict() for locucao in locucoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banco_locucoes_bp.route('/banco-locucoes/<int:locucao_id>', methods=['GET'])
def get_banco_locucao(locucao_id):
    """Obter uma locução específica"""
    try:
        locucao = BancoLocucao.query.get_or_404(locucao_id)
        return jsonify(locucao.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banco_locucoes_bp.route('/banco-locucoes', methods=['POST'])
def create_banco_locucao():
    """Criar uma nova locução"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['emissora_id', 'locutor_id', 'interprete', 'velocidade']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se a emissora existe
        emissora = Emissora.query.get(data['emissora_id'])
        if not emissora:
            return jsonify({'error': 'Emissora não encontrada'}), 404
        
        # Verificar se o locutor existe
        locutor = Locutor.query.get(data['locutor_id'])
        if not locutor:
            return jsonify({'error': 'Locutor não encontrado'}), 404
        
        # Verificar se o locutor está associado à emissora
        relacionamento = LocutorEmissora.query.filter_by(
            locutor_id=data['locutor_id'],
            emissora_id=data['emissora_id'],
            ativo=True
        ).first()
        
        if not relacionamento:
            return jsonify({'error': 'Locutor não está associado a esta emissora'}), 400
        
        # Validar velocidade
        if not (1 <= data['velocidade'] <= 5):
            return jsonify({'error': 'Velocidade deve estar entre 1 e 5'}), 400
        
        locucao = BancoLocucao(
            emissora_id=data['emissora_id'],
            locutor_id=data['locutor_id'],
            interprete=data['interprete'],
            velocidade=data['velocidade'],
            texto_locucao=data.get('texto_locucao', ''),
            arquivo_audio=data.get('arquivo_audio', ''),
            ativa=data.get('ativa', True),
            observacoes=data.get('observacoes', '')
        )
        
        db.session.add(locucao)
        db.session.commit()
        
        return jsonify(locucao.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@banco_locucoes_bp.route('/banco-locucoes/<int:locucao_id>', methods=['PUT'])
def update_banco_locucao(locucao_id):
    """Atualizar uma locução"""
    try:
        locucao = BancoLocucao.query.get_or_404(locucao_id)
        data = request.get_json()
        
        # Verificar se a emissora existe (se fornecida)
        if data.get('emissora_id'):
            emissora = Emissora.query.get(data['emissora_id'])
            if not emissora:
                return jsonify({'error': 'Emissora não encontrada'}), 404
        
        # Verificar se o locutor existe (se fornecido)
        if data.get('locutor_id'):
            locutor = Locutor.query.get(data['locutor_id'])
            if not locutor:
                return jsonify({'error': 'Locutor não encontrado'}), 404
        
        # Validar velocidade (se fornecida)
        if data.get('velocidade') and not (1 <= data['velocidade'] <= 5):
            return jsonify({'error': 'Velocidade deve estar entre 1 e 5'}), 400
        
        # Atualizar campos
        locucao.emissora_id = data.get('emissora_id', locucao.emissora_id)
        locucao.locutor_id = data.get('locutor_id', locucao.locutor_id)
        locucao.interprete = data.get('interprete', locucao.interprete)
        locucao.velocidade = data.get('velocidade', locucao.velocidade)
        locucao.texto_locucao = data.get('texto_locucao', locucao.texto_locucao)
        locucao.arquivo_audio = data.get('arquivo_audio', locucao.arquivo_audio)
        locucao.ativa = data.get('ativa', locucao.ativa)
        locucao.observacoes = data.get('observacoes', locucao.observacoes)
        
        db.session.commit()
        
        return jsonify(locucao.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@banco_locucoes_bp.route('/banco-locucoes/<int:locucao_id>', methods=['DELETE'])
def delete_banco_locucao(locucao_id):
    """Deletar uma locução"""
    try:
        locucao = BancoLocucao.query.get_or_404(locucao_id)
        
        db.session.delete(locucao)
        db.session.commit()
        
        return jsonify({'message': 'Locução deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Rotas auxiliares para facilitar a criação de locuções
@banco_locucoes_bp.route('/banco-locucoes/emissoras', methods=['GET'])
def get_emissoras_para_locucao():
    """Listar emissoras disponíveis para locução"""
    try:
        emissoras = Emissora.query.filter_by(ativa=True).order_by(Emissora.codigo).all()
        return jsonify([emissora.to_dict() for emissora in emissoras]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banco_locucoes_bp.route('/banco-locucoes/emissoras/<int:emissora_id>/locutores', methods=['GET'])
def get_locutores_da_emissora_para_locucao(emissora_id):
    """Listar locutores disponíveis de uma emissora para locução"""
    try:
        # Buscar locutores ativos associados à emissora
        relacionamentos = LocutorEmissora.query.filter_by(
            emissora_id=emissora_id,
            ativo=True
        ).all()
        
        locutores = []
        for rel in relacionamentos:
            if rel.locutor and rel.locutor.ativo:
                locutores.append(rel.locutor.to_dict())
        
        return jsonify(locutores), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banco_locucoes_bp.route('/banco-locucoes/interpretes', methods=['GET'])
def get_interpretes_para_locucao():
    """Listar intérpretes disponíveis para locução (em ordem alfabética)"""
    try:
        # Buscar todos os intérpretes únicos do banco de músicas
        interpretes_query = db.session.query(distinct(Musica.interprete1)).filter(
            Musica.interprete1.isnot(None)
        ).union(
            db.session.query(distinct(Musica.interprete2)).filter(
                Musica.interprete2.isnot(None)
            )
        ).union(
            db.session.query(distinct(Musica.interprete3)).filter(
                Musica.interprete3.isnot(None)
            )
        ).order_by(Musica.interprete1)
        
        interpretes = [row[0] for row in interpretes_query.all() if row[0]]
        interpretes.sort()  # Ordenar alfabeticamente
        
        return jsonify(interpretes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banco_locucoes_bp.route('/banco-locucoes/interpretes/search', methods=['GET'])
def search_interpretes_para_locucao():
    """Buscar intérpretes por nome para locução"""
    try:
        query = request.args.get('q', '').strip()
        if len(query) < 2:
            return jsonify([]), 200
        
        # Buscar intérpretes que contenham o termo de busca
        interpretes_query = db.session.query(distinct(Musica.interprete1)).filter(
            Musica.interprete1.ilike(f'%{query}%')
        ).union(
            db.session.query(distinct(Musica.interprete2)).filter(
                Musica.interprete2.ilike(f'%{query}%')
            )
        ).union(
            db.session.query(distinct(Musica.interprete3)).filter(
                Musica.interprete3.ilike(f'%{query}%')
            )
        )
        
        interpretes = [row[0] for row in interpretes_query.all() if row[0]]
        interpretes.sort()  # Ordenar alfabeticamente
        
        return jsonify(interpretes[:20]), 200  # Limitar a 20 resultados
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banco_locucoes_bp.route('/banco-locucoes/velocidades', methods=['GET'])
def get_velocidades_disponiveis():
    """Listar velocidades disponíveis (1-5)"""
    try:
        velocidades = [
            {'valor': 1, 'descricao': 'Muito Lenta'},
            {'valor': 2, 'descricao': 'Lenta'},
            {'valor': 3, 'descricao': 'Normal'},
            {'valor': 4, 'descricao': 'Rápida'},
            {'valor': 5, 'descricao': 'Muito Rápida'}
        ]
        return jsonify(velocidades), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

