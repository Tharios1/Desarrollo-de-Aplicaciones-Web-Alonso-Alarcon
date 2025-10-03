from flask import Flask, render_template, request, redirect, url_for, flash
import os
from database import db
from utilis.validations import validate_aviso

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = "clave-secreta"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def parse_contactos(form):
    contactos = []
    for key, value in form.items():
        if key.startswith("contactos"):
            partes = key.split("[")
            idx = int(partes[1][:-1])
            campo = partes[2][:-1]
            while len(contactos) <= idx:
                contactos.append({})
            contactos[idx][campo] = value.strip()

    # filtrar los que estén realmente vacíos
    contactos = [c for c in contactos if c.get("nombre") and c.get("identificador")]
    return contactos

def guardar_fotos(files):
    fotos = []
    for f in files:
        if f and f.filename.strip() != "":   
            ruta = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
            f.save(ruta)
            fotos.append({"ruta_archivo": ruta, "nombre_archivo": f.filename})
    return fotos

@app.route("/")
def index():
    avisos = db.obtener_ultimos_avisos()
    return render_template("index.html", avisos=avisos)

@app.route("/ver-aviso")
def ver_avisos():
    page = int(request.args.get("page", 1))
    per_page = 5
    offset = (page - 1) * per_page
    avisos = db.listar_avisos(offset=offset, limit=per_page)
    return render_template("listado.html", avisos=avisos, page=page)

@app.route("/detalle/<int:aviso_id>")
def detalle(aviso_id):
    aviso = db.obtener_aviso(aviso_id)
    if not aviso:
        return redirect(url_for("index"))
    return render_template("detalle.html", aviso=aviso)



@app.route("/registrar-aviso", methods=["GET", "POST"])
def registrar_aviso():
    
    if request.method == "POST":
        data = {
            "region": request.form.get("region"),
            "comuna_id": request.form.get("comuna_id"),
            "sector": request.form.get("sector"),
            "nombre": request.form.get("nombre"),
            "email": request.form.get("email"),
            "celular": request.form.get("telefono"),
            "tipo": request.form.get("tipo"),
            "cantidad": request.form.get("cantidad"),
            "edad": request.form.get("edad"),
            "unidad_medida": request.form.get("unidad_medida"),
            "fecha_entrega": request.form.get("fechaEntrega"),
            "descripcion": request.form.get("descripcion"),
        }
        fotos_archivos = request.files.getlist("fotos")
        contactos = parse_contactos(request.form)
        fotos_validacion = [f for f in fotos_archivos if f and f.filename.strip() != ""]
        fotos = guardar_fotos(fotos_validacion)

        if not validate_aviso(data, contactos, fotos_validacion):
            return redirect(url_for("registrar_aviso"))
        
        aviso_id = db.insertar_aviso(data, contactos, fotos)
        flash("Aviso publicado con éxito ", "success")
        return redirect(url_for("index", aviso_id=aviso_id))
    session = db.get_session()
    regiones = session.query(db.Region).all()
    comunas = session.query(db.Comuna).all()
    session.close()
    return render_template("agregar.html", regiones=regiones, comunas=comunas)

if __name__ == "__main__":
    app.run(debug=True)
