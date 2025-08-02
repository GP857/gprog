from flask import Blueprint, request, jsonify
from src.models.programacao import db, Locutor

locutores_bp = Blueprint('locutores', __name__)

@locutores_bp.route('/locutores', methods=['GET'])
def get_locutores():
    """Listar todos os locutores"""
    try:
        ativo = request.args.get('ativo')
        query = Locutor.query
        
        if ativo is not None:
            query = query.filter_by(ativo=ativo.lower() == 'true')
        
        locutores = query.order_by(Locutor.codigo).all()
        return jsonify([locutor.to_dict() for locutor in locutores]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@locutores_bp.route('/locutores/<int:locutor_id>', methods=['GET'])
def get_locutor(locutor_id):
    """Obter um locutor específico"""
    try:
        locutor = Locutor.query.get_or_404(locutor_id)
        return jsonify(locutor.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@locutores_bp.route('/locutores', methods=['POST'])
def create_locutor():
    """Criar um novo locutor"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('codigo') or not data.get('nome'):
            return jsonify({'error': 'Código e nome são obrigatórios'}), 400
        
        # Verificar se o código já existe
        if Locutor.query.filter_by(codigo=data['codigo']).first():
            return jsonify({'error': 'Código já existe'}), 400
        
        locutor = Locutor(
            codigo=data['codigo'],
            nome=data['nome'],
            ativo=data.get('ativo', True),
            observacoes=data.get('observacoes', '')
        )
        
        db.session.add(locutor)
        db.session.commit()
        
        return jsonify(locutor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@locutores_bp.route('/locutores/<int:locutor_id>', methods=['PUT'])
def update_locutor(locutor_id):
    """Atualizar um locutor"""
    try:
        locutor = Locutor.query.get_or_404(locutor_id)
        data = request.get_json()
        
        # Verificar se o novo código já existe (se foi alterado)
        if data.get('codigo') and data['codigo'] != locutor.codigo:
            if Locutor.query.filter_by(codigo=data['codigo']).first():
                return jsonify({'error': 'Código já existe'}), 400
        
        locutor.codigo = data.get('codigo', locutor.codigo)
        locutor.nome = data.get('nome', locutor.nome)
        locutor.ativo = data.get('ativo', locutor.ativo)
        locutor.observacoes = data.get('observacoes', locutor.observacoes)
        
        db.session.commit()
        
        return jsonify(locutor.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@locutores_bp.route('/locutores/<int:locutor_id>', methods=['DELETE'])
def delete_locutor(locutor_id):
    """Deletar um locutor"""
    try:
        locutor = Locutor.query.get_or_404(locutor_id)
        
        # Verificar se há associações com emissoras
        if locutor.emissoras_associadas:
            return jsonify({'error': 'Não é possível deletar locutor com emissoras associadas'}), 400
        
        db.session.delete(locutor)
        db.session.commit()
        
        return jsonify({'message': 'Locutor deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

