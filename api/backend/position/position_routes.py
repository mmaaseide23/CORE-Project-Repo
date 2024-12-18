########################################################
# Routes for Position blueprint
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint object for position-related routes
position = Blueprint('position', __name__)


# Update position stats for a specific PositionID
@position.route('/posstats/<int:PositionID>', methods=['PUT'])
def update_posstats(PositionID):
    data = request.json
    query = '''
        UPDATE PosStats
        SET YieldRate = %s,
            AvgAppAmount = %s,
            AvgInterview = %s,
            AvgGpa = %s,
            AvgLearning = %s,
            AvgEnvironment = %s,
            AvgInterviewTime = %s
        WHERE PositionID = %s
    '''
    params = (
        data['YieldRate'], data['AvgAppAmount'], data['AvgInterview'],
        data['AvgGpa'], data['AvgLearning'], data['AvgEnvironment'],
        data['AvgInterviewTime'], PositionID
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    return jsonify({'message': f'Position stats for PositionID {PositionID} updated successfully.'}), 200



\
# Gets position review informaiton along with reviewers
@position.route('/PositionReview', methods=['GET'])
def get_posreviews():
    query = '''
            SELECT *
            FROM PositionReview pr
            LEFT JOIN PositionReviewers prr ON pr.PosReviewID = prr.PosReviewID
            LEFT JOIN Users u ON prr.NUID = u.NUID;
        '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    reviews = cursor.fetchall()
    return jsonify(reviews), 200




# BREAK INTO MULTIPLE ROUTES - first route gets PositionID from PositionName, 
# second connects PositionID to PositionStats
# third connects PositionID to PositionReviews
# beneficial as it allows search by company to use same routes
@position.route('/positions/info', methods=['GET'])
def get_posinfo():
    query = '''
            SELECT ps.YieldRate, ps.AvgAppAmount, ps.AvgInterview,
                ps.AvgEnvironment,  ps.AvgGpa, ps.AvgLearning,

                pr.Description AS PositionReview, pr.ResponseDate,
                pr.Offer, pr.ApplicationRating, pr.EnvironmentRating, pr.EducationRating,
                pr.EnjoymentRating, pr.Applied, pr.AppliedDate,

                pt.PositionID, pt.PositionName, pt.Description AS PositionDescription,

                u.Username

            FROM PositionTable pt
            LEFT JOIN PosStats ps ON pt.PositionID = ps.PositionID
            LEFT JOIN PositionReview pr ON pt.PositionID = pr.PositionID
            LEFT JOIN PositionReviewers prr ON pr.PosReviewID = prr.PosReviewID
            LEFT JOIN Users u ON prr.NUID = u.NUID;
        '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    reviews = cursor.fetchall()
    return jsonify(reviews), 200




# Creating new position review
@position.route('/PositionReview/post', methods=['POST'])
def add_review():
    data = request.json  # Expecting JSON input
    query = '''
        INSERT INTO PositionReview (
            Description, Offer, ApplicationRating, EnvironmentRating,
            EducationRating, EnjoymentRating, Applied, AppliedDate,
            ResponseDate, PositionID
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (
        data['Description'], data['Offer'], data['ApplicationRating'],
        data['EnvironmentRating'], data['EducationRating'], 
        data['EnjoymentRating'], data['Applied'], data['AppliedDate'],
        data['ResponseDate'], data['PositionID']
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    return jsonify({'message': 'Review added successfully'}), 200





# Deleting reviews
@position.route('/PositionReview/<int:PosReviewID>', methods=['DELETE'])
def delete_review(PosReviewID):
    query = '''
        DELETE FROM PositionReview
        WHERE PosReviewID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (PosReviewID,))
    db.get_db().commit()
    return jsonify({'message': f'Review with ID {PosReviewID} deleted successfully'}), 200





# Getting position by major
@position.route('/positions/related_majors/<int:major_id>', methods=['GET'])
def get_positions_by_related_majors(major_id):
    query = '''
        SELECT DISTINCT pt.PositionID, pt.PositionName, pt.Description
        FROM Majors m
         JOIN Users u ON m.MajorID = u.MajorID
         JOIN PositionReview pr ON pr.PositionID = u.PositionId
         JOIN PositionTable pt ON pt.PositionID = pr.PositionID
        WHERE  m.MajorID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (major_id,))
    positions = cursor.fetchall()

    return jsonify(positions), 200
