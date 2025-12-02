from app.modules.auth.models import Role, User
from app.modules.profile.models import UserProfile
# Usando la importación estándar para Flask-SQLAlchemy (asumo que está configurada)
from app import db # Importar la instancia de SQLAlchemy
from core.seeders.BaseSeeder import BaseSeeder 

# Lista estática de roles para que la app sepa qué nombres buscar
ROLES_A_INSERTAR = [
    {'name': 'admin', 'description': 'Acceso total y gestión de usuarios.'},
    {'name': 'curator', 'description': 'Puede añadir, editar y eliminar contenido.'},
    {'name': 'standard user', 'description': 'Usuario autenticado.'},
]

# --- Función auxiliar para obtener Roles por Nombre (Útil fuera del Seeder) ---
def get_role_id_by_name(role_name):
    """Retorna el ID del rol por su nombre. Útil para el registro de usuarios."""
    role = Role.query.filter_by(name=role_name).first()
    if role:
        return role.id
    # Si el rol no existe, levantamos una excepción para forzar el seeding de roles
    raise ValueError(f"El rol '{role_name}' no existe en la base de datos. Ejecuta los seeders de Roles.")

class AuthSeeder(BaseSeeder):

    priority = 1  

    def run(self):
        
        # --- 1. Verificando y creando Roles ---
        print("--- 1. Verificando y creando Roles ---")
        
        for role_data in ROLES_A_INSERTAR:
            role = Role.query.filter_by(name=role_data['name']).first()
            
            if not role:
                new_role = Role(**role_data)
                db.session.add(new_role)
                print(f"-> Rol creado: {role_data['name']}")
                
        # CRÍTICO: Commit después de crear roles, antes de usarlos
        db.session.commit()
        
        # Obtener los IDs reales de los objetos (NO usar IDs fijos como 1, 2)
        admin_role = Role.query.filter_by(name='admin').first()


        # --- 2. Creación del Usuario Administrador ---
        if admin_role and not User.query.filter_by(email='admin@uvl.com').first():
            
            admin_user = User(
                email='admin@uvl.com', 
                password='123456', 
                role_id=admin_role.id # Usa el ID dinámico
            )
            # El método self.seed() maneja db.session.add y commit
            seeded_admin = self.seed([admin_user])[0] 
            
            # Creación del perfil del Administrador
            admin_profile_data = {
                "user_id": seeded_admin.id, 
                "orcid": "ADMIN",
                "affiliation": "CervezaHub Administration",
                "name": "Super",
                "surname": "Admin",
            }
            admin_profile = UserProfile(**admin_profile_data)
            self.seed([admin_profile])

            print("-> Usuario Administrador creado: admin@uvl.com con perfil.")

        standard_role = Role.query.filter_by(name='standard user').first()

        # --- 3. Creación de Usuarios de Prueba ---
        users_to_seed = []
        user_data_list = [
            {"email": "user1@example.com", "password": "1234"},
            {"email": "user2@example.com", "password": "1234"},
        ]
        names = [("John", "Doe"), ("Jane", "Doe")]

        print("--- Verificando y creando Usuarios de Prueba ---")

        for data in user_data_list:
            if standard_role and not User.query.filter_by(email=data['email']).first():
                new_user = User(
                    email=data['email'], 
                    password=data['password'], 
                    role_id=standard_role.id # Usa el ID dinámico
                )
                users_to_seed.append(new_user)
                print(f"-> Usuario de prueba añadido: {data['email']}")
            
        if users_to_seed:
            seeded_users = self.seed(users_to_seed)
        else:
            seeded_users = User.query.filter(
                User.email.in_(['user1@example.com', 'user2@example.com'])
            ).all()

        # --- 4. Creación de Perfiles de Usuario de Prueba ---
        user_profiles_to_create = []
        
        for user, name in zip(seeded_users, names):
            # Asumo que 'user.profile' usa una relación de SQLAlchemy
            if user and not user.profile: 
                profile_data = {
                    "user_id": user.id,
                    "orcid": "",
                    "affiliation": "Some University",
                    "name": name[0],
                    "surname": name[1],
                }
                user_profile = UserProfile(**profile_data)
                user_profiles_to_create.append(user_profile)

        if user_profiles_to_create:
            self.seed(user_profiles_to_create)
            print(f"--- {len(user_profiles_to_create)} Perfiles de prueba creados. ---")
        else:
             print("--- 0 Perfiles de prueba creados (ya existen). ---")

    def unseed(self):
        # Puedes implementar la lógica para eliminar los datos de prueba aquí.
        pass