# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 12:24:37 2025

@author: Ai-mindnovation
"""

# auth_database.py - Versión SQLite para persistencia mejorada
import sqlite3
import hashlib
import streamlit as st
from datetime import datetime
import os

class AuthManager:
    def __init__(self):
        # Usar directorio temporal que persiste más tiempo en Streamlit Cloud
        self.db_path = "/tmp/ai_mindnovation_users.db"
        self._init_database()
    
    def _init_database(self):
        """Inicializar la base de datos SQLite y crear tabla de usuarios"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Crear tabla de usuarios si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                email TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT 0,
                created_at TEXT NOT NULL,
                last_login TEXT,
                analyses_count INTEGER DEFAULT 0
            )
        ''')
        
        # Crear usuario administrador por defecto si no existe
        cursor.execute("SELECT username FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            admin_hash = self._hash_password("admin123")
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, is_admin, created_at, analyses_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ("admin", admin_hash, "admin@ai-mindnovation.com", True, datetime.now().isoformat(), 0))
            
            # Agregar usuario de demostración
            demo_hash = self._hash_password("demo123")
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, is_admin, created_at, analyses_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ("demo", demo_hash, "demo@ai-mindnovation.com", False, datetime.now().isoformat(), 0))
        
        conn.commit()
        conn.close()
    
    def _hash_password(self, password):
        """Hashear contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        """Autenticar usuario con username y password"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            
            if result:
                stored_hash = result[0]
                password_hash = self._hash_password(password)
                
                if stored_hash == password_hash:
                    # Actualizar último login
                    cursor.execute(
                        "UPDATE users SET last_login = ? WHERE username = ?",
                        (datetime.now().isoformat(), username)
                    )
                    conn.commit()
                    conn.close()
                    return True
            
            conn.close()
            return False
            
        except Exception as e:
            print(f"Error en autenticación: {e}")
            return False
    
    def register_user(self, username, password, email):
        """Registrar nuevo usuario"""
        try:
            # Validaciones
            if len(password) < 6:
                return False, "La contraseña debe tener al menos 6 caracteres"
            
            if not email or "@" not in email:
                return False, "Email inválido"
            
            if not username or len(username) < 3:
                return False, "El nombre de usuario debe tener al menos 3 caracteres"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT username FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                conn.close()
                return False, "El usuario o email ya existe"
            
            # Crear nuevo usuario
            password_hash = self._hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, created_at, analyses_count)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password_hash, email, datetime.now().isoformat(), 0))
            
            conn.commit()
            conn.close()
            return True, "Usuario registrado exitosamente"
            
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False, f"Error al registrar usuario: {str(e)}"
    
    def get_user_info(self, username):
        """Obtener información del usuario"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT email, is_admin, created_at, last_login, analyses_count 
                FROM users WHERE username = ?
            ''', (username,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    "email": result[0],
                    "is_admin": bool(result[1]),
                    "created_at": result[2],
                    "last_login": result[3],
                    "analyses_count": result[4]
                }
            return {}
            
        except Exception as e:
            print(f"Error al obtener info del usuario: {e}")
            return {}
    
    def increment_analysis_count(self, username):
        """Incrementar contador de análisis del usuario"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE users SET analyses_count = analyses_count + 1 WHERE username = ?",
                (username,)
            )
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error al incrementar contador: {e}")
    
    def get_all_users(self):
        """Obtener todos los usuarios (para panel administrativo)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT username, email, is_admin, created_at, last_login, analyses_count 
                FROM users ORDER BY created_at DESC
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            users = []
            for row in results:
                users.append({
                    "username": row[0],
                    "email": row[1],
                    "is_admin": bool(row[2]),
                    "created_at": row[3],
                    "last_login": row[4],
                    "analyses_count": row[5]
                })
            
            return users
            
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
    
    def delete_user(self, username):
        """Eliminar usuario (para panel administrativo)"""
        try:
            if username == "admin":
                return False, "No se puede eliminar el usuario administrador"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                return True, "Usuario eliminado exitosamente"
            else:
                conn.close()
                return False, "Usuario no encontrado"
                
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False, f"Error al eliminar usuario: {str(e)}"
    
    def update_user_admin_status(self, username, is_admin):
        """Cambiar estado de administrador de un usuario"""
        try:
            if username == "admin":
                return False, "No se puede cambiar el estado del usuario administrador principal"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE users SET is_admin = ? WHERE username = ?",
                (is_admin, username)
            )
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                return True, f"Usuario {'promovido a' if is_admin else 'removido de'} administrador"
            else:
                conn.close()
                return False, "Usuario no encontrado"
                
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False, f"Error al actualizar usuario: {str(e)}"
    
    def get_stats(self):
        """Obtener estadísticas generales (para panel administrativo)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total de usuarios
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            
            # Total de análisis realizados
            cursor.execute("SELECT SUM(analyses_count) FROM users")
            total_analyses = cursor.fetchone()[0] or 0
            
            # Usuarios activos (que han hecho login)
            cursor.execute("SELECT COUNT(*) FROM users WHERE last_login IS NOT NULL")
            active_users = cursor.fetchone()[0]
            
            # Usuario más activo
            cursor.execute('''
                SELECT username, analyses_count FROM users 
                WHERE analyses_count > 0 
                ORDER BY analyses_count DESC LIMIT 1
            ''')
            top_user = cursor.fetchone()
            
            conn.close()
            
            return {
                "total_users": total_users,
                "total_analyses": total_analyses,
                "active_users": active_users,
                "top_user": top_user[0] if top_user else "N/A",
                "top_user_analyses": top_user[1] if top_user else 0
            }
            
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                "total_users": 0,
                "total_analyses": 0,
                "active_users": 0,
                "top_user": "N/A",
                "top_user_analyses": 0
            }

# Función para obtener instancia del AuthManager
def get_auth_manager():
    """Obtener instancia singleton del AuthManager"""
    if 'auth_manager' not in st.session_state:
        st.session_state.auth_manager = AuthManager()
    return st.session_state.auth_manager