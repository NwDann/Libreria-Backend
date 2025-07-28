# Instalar faker = pip install faker
import random
from datetime import date, timedelta
from sqlalchemy.orm import Session
from faker import Faker
from src.database.core import Base, engine

from src.entities.user import Usuario, TipoUsuarioEnum, EstadoUsuarioEnum
from src.entities.student import Alumno
from src.entities.teacher import Profesor
from src.entities.book import Libro
from src.entities.copyBook import Ejemplar
from src.entities.loan import Prestamo
from src.entities.loanHistory import PrestamoHist
from src.entities.penalty import Multa
from src.entities.penaltyHistory import MultaHist
from src.entities.recomendation import Recomendacion

Base.metadata.create_all(bind=engine)

fake = Faker()
session = Session(bind=engine)

# Crear usuarios (5 alumnos, 3 profesores)
usuarios = []
alumnos = []
profesores = []

# Crear alumnos
for i in range(5):
    user_id = 1000000000 + i  # Simula cédula
    user = Usuario(
        id=user_id,
        password_hash=f"pass{i}",  # sin hashear
        email=fake.unique.email(),
        nombre=fake.first_name(),
        apellido1=fake.last_name(),
        apellido2=fake.last_name(),
        ciudad=fake.city(),
        estado=EstadoUsuarioEnum.ACTIVO,
        tipo=TipoUsuarioEnum.ALUMNO
    )
    usuarios.append(user)

# Crear profesores
for i in range(3):
    user_id = 2000000000 + i
    user = Usuario(
        id=user_id,
        password_hash=f"pass{i+5}",  # sin hashear
        email=fake.unique.email(),
        nombre=fake.first_name(),
        apellido1=fake.last_name(),
        apellido2=fake.last_name(),
        ciudad=fake.city(),
        estado=EstadoUsuarioEnum.ACTIVO,
        tipo=TipoUsuarioEnum.PROFESOR
    )
    usuarios.append(user)

session.add_all(usuarios)
session.commit()

for u in usuarios:
    if u.tipo == TipoUsuarioEnum.ALUMNO:
        alumno = Alumno(
            usuario_id=u.id,
            telefono_padres=fake.phone_number()
        )
        alumnos.append(alumno)
    elif u.tipo == TipoUsuarioEnum.PROFESOR:
        profesor = Profesor(
            usuario_id=u.id,
            departamento=fake.word()
        )
        profesores.append(profesor)

session.add_all(alumnos + profesores)
session.commit()


# Crear libros
libros = []
for i in range(10):
    libro = Libro(
        isbn=fake.isbn13(),
        titulo=fake.sentence(nb_words=4),
        autor=fake.name(),
        num_paginas=random.randint(100, 800),
        total_ejemplares=3,
        portada_uri=fake.image_url()
    )
    libros.append(libro)

session.add_all(libros)
session.commit()

# Crear ejemplares
ejemplares = []
for libro in libros:
    for i in range(3):
        ej = Ejemplar(
            libro_id=libro.id,
            codigo=f"{libro.id}-{i}",
            disponible=True,
            fecha_adquisicion=date.today() - timedelta(days=random.randint(0, 1000)),
            observaciones=None
        )
        ejemplares.append(ej)

session.add_all(ejemplares)
session.commit()

# Crear recomendaciones
recomendaciones = []
for _ in range(10):
    origen, destino = random.sample(libros, 2)
    rec = Recomendacion(
        origen_id=origen.id,
        recomendado_id=destino.id,
        comentario=fake.sentence()
    )
    recomendaciones.append(rec)

session.add_all(recomendaciones)
session.commit()

# Crear préstamos actuales y en historial
prestamos = []
prestamos_hist = []
multas = []
multas_hist = []

for user in usuarios:
    for _ in range(1):
        ej = random.choice(ejemplares)
        fecha_prestamo = date.today() - timedelta(days=random.randint(1, 30))
        fecha_prevista = fecha_prestamo + timedelta(days=7 if user.tipo == TipoUsuarioEnum.ALUMNO else 30)
        prestamo = Prestamo(
            usuario_id=user.id,
            ejemplar_id=ej.id,
            fecha_prestamo=fecha_prestamo,
            fecha_prevista=fecha_prevista
        )
        prestamos.append(prestamo)

        # Historial simulado
        devolucion = fecha_prevista + timedelta(days=random.randint(0, 5))
        estado = devolucion <= fecha_prevista
        multa_obj = None

        if not estado:
            dias_multa = (devolucion - fecha_prevista).days
            multa_obj = Multa(
                usuario_id=user.id,
                fecha_inicio=devolucion,
                fecha_fin=devolucion + timedelta(days=dias_multa * 2)
            )
            session.add(multa_obj)
            session.flush()  # Obtener multa.id

            multas_hist.append(MultaHist(
                usuario_id=user.id,
                fecha_inicio=devolucion,
                fecha_fin=devolucion + timedelta(days=dias_multa * 2),
                dias_acumulados=dias_multa * 2
            ))

        prestamo_hist = PrestamoHist(
            usuario_id=user.id,
            ejemplar_id=ej.id,
            fecha_prestamo=fecha_prestamo,
            fecha_prevista=fecha_prevista,
            fecha_devolucion=devolucion,
            estado=estado,
            multa_id=multa_obj.id if multa_obj else None
        )
        prestamos_hist.append(prestamo_hist)

session.add_all(prestamos)
session.add_all(prestamos_hist)
session.add_all(multas_hist)
session.commit()

print("Datos insertados correctamente.")
