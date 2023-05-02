import json
from db import db
from flask import Flask, request
from db import User, Reviews, Dining_hall

app = Flask(__name__)
db_filename = "food.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


@app.route("/reviews/")
def get_all_reviews():
    reviews = [review.serialize() for review in Reviews.query.all()] 
    return success_response({"Reviews": reviews})  
    

@app.route("/reviews/<int:dining_hall_id>/")
def get_reviews_by_dh(dining_hall_id):
    """
    Endpoint for getting reviews by dining hall
    """
    reviews = [reviews.serialize() for review in Reviews.query.filter_by(id=dining_hall_id).first()] #test
    if reviews is None:
        return failure_response("Dining hall not found", 400) #what if its correct dining hall but there's no reviews?
    return success_response(reviews.serialize())                                                                                                         


@app.route("/user/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a new review
    """
    body = json.loads(request.data)
    new_user= User(
        username= body.get("username"),
        password = body.get("password")
    )
    if not body.get("username"):
        return failure_response("Sender not found",400)
    
    if not body.get("password"):
        return failure_response("Sender not found",400)

    db.session.add(new_user) 
    db.session.commit() 
    return success_response(new_user.serialize(), 201)


@app.route("/api/user/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by id
    """
    user = User.query.filter_by(id=user_id).first() 
    if user is None:
        return failure_response("User not found!") 
    return success_response(user.serialize())


@app.route("/api/user/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a task by id
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Task not found!")
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize())



@app.route("/api/courses/<int:course_id>/assignments/", methods=["POST"])
def create_assignments(course_id):
    """
    Endpoint for creating a subtask
    for a task by id
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Task not found!")
    body = json.loads(request.data)
    new_assignment = Assignments(
        title = body.get("title"),
        due_date = body.get("due_date"),
        course_id = course_id
    )
    if not body.get("title"):
        return failure_response("Sender not found",400)
    
    if not body.get("due_date"):
        return failure_response("Sender not found",400)
    db.session.add(new_assignment)
    db.session.commit()
    result = new_assignment.serialize()
    result["course"] = course.simple_serialize()
    return success_response(result,201)


'''
@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a subtask
    for a task by id
    """
    body = json.loads(request.data)
    new_user = User(
        name = body.get("name"),
        netid = body.get("netid"),
    )
    if not body.get("name"):
        return failure_response("Sender not found",400)
    
    if not body.get("netid"):
        return failure_response("Sender not found",400)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(),201)
'''

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for creating a subtask
    for a task by id
    """

    user = User.query.filter_by(id=user_id).first() 
    if user is None:
        return failure_response("Course not found!") 
    return success_response(user.serialize())

@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def assign_user(course_id):
    """
    Endpoint for assigning a category
    to a task by id
    """
    
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Task not found!")
    body = json.loads(request.data)
    user_id = body.get("user_id")
    type = body.get("type")


    user = User.query.filter_by(id = user_id).first()

    if type == "student":
        course.students.append(user)
    if type == "instructor":
        course.instructors.append(user)
    db.session.commit()
    return success_response(course.serialize(),201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
