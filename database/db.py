from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, joinedload
from datetime import datetime


DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Region(Base):
    __tablename__= "region"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    comunas = relationship("Comuna", back_populates="region")

class Comuna(Base):
    __tablename__= "comuna"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)
    region = relationship("Region", back_populates="comunas")
    avisos = relationship("AvisoAdopcion", back_populates="comuna")


class AvisoAdopcion(Base):
    __tablename__ = "aviso_adopcion"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(DateTime, default=datetime.now, nullable=False)
    comuna_id = Column(Integer, ForeignKey("comuna.id"), nullable=False)
    sector = Column(String(100))
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15))
    tipo = Column(Enum("gato", "perro"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_medida = Column(Enum("a", "m"), nullable=False)
    fecha_entrega = Column(DateTime, nullable=False)
    descripcion = Column(Text)

    comuna = relationship("Comuna", back_populates="avisos")
    fotos = relationship("Foto", back_populates="aviso", cascade="all, delete-orphan")
    contactos = relationship("ContactarPor", back_populates="aviso", cascade="all, delete-orphan")
    comentarios = relationship("Comentario", back_populates="aviso", cascade="all, delete-orphan")

class Foto(Base):
    __tablename__ = "foto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    aviso_id = Column(Integer, ForeignKey("aviso_adopcion.id"), nullable=False)
    aviso = relationship("AvisoAdopcion", back_populates="fotos")

class ContactarPor(Base):
    __tablename__ = "contactar_por"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum("whatsapp", "telegram", "X", "instagram", "tiktok", "otra"), nullable=False)
    identificador = Column(String(150), nullable=False)
    aviso_id = Column(Integer, ForeignKey("aviso_adopcion.id"), nullable=False)

    aviso = relationship("AvisoAdopcion", back_populates="contactos")



class Comentario(Base):
    __tablename__ = "comentario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    texto = Column(String(300), nullable=False)
    fecha = Column(DateTime, default=datetime.now, nullable=False)
    aviso_id = Column(Integer, ForeignKey("aviso_adopcion.id"), nullable=False)

    aviso = relationship("AvisoAdopcion", back_populates="comentarios")



def get_session():
    return SessionLocal()


def insertar_aviso(data, contactos, fotos):
    session = get_session()
    try:
        aviso = AvisoAdopcion(
            comuna_id=data["comuna_id"],
            sector = data["sector"],
            nombre=data["nombre"],
            email=data["email"],
            celular=data["celular"],
            tipo=data["tipo"],
            cantidad=data["cantidad"],
            edad=data["edad"],
            unidad_medida=data["unidad_medida"],
            fecha_entrega=data["fecha_entrega"],
            descripcion=data["descripcion"],
            fecha_ingreso=datetime.now()
        )

        session.add(aviso)
        session.flush()

        for c in contactos:
            contacto= ContactarPor( 
                aviso_id=aviso.id,
                nombre=c["nombre"],
                identificador=c["identificador"]
            )
            session.add(contacto)
        
        for f in fotos:
            foto = Foto(
                aviso_id=aviso.id,
                ruta_archivo=f["ruta_archivo"],
                nombre_archivo=f["nombre_archivo"]
            )
            session.add(foto)
        session.commit()
        return aviso.id
    
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def obtener_ultimos_avisos(limit=5):
    session = get_session()
    try:
        return(
            session.query(AvisoAdopcion)
            .options(joinedload(AvisoAdopcion.comuna),
                     joinedload(AvisoAdopcion.fotos),
                     joinedload(AvisoAdopcion.contactos))
            .order_by(AvisoAdopcion.fecha_ingreso.desc())
            .limit(limit)
            .all()
        )
    finally:
        session.close()


def listar_avisos(offset=0, limit=5):
    session = get_session()
    try:
        return(
            session.query(AvisoAdopcion)
            .options(joinedload(AvisoAdopcion.comuna),
                     joinedload(AvisoAdopcion.fotos),
                     joinedload(AvisoAdopcion.contactos))
            .order_by(AvisoAdopcion.fecha_ingreso.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
    finally:
        session.close()



def obtener_aviso(id_aviso):
    session = get_session()
    try:
        return(
            session.query(AvisoAdopcion)
            .options(joinedload(AvisoAdopcion.comuna),
                     joinedload(AvisoAdopcion.fotos),
                     joinedload(AvisoAdopcion.contactos))
            .filter_by(id=id_aviso)
            .first()
            
        )
    finally:
        session.close()
