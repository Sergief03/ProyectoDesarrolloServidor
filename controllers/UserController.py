from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

class UserController:
    
    @staticmethod
    def login():
        if 'user_id' in session:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            usuario = User.query.filter_by(username=username).first()
            
            if usuario and check_password_hash(usuario.password, password):
                session['username'] = usuario.username
                session['user_id'] = usuario.id
                session['role'] = usuario.role 
                session['is_admin'] = usuario.is_admin
                
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error="Credenciales inválidas")
                
        return render_template('login.html')

    @staticmethod
    def register():
        if 'user_id' in session:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            if User.query.filter_by(username=username).first():
                return render_template('register.html', error="El usuario ya existe")
            
            hashed_pw = generate_password_hash(password)
            
            nuevo_usuario = User(username=username, password=hashed_pw)
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            return redirect(url_for('login'))
            
        return render_template('register.html')

    @staticmethod
    def logout():
        session.clear()
        return redirect(url_for('login'))