from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# create blueprint for landing
feed = Blueprint("feed", __name__)

# ---This blueprint is for the feed page of the site---

# GET (to populate user feed)
# Tables accessed: posts, users, graphs, bookmarked user
# Parameters:
# Sort by (default most recent)
# Filter by (multiple enumerations/modes for this)
# Search by (takes a postName)



# get all feed information needed to populate a user's feed for a particular user
@feed.route("/posts/<int:user_id>", methods=["GET"])
def get_feed(user_id):
    try:
        filter = request.args.get("filter_by")
        search = request.args.get("search")
        sort = request.args.get("sort_by")

        if sort and (sort not in ['newest', 'oldest', 'top', 'bottom']):
            return jsonify({"error": "sort parameter must be one of [newest, oldest, top, bottom]"})
        elif filter and (filter not in ['all', 'following', 'saved']):
            return jsonify({"error": "filter parameter must be one of [all, following, saved]"})

        current_app.logger.info(f"""Starting get_feed request for parameters:
                                 sort: {sort}, filter: {filter}, search: {search}""")
        cursor = db.get_db().cursor()

        current_app.logger.info("Starting query")
        # get details for a specific user
        # im ngl this took forever to do
        query = """SELECT 
                    p.PostID,
                    p.Title,
                    p.Description,
                    p.NumUpvotes,
                    p.NumDownvotes,
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
                    WHERE 1=1"""
        params = [user_id, user_id, user_id, user_id]

        # add paramter filters
        if filter:
            if filter == 'following': # TODO: following filter 
                query += """ AND 2=2"""
                params.append(user_id)
            elif filter == 'saved':
                query += " AND bu.UserID IS NOT NULL"

        if search:
            pass # TODO: search functionality                
        
        current_app.logger.debug(f'Executing query: {query}')
        cursor.execute(query, params)
        feed = cursor.fetchall()
        cursor.close()
        
        return jsonify(feed), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500