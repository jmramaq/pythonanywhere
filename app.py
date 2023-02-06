from flask import Flask, request, jsonify, session, url_for, redirect, render_template, flash
import pickle
import joblib

# IMPORTAR FORMULARIO CUSTOM
# from flower_form import FlowerForm

app = Flask(__name__)

app.config['DEBUG']=True # Evita tener que re-ejecutar la aplicación en caso de fallo. Se actualizan los cambios cada vez que se guardan

classifier_loaded = joblib.load('saved_models/randomForest.pkl')

# Route for the GitHub webhook

@app.route('/git_update', methods=['POST'])
def git_update():
    repo = git.Repo('./Flask')
    origin = repo.remotes.origin
    repo.create_head('main',
                     origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200

@app.route('/', methods=["GET"]) # No es necesario otros métodos como POST, dado que es la página principal.
# Creamos el formulario de la página inicial
def index():
    return "Página Inicial. Homepage. Agregado posterior."


# Creamos el formulario de la página v1
@app.route('/api/v1/predict', methods=['GET'])
def predict():

    model = pickle.load(open('finished_model.pkl','rb'))
    tv = float(request.args.get('tv', None))
    radio = float(request.args.get('radio', None))
    newspaper = float(request.args.get('newspaper', None))

    if tv is None or radio is None or newspaper is None:
        return "Args empty, the data are not enough to predict"
    else:
        prediction = model.predict([[tv,radio,newspaper]])

    return jsonify({'predictions': prediction[0]})
        

app.run()
