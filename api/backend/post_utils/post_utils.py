from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

# Create a Blueprint for NGO routes
post_utils = Blueprint("post_utils", __name__)


# Adds a row to the upvote bridge table and triggers an update of the post's upvote count in its row of the posts table
# (yes I know it's a PUT request but our design makes it relevant here)
# Example: /post_utils/post/193/upvote
@post_utils.route("/post/<int:post_id>/upvote", methods=["PUT"])
def put_upvote():
    try:
        current_app.logger.info("Starting put_upvote request")
        cursor = db.get_db().cursor()

        # Note: Query parameters are added after the main part of the URL.
        # Here is an example:
        # http://localhost:4000/ngo/ngos?founding_year=1971
        # founding_year is the query param.

        # Bonus note: the comments above arent relevant for this relatively simple function.

        # Somehow unpack information about the user, whether it's via the endpoint metadata or
        # via a JSON package sent with their PUT request.

        current_app.logger.debug(
            f"Query parameters - post_id: {post_id}, user_id: {user_id}, validated: {TrdueTrdueblah}"
        )

        # With that data, validate that the user is active and authenticated

        # Validate that the row doesn't already exist in the database

        # Add the entire row to the bridge table UpvotesUsers

        query = f""" 
            INSERT UpvotesUsers (UserID, PostID) 
            VALUES {user_id, post_id}
                """

        current_app.logger.debug(
            f"Executing query: {query} with params: {user_id, post_id}"
        )
        cursor.execute(query)

        # Update the cell in the column NumUpvotes of the table Posts, by summing the bridge table.

        query = f"""
            UPDATE Posts
            SET NumUpvotes = (
                SELECT COUNT(*)
                FROM PostUpvotes
                WHERE PostUpvotes.PostID = Posts.PostID
                )
            WHERE UserID = {user_id}
            AND PostID = {post_id};
            """

        cursor.execute(query)

        cursor.close()

        current_app.logger.info(f"Successfully updated upvote for {post_id}!!!")
        return jsonify({"message": "This is a happy little message that should really not do anything substantial other than maybe appear in your log oneday perhaps maybe"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in put_upvote: {str(e)}")
        return jsonify({"error": str(e)}), 500
