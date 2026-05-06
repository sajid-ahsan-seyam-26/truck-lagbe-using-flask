from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    pickup_location = db.Column(db.String(200), nullable=False)
    drop_location = db.Column(db.String(200), nullable=False)

    truck_type = db.Column(db.String(100), nullable=False)
    goods_details = db.Column(db.Text, nullable=True)

    estimated_fare = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="Pending")

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Booking {self.id} - {self.customer_name}>"
