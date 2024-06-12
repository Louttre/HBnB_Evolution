import json
import uuid
from datetime import datetime
from .crud import CRUD
from .storage_utils import read_storage, write_storage


class User(CRUD):

    storage_file = 'user_storage.json'

    def __init__(self, first_name, last_name, email, password):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.hosted_places = []
        self.reviews = []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f"ID:{self.id}: {self.last_name}_{self.first_name}<{self.email}>"

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'hosted_places': self.hosted_places,
            'reviews': self.reviews,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def read_storage(cls):
        try:
            with open(cls.storage_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    @classmethod
    def write_storage(cls, storage):
        with open(cls.storage_file, 'w') as file:
            json.dump(storage, file, indent=4)

    @classmethod
    def create(cls, data):
        storage = cls.read_storage()
        user = User(**data)
        storage[user.id] = user.to_dict()
        cls.write_storage(storage)
        return user

    @classmethod
    def read(cls, id):
        storage = cls.read_storage()
        user_data = storage.get(id)
        if user_data:
            return User(**user_data)
        return None

    @classmethod
    def update(cls, id, data):
        storage = cls.read_storage()
        user_data = storage.get(id)
        if user_data:
            user = User(**user_data)
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.updated_at = datetime.utcnow()
            storage[id] = user.to_dict()
            cls.write_storage(storage)
            return user
        return None

    @classmethod
    def get_user(cls, id):
        user = cls.read(id)
        if user is None:
            raise ValueError("User not found")
        return user

    @classmethod
    def delete(cls, id):
        storage = cls.read_storage()
        if id in storage:
            user = storage.pop(id)
            cls.write_storage(storage)
            return User(**user)
        return None
