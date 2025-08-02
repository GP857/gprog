from flask import Blueprint, request, jsonify
from src.models.programacao import db, Emissora

emissoras_bp = Blueprint('emissoras', __name__)

@emissoras_bp.route('/emissoras', methods=['GET'])
def get_emissoras():
    """Listar todas as emissoras"""
    try:
        ativa = request.args.get('ativa')
        cidade = request.args.get('cidade')
        estado = request.args.get('estado')
        
        query = Emissora.query
        
        if ativa is not None:
            query = query.filter_by(ativa=ativa.lower() == 'true')
        if cidade:
            query = query.filter(Emissora.cidade.ilike(f'%{cidade}%'))
        if estado:
            query = query.filter_by(estado=estado.upper())
        
        emissoras = query.order_by(Emissora.codigo).all()
        return jsonify([emissora.to_dict() for emissora in emissoras]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@emissoras_bp.route('/emissoras/<int:emissora_id>', methods=['GET'])
def get_emissora(emissora_id):
    """Obter uma emissora específica"""
    try:
        emissora = Emissora.query.get_or_404(emissora_id)
        return jsonify(emissora.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@emissoras_bp.route('/emissoras', methods=['POST'])
def create_emissora():
    """Criar uma nova emissora"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('codigo') or not data.get('nome'):
            return jsonify({'error': 'Código e nome são obrigatórios'}), 400
        
        # Verificar se o código já existe
        if Emissora.query.filter_by(codigo=data['codigo']).first():
            return jsonify({'error': 'Código já existe'}), 400
        
        emissora = Emissora(
            codigo=data['codigo'],
            nome=data['nome'],
            frequencia=data.get('frequencia', ''),
            cidade=data.get('cidade', ''),
            estado=data.get('estado', '').upper() if data.get('estado') else '',
            ativa=data.get('ativa', True),
            observacoes=data.get('observacoes', '')
        )
        
        db.session.add(emissora)
        db.session.commit()
        
        return jsonify(emissora.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@emissoras_bp.route('/emissoras/<int:emissora_id>', methods=['PUT'])
def update_emissora(emissora_id):
    """Atualizar uma emissora"""
    try:
        emissora = Emissora.query.get_or_404(emissora_id)
        data = request.get_json()
        
        # Verificar se o novo código já existe (se foi alterado)
        if data.get('codigo') and data['codigo'] != emissora.codigo:
            if Emissora.query.filter_by(codigo=data['codigo']).first():
                return jsonify({'error': 'Código já existe'}), 400
        
        emissora.codigo = data.get('codigo', emissora.codigo)
        emissora.nome = data.get('nome', emissora.nome)
        emissora.frequencia = data.get('frequencia', emissora.frequencia)
        emissora.cidade = data.get('cidade', emissora.cidade)
        emissora.estado = data.get('estado', emissora.estado).upper() if data.get('estado') else emissora.estado
        emissora.ativa = data.get('ativa', emissora.ativa)
        emissora.observacoes = data.get('observacoes', emissora.observacoes)
        
        db.session.commit()
        
        return jsonify(emissora.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@emissoras_bp.route('/emissoras/<int:emissora_id>', methods=['DELETE'])
def delete_emissora(emissora_id):
    """Deletar uma emissora"""
    try:
        emissora = Emissora.query.get_or_404(emissora_id)
        
        # Verificar se há associações com locutores
        if emissora.locutores_associados:
            return jsonify({'error': 'Não é possível deletar emissora com locutores associados'}), 400
        
        db.session.delete(emissora)
        db.session.commit()
        
        return jsonify({'message': 'Emissora deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

