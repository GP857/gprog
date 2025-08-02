from flask import Blueprint, request, jsonify
from src.models.programacao import db, Estilo

estilos_bp = Blueprint('estilos', __name__)

@estilos_bp.route('/estilos', methods=['GET'])
def get_estilos():
    """Listar todos os estilos"""
    try:
        estilos = Estilo.query.order_by(Estilo.nome).all()
        return jsonify([estilo.to_dict() for estilo in estilos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@estilos_bp.route('/estilos/<int:estilo_id>', methods=['GET'])
def get_estilo(estilo_id):
    """Obter um estilo específico"""
    try:
        estilo = Estilo.query.get_or_404(estilo_id)
        return jsonify(estilo.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@estilos_bp.route('/estilos', methods=['POST'])
def create_estilo():
    """Criar um novo estilo"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('nome'):
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        # Verificar se o nome já existe
        if Estilo.query.filter_by(nome=data['nome']).first():
            return jsonify({'error': 'Estilo já existe'}), 400
        
        estilo = Estilo(nome=data['nome'])
        
        db.session.add(estilo)
        db.session.commit()
        
        return jsonify(estilo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@estilos_bp.route('/estilos/<int:estilo_id>', methods=['PUT'])
def update_estilo(estilo_id):
    """Atualizar um estilo"""
    try:
        estilo = Estilo.query.get_or_404(estilo_id)
        data = request.get_json()
        
        # Verificar se o novo nome já existe (se foi alterado)
        if data.get('nome') and data['nome'] != estilo.nome:
            if Estilo.query.filter_by(nome=data['nome']).first():
                return jsonify({'error': 'Estilo já existe'}), 400
        
        estilo.nome = data.get('nome', estilo.nome)
        
        db.session.commit()
        
        return jsonify(estilo.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@estilos_bp.route('/estilos/<int:estilo_id>', methods=['DELETE'])
def delete_estilo(estilo_id):
    """Deletar um estilo"""
    try:
        estilo = Estilo.query.get_or_404(estilo_id)
        
        # Verificar se há músicas associadas
        if estilo.musicas:
            return jsonify({'error': 'Não é possível deletar estilo com músicas associadas'}), 400
        
        db.session.delete(estilo)
        db.session.commit()
        
        return jsonify({'message': 'Estilo deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

