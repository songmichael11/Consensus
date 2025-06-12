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


# when a post is expanded, gets the questions and answers for a post
@expanded_post.route("/questions/<int:post_id>", methods=["GET"])
def get_questions(post_id):
    try:
        current_app.logger.info(f"""Starting get_questions request""")
        cursor = db.get_db().cursor()

        query = """SELECT q.IsHidden,
                        q.CreatedAt,
                        q.QuestionText,
                        a.AnswerText,
                        u.Name AS answerAuthor
                    FROM Questions q
                        LEFT JOIN Answers a 
                            ON q.QuestionID = a.AnswerID
                        LEFT JOIN Users u 
                            ON u.UserID = a.UserID
                    WHERE q.PostID = %s"""
        params = int(post_id)

        current_app.logger.debug(f'Executing query: {query}', params)
        cursor.execute(query, params)
        questions = cursor.fetchall()
        cursor.close()
        
        return jsonify(questions), 200

    except Error as e:
            current_app.logger.debug(f'Error: ' + str(e))
            return jsonify({"error": str(e)}), 500

# post request to ask a question for a specific post, from a specific user
@expanded_post.route("/question/post/<int:post_id>/user/<int:user_id>", methods=["POST"])
def post_question(post_id, user_id):
    try:
        current_app.logger.info(f"Starting post_question request for post {post_id} by user {user_id}")

        data = request.get_json()
        current_app.logger.info(data)

        cursor = db.get_db().cursor()

        # First check if the user has already asked more than 3 questions 
        check_query = """
            SELECT COUNT(q.QuestionID) 
            FROM Questions q
                JOIN UserQuestions uq
                    ON q.QuestionID = uq.QuestionID 
            WHERE uq.UserID = %s AND q.PostID = %s
        """
        cursor.execute(check_query, (user_id, post_id))
        exists = cursor.fetchone()['COUNT(q.QuestionID)'] > 3

        if exists: # If the user has already asked more than 3 questions, return a 210 status
            current_app.logger.info(f"User {user_id} has already asked more than 3 questions for {post_id}")
            return jsonify({"message": "User has already asked more than 3 quetions"}), 210

        # insert into questions table
        insert_query = """
            INSERT INTO Questions (QuestionText, PostID) 
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (data["QuestionText"], post_id))
        db.get_db().commit()
        new_question_id = cursor.lastrowid
        current_app.logger.info(f"QuestionID {new_question_id}")

        # insert into bridge table too
        insert_query = """
            INSERT INTO UserQuestions (QuestionID, UserID) 
            VALUES (%s, %s)
        """

        cursor.execute(insert_query, (new_question_id, user_id))
        db.get_db().commit()

        cursor.close()

        current_app.logger.info(f"Successfully added question for post {post_id} by user {user_id}")
        return jsonify({"message": "Successfully added question to post"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in post_question: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# post request to answer a question for a specific questionID from a specific user
@expanded_post.route("/answer/question/<int:question_id>/user/<int:user_id>", methods=["POST"])
def post_answer(question_id, user_id):
    try:
        current_app.logger.info(f"Starting post_question request for post {question_id} by user {user_id}")

        data = request.get_json()

        cursor = db.get_db().cursor()

        # First check if the question has already been answered
        check_query = """
            SELECT COUNT(AnswerID) 
            FROM Answers
            WHERE QuestionID = %s
        """
        cursor.execute(check_query, (question_id))
        exists = cursor.fetchone()['COUNT(AnswerID)'] > 0

        if exists: # If the question has already been answered, return 200
            current_app.logger.info(f"Question {question_id} has already been answered")
            return jsonify({"message": "Question has already been answered"}), 200

        # insert into answers table
        insert_query = """
            INSERT INTO Answers (AnswerText, QuestionID, UserID) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (data["AnswerText"], question_id, user_id))
        db.get_db().commit()
        new_question_id = cursor.lastrowid

        cursor.close()

        current_app.logger.info(f"Successfully added question for question {question_id} by user {user_id}")
        return jsonify({"message": "Successfully added question to post"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in post_answer: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# when a post is expanded, gets the expert opinions
@expanded_post.route("/exops/<int:post_id>", methods=["GET"])
def get_exops(post_id):
    try:
        current_app.logger.info(f"""Starting get_exops request""")
        cursor = db.get_db().cursor()

        query = """SELECT eo.BodyText,
                        eo.CreatedAt,
                        u.Name AS answerAuthor
                    FROM ExpertOpinions eo
                        LEFT JOIN ExpertOpUsers eou 
                            ON eo.ExpertOpID = eou.ExpertOpID
                        LEFT JOIN Users u 
                            ON u.UserID = eou.UserID
                    WHERE eo.PostID = %s"""
        params = int(post_id)

        current_app.logger.debug(f'Executing query: {query}', params)
        cursor.execute(query, params)
        exops = cursor.fetchall()
        cursor.close()
        
        return jsonify(exops), 200

    except Error as e:
            return jsonify({"error": str(e)}), 500
    
# post request to add expert feedback for a specific post, from a specific user
@expanded_post.route("/exops/post/<int:post_id>/user/<int:user_id>", methods=["POST"])
def post_exop(post_id, user_id):
    try:
        current_app.logger.info(f"Starting post_exop request for post {post_id} by user {user_id}")

        data = request.get_json()
        current_app.logger.info(data)

        cursor = db.get_db().cursor()

        # First check if the user has already added expert feedback to this post
        check_query = """
            SELECT COUNT(eo.ExpertOpID) 
            FROM ExpertOpinions eo
                JOIN ExpertOpUsers eou
                    ON eo.ExpertOpID = eou.ExpertOpID 
            WHERE uq.UserID = %s AND q.PostID = %s
        """
        cursor.execute(check_query, (user_id, post_id))
        exists = cursor.fetchone()['COUNT(eo.ExpertOpID)'] > 0

        if exists: # If the user has already added feedback, return a 210 status
            current_app.logger.info(f"User {user_id} has already added feedback {post_id}")
            return jsonify({"message": "User has already added feedback"}), 210

        # insert into questions table
        insert_query = """
            INSERT INTO ExpertOpinions (BodyText, PostID) 
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (data["BodyText"], post_id))
        db.get_db().commit()
        new_exop_id = cursor.lastrowid
        current_app.logger.info(f"ExpertOpID {new_exop_id}")

        # insert into bridge table too
        insert_query = """
            INSERT INTO ExpertOpUsers (ExpertOpID, UserID) 
            VALUES (%s, %s)
        """

        cursor.execute(insert_query, (new_exop_id, user_id))
        db.get_db().commit()

        cursor.close()

        current_app.logger.info(f"Successfully added exop for post {post_id} by user {user_id}")
        return jsonify({"message": "Successfully added question to post"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in post_exop: {str(e)}")
        return jsonify({"error": str(e)}), 500