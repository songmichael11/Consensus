from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# create blueprint for feed
feed = Blueprint("feed", __name__)

# ---This blueprint is for the feed page of the site---