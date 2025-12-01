import pytest

from app import create_app, db
<<<<<<< HEAD
from app.modules.auth.models import User
=======
# Importamos modelos y funciones necesarias para el setup de los tests
from app.modules.auth.models import User
from app.modules.auth.models import Role 
# Nota: Si login/logout están definidos en este mismo fichero, no hace falta importarlos
# Si están en un módulo separado, asegúrate que la ruta sea correcta. 
# Asumo que las defines en este fichero, así que comento la importación que puede fallar.
# from app.modules.conftest import login, logout 
>>>>>>> origin/trunk


@pytest.fixture(scope="session")
def test_app():
<<<<<<< HEAD
    """Create and configure a new app instance for each test session."""
    test_app = create_app("testing")

    with test_app.app_context():
        # Imprimir los blueprints registrados
=======
    """Crea y configura una nueva instancia de la aplicación Flask para la sesión de prueba."""
    # Asegúrate de que "testing" es el nombre de la configuración de prueba
    test_app = create_app("testing")

    with test_app.app_context():
        # Imprimir los blueprints registrados (útil para debug)
>>>>>>> origin/trunk
        print("TESTING SUITE (1): Blueprints registrados:", test_app.blueprints)
        yield test_app


@pytest.fixture(scope="module")
def test_client(test_app):
<<<<<<< HEAD

=======
    """
    Configura el cliente de prueba, inicializa la base de datos y crea un usuario inicial
    con su rol asociado. Se ejecuta una vez por módulo de prueba.
    """
>>>>>>> origin/trunk
    with test_app.test_client() as testing_client:
        with test_app.app_context():
            print("TESTING SUITE (2): Blueprints registrados:", test_app.blueprints)

<<<<<<< HEAD
            db.drop_all()
            db.create_all()
            """
            The test suite always includes the following user in order to avoid repetition
            of its creation
            """
            user_test = User(email="test@example.com", password="test1234")
            db.session.add(user_test)
            db.session.commit()
=======
            # 1. Limpiar y recrear la BD con los modelos actualizados
            db.drop_all()
            db.create_all()
            
            # ----------------------------------------------------------------------
            # 🔑 SOLUCIÓN: Crear el Rol base (ID=1) antes de crear el usuario.
            # Esto previene el error de clave foránea (IntegrityError: FOREIGN KEY... role_id).
            # ----------------------------------------------------------------------
            try:
                role_test = Role(id=1, name="user", description="Default user role")
                db.session.add(role_test)
            except Exception as e:
                # Capturamos cualquier error en la creación del Role, aunque sea improbable
                print(f"⚠️ Error al crear el objeto Role(id=1): {e}")
                
            """
            El conjunto de pruebas siempre incluye este usuario para evitar su repetición.
            """
            # 2. Crear el Usuario referenciando el Rol
            user_test = User(
                email="test@example.com", 
                password="test1234",
                role_id=1, # <-- La clave foránea apunta al rol que acabamos de crear
            ) 
            
            db.session.add(user_test)
            db.session.commit() # <-- ¡Esto ya no debería fallar!
>>>>>>> origin/trunk

            print("Rutas registradas:")
            for rule in test_app.url_map.iter_rules():
                print(rule)
            yield testing_client

<<<<<<< HEAD
=======
            # 3. Limpieza al finalizar el módulo
>>>>>>> origin/trunk
            db.session.remove()
            db.drop_all()


@pytest.fixture(scope="function")
def clean_database():
<<<<<<< HEAD
=======
    """Limpia y recrea la DB antes y después de cada función de prueba (si se usa)."""
>>>>>>> origin/trunk
    db.session.remove()
    db.drop_all()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
    db.create_all()


def login(test_client, email, password):
    """
<<<<<<< HEAD
    Authenticates the user with the credentials provided.

    Args:
        test_client: Flask test client.
        email (str): User's email address.
        password (str): User's password.

    Returns:
        response: POST login request response.
    """
    response = test_client.post("/login", data=dict(email=email, password=password), follow_redirects=True)
=======
    Autentica al usuario con las credenciales proporcionadas mediante una petición POST a /login.
    """
    response = test_client.post(
        "/login", 
        data=dict(email=email, password=password), 
        follow_redirects=True
    )
>>>>>>> origin/trunk
    return response


def logout(test_client):
    """
<<<<<<< HEAD
    Logs out the user.

    Args:
        test_client: Flask test client.

    Returns:
        response: Response to GET request to log out.
    """
    return test_client.get("/logout", follow_redirects=True)
=======
    Cierra la sesión del usuario mediante una petición GET a /logout.
    """
    return test_client.get("/logout", follow_redirects=True)
>>>>>>> origin/trunk
