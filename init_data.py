#!/usr/bin/env python3
"""
Script para inicializar o banco de dados com dados de exemplo
Sistema de Programação Musical
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.models.programacao import *
from src.main import app

def init_database():
    """Inicializar banco de dados com dados de exemplo"""
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar se já existem dados
        if Estilo.query.first():
            print("Banco de dados já inicializado.")
            return
        
        print("Inicializando banco de dados...")
        
        # Inserir estilos
        estilos = [
            'Pop', 'Rock', 'MPB', 'Sertanejo', 'Funk', 'Eletrônica',
            'Jazz', 'Blues', 'Reggae', 'Hip Hop', 'R&B', 'Country',
            'Folk', 'Classical', 'Gospel', 'Forró', 'Axé', 'Pagode',
            'Samba', 'Bossa Nova'
        ]
        
        for estilo_nome in estilos:
            estilo = Estilo(nome=estilo_nome)
            db.session.add(estilo)
        
        # Inserir categorias de exemplo
        categorias = [
            {'codigo': '01', 'nome': 'Internacional Lenta FB', 'descricao': 'Músicas internacionais lentas para Facebook'},
            {'codigo': '02', 'nome': 'Nacional Pop', 'descricao': 'Músicas nacionais pop'},
            {'codigo': '03', 'nome': 'Rock Clássico', 'descricao': 'Rock clássico nacional e internacional'},
            {'codigo': '04', 'nome': 'MPB Contemporânea', 'descricao': 'MPB contemporânea'},
            {'codigo': '05', 'nome': 'Sertanejo Atual', 'descricao': 'Sertanejo atual e universitário'}
        ]
        
        for cat_data in categorias:
            categoria = Categoria(
                codigo=cat_data['codigo'],
                nome=cat_data['nome'],
                descricao=cat_data['descricao']
            )
            db.session.add(categoria)
        
        # Inserir locutores de exemplo
        locutores = [
            {'codigo': 'Locutor 1', 'nome': 'João'},
            {'codigo': 'Locutor 2', 'nome': 'Maria'},
            {'codigo': 'Locutor 3', 'nome': 'Zé'},
            {'codigo': 'Locutor 4', 'nome': 'Ana'},
            {'codigo': 'Locutor 5', 'nome': 'Carlos'}
        ]
        
        for loc_data in locutores:
            locutor = Locutor(
                codigo=loc_data['codigo'],
                nome=loc_data['nome']
            )
            db.session.add(locutor)
        
        # Inserir emissoras de exemplo
        emissoras = [
            {'codigo': 'Radio 1', 'nome': 'Educadora', 'frequencia': 'FM 104.9'},
            {'codigo': 'Radio 2', 'nome': 'Nativa', 'frequencia': 'FM 95.3'},
            {'codigo': 'Radio 3', 'nome': 'Band', 'frequencia': 'FM 96.1'},
            {'codigo': 'Radio 4', 'nome': 'Jovem Pan', 'frequencia': 'FM 100.9'},
            {'codigo': 'Radio 5', 'nome': 'Mix', 'frequencia': 'FM 106.3'}
        ]
        
        for em_data in emissoras:
            emissora = Emissora(
                codigo=em_data['codigo'],
                nome=em_data['nome'],
                frequencia=em_data['frequencia']
            )
            db.session.add(emissora)
        
        # Commit das inserções
        db.session.commit()
        
        print("Banco de dados inicializado com sucesso!")
        print(f"- {len(estilos)} estilos inseridos")
        print(f"- {len(categorias)} categorias inseridas")
        print(f"- {len(locutores)} locutores inseridos")
        print(f"- {len(emissoras)} emissoras inseridas")

if __name__ == '__main__':
    init_database()

