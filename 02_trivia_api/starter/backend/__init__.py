import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app)

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def call_after_request(resp):
        resp.headers.add('Access-Control-Allow-Methods', 'GET, PUT, PATCH, POST, DELETE, OPTIONS')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        return resp
    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route('/categories')
    def get_all_categories():
        all_categories = Category.query.all()
        dict_categories = dict()

        for category in all_categories:
            dict_categories[f'{category.id}'] = f'{category.type}'

        return jsonify({
            'success': True,
            'categories': dict_categories
        })

    def paginate_questions(req, questions):
        page = req.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        formatted_questions = [question.format() for question in questions]
        page_questions = formatted_questions[start:end]
        return page_questions
    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 


  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
    @app.route('/questions')
    def get_questions():
        all_questions = Question.query.all()
        paginated_questions = paginate_questions(request, all_questions)
        if len(paginated_questions) == 0:
            abort(404)

        all_categories = Category.query.all()
        formatted_categories = [category.format() for category in all_categories]

        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(all_questions),
            'current_category': None,
            'categories': formatted_categories
        })

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<int: question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()
            all_questions = Question.query.all()
            paginated_questions = paginate_questions(request, all_questions)
        except Exception as e:
            abort(422)

        return jsonify({
            'success': True,
            'deleted': question_id,
            'questions': paginated_questions,
            'total_questions': len(all_questions)
        })

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        try:
            question = Question(
                category=body.get('category', None),
                difficulty=body.get('difficulty', None),
                question=body.get('question', None),
                answer=body.get('answer', None),
            )
            question.insert()
            all_questions = Question.query.all()
            paginated_questions = paginate_questions(request, all_questions)
        except Exception as e:
            abort(422)

        return jsonify({
            'success': True,
            'created': question.id,
            'questions': paginated_questions,
            'total_questions': len(all_questions)
        })

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
