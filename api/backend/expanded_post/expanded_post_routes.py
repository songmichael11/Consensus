from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# create blueprint for landing
expanded_post = Blueprint("expanded_post", __name__)

# ---This blueprint is for the Expanded Post page of the site---

# get a post's information by its postID
@expanded_post.route("/post/<int:post_id>/<int:user_id>", methods=["GET"])
def get_one_post(post_id, user_id):
    try:
        current_app.logger.info("Starting get_one_post request")
        cursor = db.get_db().cursor()

        query = """SELECT 
                            p.PostID,
                            p.Title,
                            p.Description,
                            p.NumUpvotes - p.NumDownvotes AS karma,
                            p.NumEndorsements,
                            p.IsHidden,
                            author.Name AS author,
                            CASE WHEN bu.UserID IS NOT NULL 
                                THEN 'Saved' ELSE 'Not Saved' END AS bookmarked,
                            CASE WHEN uu.UserID IS NOT NULL 
                                THEN 'Upvoted' ELSE 'Not Upvoted' END AS upvoted,
                            CASE WHEN du.UserID IS NOT NULL 
                                THEN 'Downvoted' ELSE 'Not Downvoted' END AS downvoted,
                            CASE WHEN eu.UserID IS NOT NULL 
                                THEN 'Endorsed' ELSE 'Not Endorsed' END AS endorsed,
                            p.GraphID
                            FROM Posts p
                            JOIN Users author 
                                ON p.UserID = author.UserID
                            LEFT JOIN BookmarkedUsers bu 
                                ON bu.PostID = p.PostID AND bu.UserID = %s
                            LEFT JOIN UpvotesUsers uu 
                                ON uu.PostID = p.PostID AND uu.UserID = %s
                            LEFT JOIN DownvotesUsers du 
                                ON du.PostID = p.PostID AND du.UserID = %s
                            LEFT JOIN EndorsementsUsers eu 
                                ON eu.PostID = p.PostID AND eu.UserID = %s
                            LEFT JOIN FollowingFollowees ff 
                                ON ff.FolloweeID = p.UserID AND ff.FollowerID = %s
                            WHERE p.PostID = %s"""
        params = [user_id, user_id, user_id, user_id, user_id, post_id]

        current_app.logger.debug(f'Executing query: {query}')
        cursor.execute(query, params)
        feed = cursor.fetchone()
        cursor.close()
        
        return jsonify(feed), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# 