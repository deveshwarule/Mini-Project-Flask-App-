from flask import jsonify,Flask,request,Response,json,render_template
from flask_sqlalchemy import SQLAlchemy
import os

from flask_marshmallow import Marshmallow


# ----------------------------------------------------------------
class APIException(Exception):

    def __init__(self, message, status_code, payload):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        return rv


class InvalidPayload(APIException):

    def __init__(self, message='Invalid payload.', payload=None):
        super().__init__(message=message, status_code=400, payload=payload)

class ServerErrorException(APIException):

    def __init__(self, message='Something went wrong.', status_code=500, payload=None):
        super().__init__(message=message, status_code=status_code, payload=payload)


def handle_exception(error: APIException):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    response.name = error.message
    return response

def handle_general_exception(_):
    return handle_exception(ServerErrorException())

ma = Marshmallow()
app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("db_url")
db= SQLAlchemy(app)
marsh = Marshmallow(app)

class model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    add = db.Column(db.String(50),nullable=False)
    status = db.Column(db.Boolean, default=True)

class UserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    
    class Meta:
        model = model
        sqla_session = db.session
        load_instance = True

app.register_error_handler(InvalidPayload, handle_exception)

@app.route("/user",methods=["PUT"])
def user():
    schema = UserSchema(many=True)
    id = request.json.get("id")
    if id:
        if type(id) is not int:
            raise InvalidPayload(message="Invalid id")

        else:
            user = model.query.get_or_404(id)
            name = request.json.get('name')
            add = request.json.get("add")
            status = request.json.get("status")
            if type(status) is not bool:
                raise InvalidPayload(message=" status must be true or false...")
            if not name.replace(" ", "").isalpha():
                raise InvalidPayload(message="must be alpha...")
            user.name = name
            user.status = status
            user.add = add
            db.session.commit()
            return jsonify(
                {'id':user.id,'name':user.name,'add': user.add, 'status': user.status}
            )   
    else:
        name = request.json.get("name")
        add = request.json.get("add")
        status = request.json.get("status")
        if type(status) is not bool:
                raise InvalidPayload(message="status must be true or false...")
        if name.replace(" ", "").isalpha():
                user = model(name=name,add=add,status=status)
                db.session.add(user)
                db.session.commit()
                user_id = user.id
                db.session.close()
                data=model.query.filter_by(id=user_id)
                
                res = schema.dump(data)
                return jsonify(res),201
        else:
                raise InvalidPayload(message="must be alpha...")

if __name__ == "__main__":
    db.create_all()
    app.run()