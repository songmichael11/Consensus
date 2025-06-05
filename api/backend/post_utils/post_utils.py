from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

# Create a Blueprint for NGO routes
post_utils = Blueprint("post_utils", __name__)

# PUT request to add an upvote to a post
# Handles the case where user has already upvoted by returning a 200 status
# Example: /post_utils/post/193/upvote/456
@post_utils.route("/post/<int:post_id>/upvote/<int:user_id>", methods=["PUT"])
def put_upvote(post_id, user_id):
    try:
        current_app.logger.info(f"Starting put_upvote request for post {post_id} by user {user_id}")
        cursor = db.get_db().cursor()

        # First check if the upvote already exists
        check_query = """
            SELECT COUNT(*) 
            FROM UpvotesUsers 
            WHERE UserID = %s AND PostID = %s
        """
        cursor.execute(check_query, (user_id, post_id))
        exists = cursor.fetchone()['COUNT(*)'] > 0

        if exists: # If the user has already upvoted the post, return a 200 status
            current_app.logger.info(f"User {user_id} has already upvoted post {post_id}")
            return jsonify({"message": "User has already upvoted this post"}), 200

        # If no existing upvote, add the upvote
        insert_query = """
            INSERT INTO UpvotesUsers (UserID, PostID) 
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (user_id, post_id))

        # Update the post's upvote count
        update_query = """
            UPDATE Posts 
            SET NumUpvotes = (
                SELECT COUNT(*) 
                FROM UpvotesUsers 
                WHERE PostID = %s
            )
            WHERE PostID = %s
        """
        cursor.execute(update_query, (post_id, post_id))
        
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Successfully added upvote for post {post_id} by user {user_id}")
        return jsonify({"message": "Successfully upvoted post"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in put_upvote: {str(e)}")
        return jsonify({"error": str(e)}), 500

# DELETE request to remove an upvote from a post
# Example: /post_utils/post/193/upvote/456
@post_utils.route("/post/<int:post_id>/upvote/<int:user_id>", methods=["DELETE"])
def delete_upvote(post_id, user_id):
    try:
        current_app.logger.info(f"Starting delete_upvote request for post {post_id} by user {user_id}")
        cursor = db.get_db().cursor()

        # Delete the upvote
        delete_query = """
            DELETE FROM UpvotesUsers 
            WHERE UserID = %s AND PostID = %s
        """
        cursor.execute(delete_query, (user_id, post_id))
        
        # Check if any rows were actually deleted
        if cursor.rowcount == 0:
            current_app.logger.info(f"No upvote found to delete for post {post_id} by user {user_id}")
            return jsonify({"message": "No upvote found to delete"}), 404

        # Update the post's upvote count
        update_query = """
            UPDATE Posts 
            SET NumUpvotes = (
                SELECT COUNT(*) 
                FROM UpvotesUsers 
                WHERE PostID = %s
            )
            WHERE PostID = %s
        """
        cursor.execute(update_query, (post_id, post_id))
        
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Successfully removed upvote for post {post_id} by user {user_id}")
        return jsonify({"message": "Successfully removed upvote"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in delete_upvote: {str(e)}")
        return jsonify({"error": str(e)}), 500
