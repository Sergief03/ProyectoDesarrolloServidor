# controllers/accommodation_bp.py
from flask import Blueprint, request, jsonify
from models import db
from models import Accommodation, AccommodationBookingLine, Review, Room, User
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for


accommodation_bp = Blueprint('accommodation', __name__, url_prefix='/accommodation',template_folder='../templates')

# =========================
# FORMULARIO CREAR ALOJAMIENTO
# =========================
@accommodation_bp.route('/new', methods=['GET','POST'])
def create_accommodation():

    if request.method == 'POST':
        try:
            acc = Accommodation(
                name=request.form.get('name'),
                address=request.form.get('address'),
                phoneNumber=request.form.get('phoneNumber'),
                web=request.form.get('web'),
                stars_quality=request.form.get('stars_quality'),
                description=request.form.get('description'),
                type=request.form.get('type'),
                id_company=request.form.get('id_company')
            )

            db.session.add(acc)
            db.session.commit()

            return redirect(url_for('accommodation.list_accommodations'))

        except Exception as e:
            db.session.rollback()
            return render_template('accommodation_new.html', error=str(e))

    users = User.query.all()
    return render_template('accommodation_new.html', users=users)

# =========================
# LISTAR ALOJAMIENTOS
# =========================
@accommodation_bp.route('/', methods=['GET'])
def list_accommodations():
    accommodations = Accommodation.query.all()
    return render_template('accommodations.html', accommodations=accommodations)

# =========================
# VER ALOJAMIENTO
# =========================
@accommodation_bp.route('/<int:id>', methods=['GET'])
def view_accommodation(id):
    accommodation = Accommodation.query.get_or_404(id)
    return render_template('accommodation_detail.html', accommodation=accommodation)


# =========================
# ELIMINAR ALOJAMIENTO
# =========================
@accommodation_bp.route('/delete/<int:id>', methods=['POST'])
def delete_accommodation(id):

    accommodation = Accommodation.query.get_or_404(id)

    try:
        db.session.delete(accommodation)
        db.session.commit()
        return redirect(url_for('accommodation.list_accommodations'))

    except Exception as e:
        db.session.rollback()
        return str(e)


# =========================
# FORMULARIO RESERVA
# =========================
@accommodation_bp.route('/book', methods=['GET', 'POST'])
def book_accommodation():
    if request.method == 'POST':
        user_id = request.form.get('userId')
        accommodation_id = request.form.get('accommodationId')
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')
        total_price = request.form.get('totalPrice')

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if start_date > end_date:
                return render_template('book.html', error='La fecha de inicio no puede ser posterior a la fecha de fin.')

            booking = AccommodationBookingLine(
                idUser=user_id,
                idAccommodation=accommodation_id,
                startDate=start_date,
                endDate=end_date,
                totalPrice=total_price,
                status='pending'
            )

            db.session.add(booking)
            db.session.commit()
            return redirect(url_for('accommodation.list_user_bookings_html', user_id=user_id))

        except Exception as e:
            db.session.rollback()
            return render_template('book.html', error=str(e))

    accommodations = Accommodation.query.all()
    users = User.query.all()
    return render_template('book.html', accommodations=accommodations, users=users)


# =========================
# FORMULARIO RESEÑA
# =========================
@accommodation_bp.route('/review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        user_id = request.form.get('idUser')
        accommodation_id = request.form.get('idAccommodation')
        rating = request.form.get('ratingStars')
        comment = request.form.get('reviewComment')

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return render_template('review.html', error='La calificación debe estar entre 1 y 5.')

            review = Review(
                idUser=user_id,
                idAccommodation=accommodation_id,
                ratingStars=rating,
                reviewComment=comment
            )
            db.session.add(review)
            db.session.commit()
            return redirect(url_for('accommodation.list_accommodation_reviews_html', accommodation_id=accommodation_id))

        except Exception as e:
            db.session.rollback()
            return render_template('review.html', error=str(e))

    accommodations = Accommodation.query.all()
    users = User.query.all()
    return render_template('review.html', accommodations=accommodations, users=users)


# =========================
# LISTAR RESERVAS (JSON)
# =========================
@accommodation_bp.route('/bookings/json/<int:user_id>', methods=['GET'])
def list_user_bookings(user_id):
    bookings = AccommodationBookingLine.query.filter_by(idUser=user_id).all()
    return jsonify([{
        'id': b.id,
        'accommodationId': b.idAccommodation,
        'startDate': b.startDate.isoformat(),
        'endDate': b.endDate.isoformat(),
        'totalPrice': float(b.totalPrice),
        'status': b.status
    } for b in bookings])


# =========================
# LISTAR RESERVAS (HTML)
# =========================
@accommodation_bp.route('/bookings/<int:user_id>', methods=['GET'])
def list_user_bookings_html(user_id):
    bookings = AccommodationBookingLine.query.filter_by(idUser=user_id).all()
    return render_template('bookings.html', bookings=bookings)


# =========================
# LISTAR RESEÑAS (JSON)
# =========================
@accommodation_bp.route('/reviews/json/<int:accommodation_id>', methods=['GET'])
def list_accommodation_reviews(accommodation_id):
    reviews = Review.query.filter_by(idAccommodation=accommodation_id).all()
    return jsonify([{
        'idReview': r.id,
        'idUser': r.idUser,
        'ratingStars': r.ratingStars,
        'reviewComment': r.reviewComment,
        'createdAt': r.createdAt.isoformat()
    } for r in reviews])


# =========================
# LISTAR RESEÑAS (HTML)
# =========================
@accommodation_bp.route('/reviews/<int:accommodation_id>', methods=['GET'])
def list_accommodation_reviews_html(accommodation_id):
    reviews = Review.query.filter_by(idAccommodation=accommodation_id).all()
    return render_template('reviews.html', reviews=reviews)