from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# create blueprint for landing
landing = Blueprint("landing", __name__)

# ---This blueprint is for the landing page of the site---

# get all users ids and their names by roleID, to populate landing page
@landing.route("/users/role/<int:role_id>", methods=["GET"])
def get_user_by_role(role_id):
    try:
        current_app.logger.info('Starting get_user_by_role request for role %s', role_id)
        cursor = db.get_db().cursor()

        # get details for a specific user
        current_app.logger.info('Executing queries')
        cursor.execute("""SELECT 
                       u.Name,
                       u.UserID
                        FROM Users u
                       JOIN RolesUsers ru
                            ON u.UserID = ru.UserID
                       WHERE RoleID = %s""", (role_id,))
        user = cursor.fetchall()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        cursor.close()
        return jsonify(user), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# get all user information for a session state, given a user ID
@landing.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        current_app.logger.info('Starting get_user request for user %s', user_id)
        cursor = db.get_db().cursor()

        # get details for a specific user
        current_app.logger.info('Executing queries')
        cursor.execute("SELECT * FROM Users WHERE UserID = %s", (user_id,))
        user = cursor.fetchone()
        
        cursor.execute("""SELECT RoleType FROM Roles r
                       JOIN RolesUsers ru 
                        ON r.RoleID = ru.RoleID
                       WHERE ru.UserID = %s""", user_id)
        roles = cursor.fetchall()

        user["Roles"] = [role["RoleType"] for role in roles]
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        cursor.close()
        return jsonify(user), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500