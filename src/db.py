from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    User model
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    reviews = db.relationship("Reviews", cascade="delete")

    def __init__(self, **kwargs): 
        """
        Initializes a User object
        """

        self.username = kwargs.get("username", "") 
        self.password = kwargs.get("password","")
        
    def serialize(self):
        """
        Serializes a User object
        """

        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "reviews": [s.serialize() for s in self.reviews],
        }

    def simple_serialize(self):
        """
        Serialize a User object without the assignments, isntructors, students
        """

        return {
            "id": self.id,
            "username": self.username,
            "password": self.password
        }

class Reviews(db.Model):
    """
    Reviews model
    """

    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    dining_hall_id = db.Column(db.Integer, db.ForeignKey("dining_hall.id"), nullable=False)
    dining_hall =  db.relationship("User", cascade="delete")


    def __init__(self, **kwargs):
        """
        Initializes a review object
        """
        self.review = kwargs.get("review", "")
        self.rating = kwargs.get("rating", False)
        self.user_id = kwargs.get("user_id")
        self.dining_hall_id = kwargs.get("dining_hall_id")

    def serialize(self):
        """
        Serialize a review object
        """

        return {
            "id": self.id,
            "review": self.review,
            "rating": self.rating,
            "dining_hall": [c.simple_serialize() for c in self.instructors],
        }

class Dining_hall(db.Model):
    """
    Dining hall model
    """

    __tablename__ = "dining_hall"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    reviews = []


    def __init__(self, **kwargs):
        """
        Initializes a Dining hall object
        """

        self.name = kwargs.get("name", "")

    def serialize(self):
        """
        Serializes a Dining hall object
        """
        
        return {
            "id": self.id,
            "name": self.name,
            "reviews": self.reviews

        }

    def simple_serialize(self):
        """
        Serialize a Dining hall object without the review field
        """

        return {
            "id": self.id,
            "name": self.name
        }
