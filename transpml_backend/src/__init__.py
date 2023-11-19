import os
from flask import Flask, flash, request, jsonify
from werkzeug.utils import secure_filename
from src.database import Codes, db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config == None:
        app.config.from_mapping(SECRET_KEY="dev",
                                SQLALCHEMY_DATABASE_URI="sqlite:///codes.db",
                                UPLOAD_FOLDER="D:/Web Development/Atharva's Final Year Project/TranspML_Ledger/transpml_backend/uploaded_files")
    else:
        app.config.from_mapping(test_config)

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            file = request.files['file']
            code = Codes (
                user_account=request.form["user_account"],
                model_name=file.filename
            )
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            db.session.add(code)
            db.session.commit()
            return jsonify({
                "user_account": code.user_account,
                "model_name": file.filename
            })
        
    @app.route('/fetch', methods=['GET'])
    def fetch_code():
        data = Codes.query.all()
        results = {"data": [{
            "id": code.id,
            "user_account": code.user_account,
            "model_name": code.model_name
        } for code in data]}
        return jsonify(results)

    @app.route('/health_check', methods=['GET'])
    def health_check():
        results = {"health_check": "success"}
        return jsonify(results)

    db.app = app
    db.init_app(app)
    
    return app