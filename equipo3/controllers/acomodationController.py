from flask import Blueprint, render_template, flash, redirect, url_for, request, session, current_app
from werkzeug.utils import secure_filename
from models import Accommodation, db
from equipo3.models.AccommodationBookingLine import AccommodationBookingLine
from equipo3.models.Room import Room
from equipo3.models.Review import Review
from datetime import datetime
import os
import uuid

acomodation_bp = Blueprint('aco', __name__, template_folder='../templates')

# Allowed extensions for images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    """Guarda un archivo subido y retorna la ruta relativa"""
    if file and file.filename and allowed_file(file.filename):
        # Generar nombre único para evitar conflictos
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # Obtener la ruta de upload desde la configuración
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'equipo3/static/uploads')
        
        # Asegurar que el directorio existe
        os.makedirs(upload_folder, exist_ok=True)
        
        # Guardar el archivo
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # Retornar la ruta relativa para guardar en la BD
        return f"uploads/{unique_filename}"
    return None

# =========================
# ADMIN DASHBOARD
# =========================
# Solo puede verlo el admin
@acomodation_bp.route('/admin/dashboard')
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "admin": # changed to admin lowercase
        flash('Permission denied')
        return redirect(url_for('aco.home'))
        
    from models.User import User
    from equipo3.models.AccommodationBookingLine import AccommodationBookingLine
    
    users = User.query.all()
    accommodations = Accommodation.query.all()
    bookings = AccommodationBookingLine.query.order_by(AccommodationBookingLine.bookingDate.desc()).limit(20).all()
    
    return render_template('admin_dashboard.html', 
                           users_count=len(users),
                           accommodations_count=len(accommodations),
                           bookings_count=len(bookings), # Total logic might vary but sending list length for simple summary or separate query for count
                           accommodations=accommodations,
                           bookings=bookings)

# =========================
# MANAGE HOTELS (Company)
# =========================
# Solo puede verlo la company
@acomodation_bp.route('/manage_hotels')
def manage_hotels():
    if "user_id" not in session or session.get("role") != "company":
         flash('Access denied.')
         return redirect(url_for('login'))
         
    accommodations = Accommodation.query.filter_by(idCompany=session["user_id"]).all()
    return render_template('manage_hotels.html', accommodations=accommodations)


# =========================
# HOME (Landing Page)
# =========================
@acomodation_bp.route('/')
def home():
    accommodations = Accommodation.query.limit(9).all()
    return render_template('index.html', accommodations=accommodations, checkin='', checkout='')

# =========================
# SEARCH
# =========================
@acomodation_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('location', '')
    checkin = request.args.get('checkin', '')
    checkout = request.args.get('checkout', '')

    # Base query: filter by location
    if query:
        base_query = Accommodation.query.filter(
            (Accommodation.name.ilike(f'%{query}%')) |
            (Accommodation.address.ilike(f'%{query}%'))
        )
    else:
        base_query = Accommodation.query

    results = base_query.all()

    # If dates are provided, filter to only accommodations that have at least one available room
    if checkin and checkout:
        try:
            checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
            checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()

            if checkin_date < checkout_date:
                filtered = []
                for acc in results:
                    # Get IDs of rooms that overlap with the requested dates
                    booked_room_ids = db.session.query(AccommodationBookingLine.idRoom).filter(
                        AccommodationBookingLine.idAccommodation == acc.id,
                        AccommodationBookingLine.idRoom.isnot(None),
                        AccommodationBookingLine.startDate < checkout_date,
                        AccommodationBookingLine.endDate > checkin_date,
                        AccommodationBookingLine.status != 'cancelled'
                    ).distinct().all()
                    booked_ids = {r[0] for r in booked_room_ids}

                    # Check if at least one room is available
                    available = [room for room in acc.rooms if room.id not in booked_ids]
                    if available or not acc.rooms:  # show accommodations with no rooms too
                        filtered.append(acc)
                results = filtered
        except (ValueError, TypeError):
            pass  # Invalid dates — ignore date filtering

    return render_template('index.html', accommodations=results, checkin=checkin, checkout=checkout)


# =========================
# CREATE
# =========================
# Solo puede crearlo la company
@acomodation_bp.route('/acomodation/create', methods=['GET', 'POST'])
def create():

    if "user_id" not in session:
        flash('Debes iniciar sesión')
        return redirect(url_for('login'))

    if session.get("role") not in ["company", "admin"]:
        flash('No tienes permisos')
        return redirect(url_for('aco.home'))

    if request.method == 'POST':
        # Manejar subida de imagen
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                image_url = save_uploaded_file(file)
        
        accommodation = Accommodation(
            name=request.form['name'],
            address=request.form['address'],
            phoneNumber=request.form['phoneNumber'],
            web=request.form['web'],
            stars_quality=request.form['stars_quality'],
            description=request.form['description'],
            type=request.form['type'],
            idCompany=session["user_id"],
            image_url=image_url
        )

        db.session.add(accommodation)
        db.session.commit()
        flash('Property created successfully!', 'success')
        return redirect(url_for('aco.home'))
    
    return render_template('acomodationCreate.html')


# =========================
# SHOW
# =========================
@acomodation_bp.route('/acomodation/show/<int:id>', methods=['GET'])
def show(id):
    accommodation = Accommodation.query.get_or_404(id)
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')

    # Compute which rooms are unavailable for the selected dates
    unavailable_room_ids = set()
    if checkin and checkout:
        try:
            checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
            checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()

            if checkin_date < checkout_date:
                booked = db.session.query(AccommodationBookingLine.idRoom).filter(
                    AccommodationBookingLine.idAccommodation == id,
                    AccommodationBookingLine.idRoom.isnot(None),
                    AccommodationBookingLine.startDate < checkout_date,
                    AccommodationBookingLine.endDate > checkin_date,
                    AccommodationBookingLine.status != 'cancelled'
                ).distinct().all()
                unavailable_room_ids = {r[0] for r in booked}
        except (ValueError, TypeError):
            pass

    # Load reviews for this accommodation
    reviews = Review.query.filter_by(idAccommodation=id).order_by(Review.createdAt.desc()).limit(10).all()
    
    return render_template('acomodationShow.html',
                           accommodation=accommodation,
                           checkin=checkin,
                           checkout=checkout,
                           unavailable_room_ids=unavailable_room_ids,
                           reviews=reviews)


# =========================
# DELETE
# =========================
# Solo puede eliminarlo la company
@acomodation_bp.route('/acomodation/delete/<int:id>', methods=['POST'])
def delete(id):

    if "user_id" not in session:
        flash('Debes iniciar sesión')
        return redirect(url_for('login'))

    accommodation = Accommodation.query.get_or_404(id)

    if session["user_id"] != accommodation.idCompany and session.get("role") != "admin":
        flash('No tienes permiso')
        return redirect(url_for('aco.home'))

    # Eliminar imagen asociada si existe
    if accommodation.image_url:
        image_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'equipo3/static/uploads'), 
                                 os.path.basename(accommodation.image_url))
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print(f"Error deleting image: {e}")

    db.session.delete(accommodation)
    db.session.commit()
    flash('Property deleted successfully!', 'success')
    return redirect(url_for('aco.home'))


# =========================
# EDIT
# =========================
# Solo puede editarlo la company
@acomodation_bp.route('/acomodation/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    if "user_id" not in session:
        flash('Debes iniciar sesión')
        return redirect(url_for('login'))

    accommodation = Accommodation.query.get_or_404(id)

    if session["user_id"] != accommodation.idCompany and session.get("role") != "admin": # changed ADMIN to admin
        flash('No tienes permiso')
        return redirect(url_for('aco.home'))

    if request.method == 'POST':
        accommodation.name = request.form['name']
        accommodation.address = request.form['address']
        accommodation.phoneNumber = request.form['phoneNumber']
        accommodation.web = request.form['web']
        accommodation.stars_quality = request.form['stars_quality']
        accommodation.description = request.form['description']
        accommodation.type = request.form['type']
        
        # Manejar subida de nueva imagen (opcional)
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                # Eliminar imagen anterior si existe
                if accommodation.image_url:
                    old_image_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'equipo3/static/uploads'), 
                                                 os.path.basename(accommodation.image_url))
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                # Guardar nueva imagen
                image_url = save_uploaded_file(file)
                if image_url:
                    accommodation.image_url = image_url

        db.session.commit()
        flash('Property updated successfully!', 'success')
        return redirect(url_for('aco.home'))
    
    # GET request - mostrar formulario de edición
    return render_template('acomodationEdit.html', accommodation=accommodation)

# =========================
# MANAGE ROOMS
# =========================
# Solo puede gestionarlo la company
@acomodation_bp.route('/acomodation/<int:id>/rooms', methods=['GET'])
def manage_rooms(id):
    if "user_id" not in session:
        return redirect(url_for('login'))
        
    accommodation = Accommodation.query.get_or_404(id)
    
    # Check ownership or admin
    if session["user_id"] != accommodation.idCompany and session.get("role") != "admin": # changed ADMIN to admin (lowercase based on User model default)
        flash('Permission denied')
        return redirect(url_for('aco.home'))

    return render_template('manage_rooms.html', accommodation=accommodation)

# =========================
# ADD ROOM
# =========================
# Solo puede añadirlo la company
@acomodation_bp.route('/acomodation/<int:id>/rooms/add', methods=['POST'])
def add_room(id):
    if "user_id" not in session:
        return redirect(url_for('login'))
        
    accommodation = Accommodation.query.get_or_404(id)
    
    if session["user_id"] != accommodation.idCompany and session.get("role") != "admin":
        flash('Permission denied')
        return redirect(url_for('aco.home'))
        
    from equipo3.models.Room import Room
    
    new_room = Room(
        idAccommodation=id,
        roomNumber=request.form['roomNumber'],
        type=request.form['type'],
        priceNight=request.form['priceNight'],
        capacity=request.form['capacity']
    )
    
    db.session.add(new_room)
    db.session.commit()
    
    flash('Room added successfully!')
    return redirect(url_for('aco.manage_rooms', id=id))

# =========================
# DELETE ROOM
# =========================
# Solo puede eliminarlo la company
@acomodation_bp.route('/acomodation/rooms/delete/<int:id>', methods=['POST'])
def delete_room(id):
    if "user_id" not in session:
        return redirect(url_for('login'))
        
    from equipo3.models.Room import Room
    room = Room.query.get_or_404(id)
    accommodation = Accommodation.query.get(room.idAccommodation)
    
    if session["user_id"] != accommodation.idCompany and session.get("role") != "admin":
        flash('Permission denied')
        return redirect(url_for('aco.home'))
        
    db.session.delete(room)
    db.session.commit()
    
    flash('Room deleted successfully!')
    return redirect(url_for('aco.manage_rooms', id=accommodation.id))
