from flask import Blueprint, request, jsonify
from src.models.programacao import db, Categoria

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/categorias', methods=['GET'])
def get_categorias():
    """Listar todas as categorias"""
    try:
        categorias = Categoria.query.all()
        return jsonify([categoria.to_dict() for categoria in categorias]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categorias_bp.route('/categorias/<int:categoria_id>', methods=['GET'])
def get_categoria(categoria_id):
    """Obter uma categoria específica"""
    try:
        categoria = Categoria.query.get_or_404(categoria_id)
        return jsonify(categoria.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categorias_bp.route('/categorias', methods=['POST'])
def create_categoria():
    """Criar uma nova categoria"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('codigo') or not data.get('nome'):
            return jsonify({'error': 'Código e nome são obrigatórios'}), 400
        
        # Verificar se o código já existe
        if Categoria.query.filter_by(codigo=data['codigo']).first():
            return jsonify({'error': 'Código já existe'}), 400
        
        categoria = Categoria(
            codigo=data['codigo'],
            nome=data['nome'],
            descricao=data.get('descricao', '')
        )
        
        db.session.add(categoria)
        db.session.commit()
        
        return jsonify(categoria.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@categorias_bp.route('/categorias/<int:categoria_id>', methods=['PUT'])
def update_categoria(categoria_id):
    """Atualizar uma categoria"""
    try:
        categoria = Categoria.query.get_or_404(categoria_id)
        data = request.get_json()
        
        # Verificar se o novo código já existe (se foi alterado)
        if data.get('codigo') and data['codigo'] != categoria.codigo:
            if Categoria.query.filter_by(codigo=data['codigo']).first():
                return jsonify({'error': 'Código já existe'}), 400
        
        categoria.codigo = data.get('codigo', categoria.codigo)
        categoria.nome = data.get('nome', categoria.nome)
        categoria.descricao = data.get('descricao', categoria.descricao)
        
        db.session.commit()
        
        return jsonify(categoria.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@categorias_bp.route('/categorias/<int:categoria_id>', methods=['DELETE'])
def delete_categoria(categoria_id):
    """Deletar uma categoria"""
    try:
        categoria = Categoria.query.get_or_404(categoria_id)
        
        # Verificar se há músicas associadas
        if categoria.musicas:
            return jsonify({'error': 'Não é possível deletar categoria com músicas associadas'}), 400
        
        db.session.delete(categoria)
        db.session.commit()
        
        return jsonify({'message': 'Categoria deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

