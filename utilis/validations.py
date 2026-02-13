import re
import filetype
from datetime import datetime


def validate_region(region_id: str) -> bool:
    return bool(region_id and region_id.strip())

def validate_comuna(comuna_id: str) -> bool:
    return bool(comuna_id and comuna_id.strip())

def validate_nombre(nombre: str) -> bool:
    if not nombre:
        return False
    return 3 <= len(nombre.strip()) <= 200

def validate_email(email: str) -> bool:
    if not email:
        return False
    if len(email) < 15:
        return False
    
    email_regex = r"^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    return re.match(email_regex, email) is not None

def validate_celular(celular: str) -> bool:
    if not celular:
        return True  
    return re.match(r"^\+\d{3}\.\d{8,9}$", celular) is not None

def validate_tipo(tipo: str) -> bool:
    return tipo in {"gato", "perro"}

def validate_cantidad(cantidad: str) -> bool:
    try:
        return int(cantidad) >= 1
    except:
        return False

def validate_edad(edad: str) -> bool:
    try:
        return int(edad) >= 1
    except:
        return False

def validate_unidad_medida(unidad: str) -> bool:
    return unidad in {"m", "a"}  

def validate_fecha_entrega(fecha: str) -> bool:
    try:
        fecha_ent = datetime.strptime(fecha, "%Y-%m-%d")
        return fecha_ent.date() >= datetime.now().date()
    except:
        return False
    
def validate_contacto(nombre: str, identificador: str) -> bool:
    if not nombre or nombre.strip() == "":
        return True
    if not identificador:
        return False
    return 4 <= len(identificador.strip()) <= 50

def validate_foto(file) -> bool:
    if file is None or file.filename == "":
        return False
    
    ftype = filetype.guess(file)
    
    return ftype.extension in {"png", "jpg", "jpeg", "gif"} and \
           ftype.mime in {"image/png", "image/jpeg", "image/gif"}

def validate_fotos(files) -> bool:
    valid_files = [f for f in files if f and f.filename.strip() !=""]
    if not valid_files or len(valid_files)>5:
        return False
    return all(validate_foto(f) for f in valid_files)

def validate_aviso(data, contactos, fotos) -> bool:
    ok_region = validate_region(data.get("region"))
    ok_comuna = validate_comuna(data.get("comuna_id"))
    ok_nombre = validate_nombre(data.get("nombre"))
    ok_email = validate_email(data.get("email"))
    ok_celular = validate_celular(data.get("celular"))
    ok_tipo = validate_tipo(data.get("tipo"))
    ok_cantidad = validate_cantidad(data.get("cantidad"))
    ok_edad = validate_edad(data.get("edad"))
    ok_unidad = validate_unidad_medida(data.get("unidad_medida"))
    ok_fecha = validate_fecha_entrega(data.get("fecha_entrega"))
    ok_contactos = all(validate_contacto(c.get("nombre"), c.get("identificador")) for c in contactos)
    ok_fotos = validate_fotos(fotos)

    return (
        ok_region and ok_comuna and ok_nombre and ok_email and ok_celular
        and ok_tipo and ok_cantidad and ok_edad and ok_unidad and ok_fecha
        and ok_contactos and ok_fotos
    )