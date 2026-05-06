from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Booking

main = Blueprint("main", __name__)


def calculate_fare(truck_type):
    fares = {
        "Pickup": 1200,
        "Mini Truck": 1800,
        "Covered Van": 2500,
        "Large Truck": 4000,
    }
    return fares.get(truck_type, 1500)


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/book", methods=["GET", "POST"])
def book_truck():
    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        phone = request.form.get("phone", "").strip()
        pickup_location = request.form.get("pickup_location", "").strip()
        drop_location = request.form.get("drop_location", "").strip()
        truck_type = request.form.get("truck_type", "").strip()
        goods_details = request.form.get("goods_details", "").strip()

        if not customer_name or not phone or not pickup_location or not drop_location or not truck_type:
            flash("Please fill all required fields.", "danger")
            return redirect(url_for("main.book_truck"))

        booking = Booking(
            customer_name=customer_name,
            phone=phone,
            pickup_location=pickup_location,
            drop_location=drop_location,
            truck_type=truck_type,
            goods_details=goods_details,
            estimated_fare=calculate_fare(truck_type),
            status="Pending",
        )

        db.session.add(booking)
        db.session.commit()

        flash("Your truck request has been submitted successfully!", "success")
        return redirect(url_for("main.jobs"))

    return render_template("book.html")


@main.route("/jobs")
def jobs():
    bookings = Booking.query.order_by(Booking.id.desc()).all()
    return render_template("jobs.html", bookings=bookings)


@main.route("/accept/<int:booking_id>", methods=["POST"])
def accept_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if booking.status == "Pending":
        booking.status = "Accepted"
        db.session.commit()
        flash("Booking accepted successfully!", "success")
    else:
        flash("This booking has already been accepted.", "warning")

    return redirect(url_for("main.jobs"))


@main.route("/dashboard")
def dashboard():
    total_bookings = Booking.query.count()
    pending_bookings = Booking.query.filter_by(status="Pending").count()
    accepted_bookings = Booking.query.filter_by(status="Accepted").count()
    recent_bookings = Booking.query.order_by(Booking.id.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_bookings=total_bookings,
        pending_bookings=pending_bookings,
        accepted_bookings=accepted_bookings,
        recent_bookings=recent_bookings,
    )
