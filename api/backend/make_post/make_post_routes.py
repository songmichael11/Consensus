from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# create blueprint for landing
make_post = Blueprint("make_post", __name__)

# ---This blueprint is for the Make Post page of the site---

# route for make post button
@make_post.route("/post/<int:user_id>", methods=["POST"])
def post_post(user_id):
    try:
        current_app.logger.info(f"Starting make_post request for post by user {user_id}")

        data = request.get_json()
        current_app.logger.info(data)

        cursor = db.get_db().cursor()

        # insert into questions table
        insert_query = """
            INSERT INTO Posts (Title, Description, UserID, GraphID) 
            VALUES (%s, %s, %s, %s)
        """
        params = [data["Title"], data["Description"], user_id, data["GraphID"]]
        cursor.execute(insert_query, params)
        db.get_db().commit()
        new_post_id = cursor.lastrowid
        current_app.logger.info(f"PostID {new_post_id}")

        cursor.close()

        current_app.logger.info(f"Successfully added post for post {new_post_id} by user {user_id}")
        return jsonify({"message": "Successfully added created post"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in post_question: {str(e)}")
        return jsonify({"error": str(e)}), 500