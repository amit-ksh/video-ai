import bcrypt
from flask_jwt_extended import create_access_token


from app.app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    email = db.Column(db.String, nullable=False, unique=True)
    hashed_password = db.Column(db.String, nullable=False)

    @classmethod
    def create_user(cls, email, password):
        """Create new user

        Args:
            email (str): User email
            password (str): User password

        Returns:
            user: User object
        """
        user = cls(
            email=email,
            hashed_password=bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8"),
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def validate_user(cls, email, password):
        """Login user

        Args:
            email (str): User email
            password (str): User password

        Returns:
            user: User object
        """
        user = cls.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(
            password.encode("utf-8"), user.hashed_password.encode("utf-8")
        ):
            return user
        else:
            return None

    @classmethod
    def get_user_by_email(cls, user_email):
        """Return a user by id

        Args:
            user_id (int): User id

        Returns:
            user: User object
        """
        return cls.query.filter_by(email=user_email).first()

    def generate_access_token(self):
        """Generate access token

        Returns:
            str: Access token
        """
        return create_access_token(identity=self.id)

    def to_json(self):
        """Convert User object to JSON

        Returns:
            dict: User object as JSON
        """
        return dict(
            id=self.id, email=self.email, created_at=self.created_at.isoformat()
        )

    def __repr__(self):
        return f"<User {self.email}>"

    def get_id(self):
        """Return user id

        Returns:
            int: User id
        """
        return self.id
