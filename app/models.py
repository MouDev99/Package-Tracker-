from flask_sqlalchemy import SQLAlchemy
from map.map import advance_delivery, DELIVERED
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin


db = SQLAlchemy()


class Package(db.Model):
    __tablename__ = "packages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    recipient = db.Column(db.String(20), nullable=False)
    origin = db.Column(db.String(20), nullable=False)
    destination = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    express_shipping = db.Column(db.Boolean)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="packages")

    @staticmethod
    def advance_all_locations():
        packages = Package.query.all()
        for package in packages:
            if package.location is not DELIVERED:
                package.location = advance_delivery(package.location,
                                                    package.destination)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    packages = relationship("Package", back_populates="user")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
