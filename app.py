from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from sqlalchemy import func
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



@app.route("/api/comentarios", methods=["POST"])
def agregar_comentario():
    data = request.get_json()
    nombre = data.get("nombre", "").strip()
    texto = data.get("texto", "").strip()
    aviso_id = data.get("aviso_id")

    if len(nombre) < 3 or len(nombre) > 80 or len(texto) < 5:
        return jsonify({"error": "Datos inválidos"}), 400
    
    session = db.get_session()
    try:
        nuevo = db.Comentario(nombre=nombre, texto=texto, aviso_id=aviso_id)
        session.add(nuevo)
        session.commit()
        return jsonify({
            "id": nuevo.id,
            "nombre": nuevo.nombre,
            "texto": nuevo.texto,
            "fecha": nuevo.fecha.strftime("%Y-%m-%d %H:%M")
        }), 201
    finally:
        session.close()

@app.route("/api/comentarios/<int:aviso_id>")
def listar_comentarios(aviso_id):
    session = db.get_session()
    try:
        comentarios = session.query(db.Comentario).filter_by(aviso_id=aviso_id).order_by(db.Comentario.fecha.desc()).all()
        return jsonify([
            {
                "nombre": c.nombre,
                "texto": c.texto,
                "fecha": c.fecha.strftime("%Y-%m-%d %H:%M")
            } for c in comentarios
        ])
    finally:
        session.close()


@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")

@app.route("/api/estadisticas")
def api_estadisticas():
    session = db.get_session()
    try:

        
        avisos_por_dia = (
            session.query(func.date(db.AvisoAdopcion.fecha_ingreso), func.count(db.AvisoAdopcion.id))
            .group_by(func.date(db.AvisoAdopcion.fecha_ingreso))
            .order_by(func.date(db.AvisoAdopcion.fecha_ingreso))
            .all()
        )

       
        avisos_por_tipo = (
            session.query(db.AvisoAdopcion.tipo, func.count(db.AvisoAdopcion.id))
            .group_by(db.AvisoAdopcion.tipo)
            .all()
        )

        
        avisos_por_mes_tipo = (
            session.query(
                func.extract("month", db.AvisoAdopcion.fecha_ingreso).label("mes"),
                db.AvisoAdopcion.tipo,
                func.count(db.AvisoAdopcion.id)
            )
            .group_by("mes", db.AvisoAdopcion.tipo)
            .order_by("mes")
            .all()
        )


        return jsonify({
            "por_dia": [{"fecha": f.strftime("%Y-%m-%d %H:%M"), "cantidad": c} for f, c in avisos_por_dia],
            "por_tipo": [{"tipo": t, "cantidad": c} for t, c in avisos_por_tipo],
            "por_mes_tipo": [{"mes": int(m), "tipo": t, "cantidad": c} for m, t, c in avisos_por_mes_tipo]
        })
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
