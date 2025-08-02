from flask import Blueprint, request, jsonify
from src.models.programacao import db, LocutorEmissora, Locutor, Emissora
from datetime import datetime

locutor_emissora_bp = Blueprint('locutor_emissora', __name__)

@locutor_emissora_bp.route('/locutor-emissora', methods=['GET'])
def get_relacionamentos():
    """Listar todos os relacionamentos locutor-emissora"""
    try:
        ativo = request.args.get('ativo')
        locutor_id = request.args.get('locutor_id', type=int)
        emissora_id = request.args.get('emissora_id', type=int)
        
        query = LocutorEmissora.query
        
        if ativo is not None:
            query = query.filter_by(ativo=ativo.lower() == 'true')
        if locutor_id:
            query = query.filter_by(locutor_id=locutor_id)
        if emissora_id:
            query = query.filter_by(emissora_id=emissora_id)
        
        relacionamentos = query.all()
        return jsonify([rel.to_dict() for rel in relacionamentos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@locutor_emissora_bp.route('/locutor-emissora/<int:relacionamento_id>', methods=['GET'])
def get_relacionamento(relacionamento_id):
    """Obter um relacionamento específico"""
    try:
        relacionamento = LocutorEmissora.query.get_or_404(relacionamento_id)
        return jsonify(relacionamento.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@locutor_emissora_bp.route('/locutor-emissora', methods=['POST'])
def create_relacionamento():
    """Criar um novo relacionamento locutor-emissora"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('locutor_id') or not data.get('emissora_id'):
            return jsonify({'error': 'Locutor e emissora são obrigatórios'}), 400
        
        # Verificar se o locutor existe
        locutor = Locutor.query.get(data['locutor_id'])
        if not locutor:
            return jsonify({'error': 'Locutor não encontrado'}), 404
        
        # Verificar se a emissora existe
        emissora = Emissora.query.get(data['emissora_id'])
        if not emissora:
            return jsonify({'error': 'Emissora não encontrada'}), 404
        
        # Verificar se o relacionamento já existe
        relacionamento_existente = LocutorEmissora.query.filter_by(
            locutor_id=data['locutor_id'],
            emissora_id=data['emissora_id']
        ).first()
        
        if relacionamento_existente:
            return jsonify({'error': 'Relacionamento já existe'}), 400
        
        relacionamento = LocutorEmissora(
            locutor_id=data['locutor_id'],
            emissora_id=data['emissora_id'],
            ativo=data.get('ativo', True),
            observacoes=data.get('observacoes', '')
        )
        
        # Processar datas se fornecidas
        if data.get('data_inicio'):
            try:
                relacionamento.data_inicio = datetime.strptime(
                    data['data_inicio'], '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({'error': 'Formato de data de início inválido (use YYYY-MM-DD)'}), 400
        
        if data.get('data_fim'):
            try:
                relacionamento.data_fim = datetime.strptime(
                    data['data_fim'], '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({'error': 'Formato de data de fim inválido (use YYYY-MM-DD)'}), 400
        
        db.session.add(relacionamento)
        db.session.commit()
        
        return jsonify(relacionamento.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@locutor_emissora_bp.route('/locutor-emissora/<int:relacionamento_id>', methods=['PUT'])
def update_relacionamento(relacionamento_id):
    """Atualizar um relacionamento"""
    try:
        relacionamento = LocutorEmissora.query.get_or_404(relacionamento_id)
        data = request.get_json()
        
        relacionamento.ativo = data.get('ativo', relacionamento.ativo)
        relacionamento.observacoes = data.get('observacoes', relacionamento.observacoes)
        
        # Atualizar datas se fornecidas
        if data.get('data_inicio'):
            try:
                relacionamento.data_inicio = datetime.strptime(
                    data['data_inicio'], '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({'error': 'Formato de data de início inválido (use YYYY-MM-DD)'}), 400
        
        if data.get('data_fim'):
            try:
                relacionamento.data_fim = datetime.strptime(
                    data['data_fim'], '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({'error': 'Formato de data de fim inválido (use YYYY-MM-DD)'}), 400
        
        db.session.commit()
        
        return jsonify(relacionamento.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@locutor_emissora_bp.route('/locutor-emissora/<int:relacionamento_id>', methods=['DELETE'])
def delete_relacionamento(relacionamento_id):
    """Deletar um relacionamento"""
    try:
        relacionamento = LocutorEmissora.query.get_or_404(relacionamento_id)
        
        db.session.delete(relacionamento)
        db.session.commit()
        
        return jsonify({'message': 'Relacionamento deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Rotas auxiliares para facilitar consultas
@locutor_emissora_bp.route('/locutores/<int:locutor_id>/emissoras', methods=['GET'])
def get_emissoras_do_locutor(locutor_id):
    """Listar emissoras associadas a um locutor"""
    try:
        locutor = Locutor.query.get_or_404(locutor_id)
        relacionamentos = LocutorEmissora.query.filter_by(locutor_id=locutor_id).all()
        
        return jsonify({
            'locutor': locutor.to_dict(),
            'emissoras': [rel.emissora.to_dict() for rel in relacionamentos if rel.emissora]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@locutor_emissora_bp.route('/emissoras/<int:emissora_id>/locutores', methods=['GET'])
def get_locutores_da_emissora(emissora_id):
    """Listar locutores associados a uma emissora"""
    try:
        emissora = Emissora.query.get_or_404(emissora_id)
        relacionamentos = LocutorEmissora.query.filter_by(emissora_id=emissora_id).all()
        
        return jsonify({
            'emissora': emissora.to_dict(),
            'locutores': [rel.locutor.to_dict() for rel in relacionamentos if rel.locutor]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

