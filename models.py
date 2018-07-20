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
    def to_dict(self):
        movie = {'id': self.id, 'title': self.title, 'budget': self.budget, 'revenue': self.revenue, 'release_date': self.release_date, 'runtime': self.runtime, 'imdb_rating': self.imdb_rating,
        'genres': [genre.to_dict()['name'] for genre in self.genres], 'director': self.director.to_dict()['name']}
        return movie

class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    movies = db.relationship(Movie, back_populates=('director'))
    def to_dict(self):
        director = {'id': self.id, 'name': self.name, 'movies': [movie.title for movie in self.movies]}
        return director

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    movies = db.relationship(Movie, secondary='movie_genres')
    def to_dict(self):
        genre = {'id': self.id, 'name': self.name, 'movies': [movie.title for movie in self.movies]}
        return genre

class MovieGenre(db.Model):
    __tablename__ = "movie_genres"
    #id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'),primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'),primary_key=True)

db.create_all()
