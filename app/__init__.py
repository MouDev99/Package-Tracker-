from flask import Flask, redirect, render_template
from flask_migrate import Migrate
from flask_login import current_user, LoginManager, login_required
from .config import Configuration
from app.forms.shipping_form import ShippingForm
from app.routes.session import session_bp
from .models import db, Package, User


app = Flask(__name__)
app.config.from_object(Configuration)

app.register_blueprint(session_bp)


db.init_app(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = "session.login"

@login.user_loader
def load_user(id):
    return User.query.get(id)


@app.route("/")
@login_required
def index():
    rows = Package.query.filter(Package.user_id==current_user.id).all()
    user_info = {
        "name": current_user.user_name,
        "email": current_user.email
    }
    return render_template("package_status.html", rows=rows, user=user_info)


@app.route("/new_package", methods=["GET", "POST"])
@login_required
def add_new_package():
    form = ShippingForm()
    if form.validate_on_submit():
        data = form.data
        package_data = {"name": data["sender_name"],
                        "recipient": data["recipient_name"],
                        "destination": data["destination"],
                        "origin": data["origin"],
                        "location": data["origin"]
                        }
        user = User.query.get(current_user.id)
        new_package = Package(**package_data, user=user)
        db.session.add(new_package)
        db.session.commit()

        Package.advance_all_locations()
        return redirect("/")

    return render_template("shipping_request.html", form=form)
