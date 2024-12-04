########################################################
# Routes for Users blueprint
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
users = Blueprint('users', __name__)

#------------------------------------------------------------

# GET route for Persona2, retrieves student data under specfic advisor

@users.route('/users/<advisorid>', methods=['GET'])
def view_student_data (AdvisorId):

    query = f'''SELECT Username,
                       GPA, 
                       MajorID, 
                       AppCount, 
                       OfferCount, 
                       NUID
                        
                FROM Users 
                WHERE AdvisorId = {str(AdvisorId)}
    '''
    
    current_app.logger.info(f'GET /users/<advisorid> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /user/advisorid> Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response
    
# ------------------------------------------------------------

# GET Route for all Personas, retrieves student data under specifc NUID

@users.route('/users/<nuid>', methods=['GET'])
def view_student_data (NUID):

    query = f'''SELECT Username,
                       GPA, 
                       MajorID, 
                       AppCount, 
                       OfferCount, 
                       NUID
                        
                FROM Users 
                WHERE NUID = {str(NUID)}
    '''
    
    current_app.logger.info(f'GET /users/<nuid> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /user/<nuid> Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# ------------------------------------------------------------

# PUT Route for Persona 2, allows advisor to update Users GPA

@users.route('/users/<nuid>/update_gpa', methods=['PUT'])

def update_user_gpa(NUID):
    data = request.get_json()
    gpa = data['gpa']
    
    query = f'''
        UPDATE Users
        SET GPA = {str(gpa)}
        WHERE NUID = {str(NUID)}
    '''
    
    current_app.logger.info(f'PUT /users/<nuid>/update_gpa query={query}')
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    current_app.logger.info(f'PUT /users/<nuid>/update_gpa GPA updated for NUID = {NUID}')
    
    response = make_response(jsonify({'message': f'GPA for user {NUID} updated to {gpa}'}))
    response.status_code = 200
    return response

# ------------------------------------------------------------

# POST Route for Persona 4, allows system administrator insert new user

@users.route('/users/add_user', methods=['POST'])
def add_new_user():
    
    the_data = request.get_json()
    current_app.logger.info(the_data)


    username = the_data['username']
    major_id = the_data['major_id']
    gpa = the_data['gpa']
    advisor_id = the_data['advisor_id']
    app_count = the_data.get('app_count', 0)  
    offer_count = the_data.get('offer_count', 0)  
    previous_count = the_data.get('previous_count', 0)  
    nuid = the_data['nuid']

    query = f'''
        INSERT INTO Users (NUID, Username, MajorID, 
                            GPA, AdvisorId, AppCount, 
                            OfferCount, PreviousCount)
        VALUES ('{username}', '{major_id}', '{gpa}', '{advisor_id}',
                '{app_count}', '{offer_count}', '{previous_count}',
                '{nuid}')
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added User")
    response.status_code = 200
    return response

# ------------------------------------------------------------

# DELETE Route for Persona 4, allows system administrator to remove users

@users.route('/users/remove_user/<nuid>', methods=['DELETE'])
def remove_user(nuid):
    query = f'''
        DELETE FROM Users
        WHERE NUID = {nuid}
    '''
    
    current_app.logger.info(f'DELETE /users/remove_user/<nuid> query={query}')
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    current_app.logger.info(f'DELETE /users/remove_user/<nuid> User with NUID={nuid} deleted')
    
    response = make_response(jsonify({'message': f'User with NUID {nuid} successfully removed'}))
    response.status_code = 200
    return response

# ------------------------------------------------------------


