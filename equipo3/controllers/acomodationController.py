from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request
from flask_login import current_user
from models import Accommodation, db


acomodation_bp = Blueprint('acomodation', __name__, template_folder='../templates')

@acomodation_bp.route('/acomodation')
def index():
    accommodations = Accommodation.query.all()
    return render_template('acomodationIndex.html', accommodations=accommodations)

@acomodation_bp.route('/acomodation/create', methods=['GET', 'POST'])
def create():
    if not current_user.is_authenticated:
        flash('Debes iniciar sesión para crear una acomodación', 'error')
        return redirect(url_for('login'))
    # Control de roles
    if current_user.role not in ['COMPANY', 'ADMIN']:
        flash('No tienes permiso para crear esta acomodación', 'error')
        return redirect(url_for('acomodation.index'))

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phoneNumber = request.form['phoneNumber']
        web = request.form['web']
        stars_quality = request.form['stars_quality']
        description = request.form['description']
        type = request.form['type']
        idCompany = current_user.id
        
        accommodation = Accommodation(
            name=name, 
            address=address, 
            phoneNumber=phoneNumber, 
            web=web, 
            stars_quality=stars_quality, 
            description=description, 
            type=type, 
            idCompany=idCompany
        )
        db.session.add(accommodation)
        db.session.commit()
        return redirect(url_for('acomodation.index'))
    
    return render_template('acomodationCreate.html')

# show
@acomodation_bp.route('/acomodation/show/<int:id>', methods=['GET'])
def show(id):

    accommodation = Accommodation.query.get_or_404(id)
    return render_template('acomodationShow.html', accommodation=accommodation)

# delete
@acomodation_bp.route('/acomodation/delete/<int:id>', methods=['POST'])
def delete(id):
    accommodation = Accommodation.query.get_or_404(id)
    # Control de roles
    if current_user.role not in ['COMPANY', 'ADMIN']:
        flash('No tienes permiso para eliminar esta acomodación', 'error')
        return redirect(url_for('acomodation.index'))
    if current_user.id != accommodation.idCompany:
        flash('No tienes permiso para eliminar esta acomodación', 'error')
        return redirect(url_for('acomodation.index'))
        
    db.session.delete(accommodation)
    db.session.commit()
    return redirect(url_for('acomodation.index'))

# Edit
@acomodation_bp.route('/acomodation/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    accommodation = Accommodation.query.get_or_404(id)
    if not current_user.is_authenticated:
        flash('Debes iniciar sesión para crear una acomodación', 'error')
        return redirect(url_for('login'))
    if current_user.id != accommodation.idCompany:
        flash('No tienes permiso para editar esta acomodación', 'error')
        return redirect(url_for('acomodation.index'))
    
    if request.method == 'POST':
        accommodation.name = request.form['name']
        accommodation.address = request.form['address']
        accommodation.phoneNumber = request.form['phoneNumber']
        accommodation.web = request.form['web']
        accommodation.stars_quality = request.form['stars_quality']
        accommodation.description = request.form['description']
        accommodation.type = request.form['type']
        # No actualizar id_company, o mantener el actual
        db.session.commit()
        return redirect(url_for('acomodation.index'))
    
    return render_template('acomodationEdit.html', accommodation=accommodation)
