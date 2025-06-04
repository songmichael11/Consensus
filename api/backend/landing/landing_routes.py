from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# create blueprint for landing
landing = Blueprint("landing", __name__)

# ---This blueprint is for the landing page of the site---

# get all user information for a session state, given a user ID
@landing.route("/users/<int:UserID>", methods=["GET"])
def get_user(UserID):
    try:
        cursor = db.get_db().cursor()

        # get details for a specific user
        cursor.execute("SELECT * FROM Users WHERE UserID = %s", (UserID,))
        user = cursor.fetchone()
        
        cursor.execute("""SELECT RoleType FROM Roles r
                       JOIN RolesUsers ru 
                        ON r.RoleID = ru.RoleID
                       WHERE ru.UserID = %s""", UserID)
        roles = cursor.fetchall()

        user["Roles"] = [role["RoleType"] for role in roles]

        if not user:
            return jsonify({"error": "User not found"}), 404
        
        cursor.close()
        return jsonify(user), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500