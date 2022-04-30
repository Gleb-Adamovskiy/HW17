from flask import current_app as app, request
from flask_restx import Api, Namespace, Resource
from appi.model import db
from appi import model, schema

api: Api = app.config['api']
movies_ns: Namespace = api.namespace('movies')

movie_schema = schema.Movie()
movies_schema = schema.Movie(many=True)

@movies_ns.route('/<int:movie_id>')
class MovieView(Resource):
    def get(self, movie_id):
        movie = db.session.query(model.Movie).filter(model.Movie.id == movie_id).first()
        if movie is None:
            return {}, 404
        return movies_schema.dump(movie), 200

@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies_query = db.session.query(model.Movie).all()
        args = request.args
        director_id = args.get('director_id')
        if director_id is not None:
            movies_query = movies_query.filter(model.Movie.director_id == director_id)
        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_query = movies_query.filter(model.Movie.genre_id == genre_id)
        movies = movies_query.all()
        return movies_schema.dump(movies), 200

