# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 12:24:37 2025

@author: USER
"""

# auth_database.py - Sistema de autenticación mejorado
import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import os

class DatabaseAuthManager:
    def __init__(self):
        self.db_path = "users.db"
        self.init_database()
    
    def init_database(self):
        """Inicializar la base de datos de usuarios"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                analyses_count INTEGER DEFAULT 0,
                last_login TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Encriptar contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, email):
        """Registrar nuevo usuario"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                conn.close()
                return False, "Usuario ya existe"
            
            # Crear nuevo usuario
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, created_at, analyses_count)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, self.hash_password(password), datetime.now().isoformat(), 0))
            
            conn.commit()
            conn.close()
            return True, "Usuario registrado exitosamente"
            
        except Exception as e:
            return False, f"Error al registrar usuario: {str(e)}"
    
    def authenticate(self, username, password):
        """Autenticar usuario"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT password_hash FROM users WHERE username = ?
            ''', (username,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0] == self.hash_password(password):
                self.update_last_login(username)
                return True
            return False
            
        except Exception as e:
            st.error(f"Error en autenticación: {str(e)}")
            return False
    
    def update_last_login(self, username):
        """Actualizar último login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users SET last_login = ? WHERE username = ?
            ''', (datetime.now().isoformat(), username))
            
            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"Error actualizando login: {str(e)}")
    
    def get_user_info(self, username):
        """Obtener información del usuario"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT username, email, created_at, analyses_count, last_login
                FROM users WHERE username = ?
            ''', (username,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'username': result[0],
                    'email': result[1],
                    'created_at': result[2],
                    'analyses_count': result[3],
                    'last_login': result[4]
                }
            return {}
            
        except Exception as e:
            st.error(f"Error obteniendo info de usuario: {str(e)}")
            return {}
    
    def increment_analysis_count(self, username):
        """Incrementar contador de análisis"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users SET analyses_count = analyses_count + 1 
                WHERE username = ?
            ''', (username,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"Error incrementando contador: {str(e)}")
    
    def get_all_users(self):
        """Obtener todos los usuarios (para admin)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT username, email, created_at, analyses_count, last_login
                FROM users ORDER BY created_at DESC
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            users = []
            for result in results:
                users.append({
                    'username': result[0],
                    'email': result[1],
                    'created_at': result[2],
                    'analyses_count': result[3],
                    'last_login': result[4]
                })
            
            return users
            
        except Exception as e:
            st.error(f"Error obteniendo usuarios: {str(e)}")
            return []

# Función para migrar usuarios existentes de YAML a SQLite
def migrate_yaml_to_sqlite():
    """Migrar usuarios de users.yaml a base de datos SQLite"""
    import yaml
    
    yaml_file = "users.yaml"
    if os.path.exists(yaml_file):
        try:
            with open(yaml_file, 'r') as f:
                yaml_users = yaml.safe_load(f) or {}
            
            db_auth = DatabaseAuthManager()
            
            for username, user_data in yaml_users.items():
                # No podemos migrar la contraseña hasheada directamente
                # Los usuarios tendrán que registrarse de nuevo
                st.info(f"Usuario {username} necesita registrarse nuevamente por migración de seguridad")
            
            # Opcional: Renombrar archivo YAML para backup
            os.rename(yaml_file, f"{yaml_file}.backup")
            
        except Exception as e:
            st.error(f"Error en migración: {str(e)}")

# Función para usar en el archivo principal
def get_auth_manager():
    """Obtener instancia del gestor de autenticación"""
    return DatabaseAuthManager()