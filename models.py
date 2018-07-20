from __init__ import db

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    budget = db.Column(db.Integer)
    revenue = db.Column(db.Integer)
    release_date = db.Column(db.String)
    runtime = db.Column(db.Integer)
    imdb_rating = db.Column(db.String)
    genres = db.relationship('Genre', secondary='movie_genres')
    director = db.relationship('Director', back_populates=('movies'))
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))

class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    movies = db.relationship(Movie, back_populates=('director'))

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    movies = db.relationship(Movie, secondary='movie_genres')

class MovieGenre(db.Model):
    __tablename__ = "movie_genres"
    #id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'),primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'),primary_key=True)

db.create_all()
