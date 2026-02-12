import os
import time
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required
)
from sqlalchemy.exc import IntegrityError

DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASS = os.getenv('DB_PASS', 'apppass')
DB_NAME = os.getenv('DB_NAME', 'CineVault')
JWT_SECRET = os.getenv('JWT_SECRET', 'change-me-to-a-secure-random-value')

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = JWT_SECRET
    app.config['JSON_SORT_KEYS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    register_routes(app)
    return app

# Extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

# Association tables
movie_genre = db.Table('movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

movie_actor = db.Table('movie_actor',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True)
)

movie_director = db.Table('movie_director',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('director_id', db.Integer, db.ForeignKey('director.id'), primary_key=True)
)

movie_language = db.Table('movie_language',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'), primary_key=True)
)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    duration = db.Column(db.Integer)
    year = db.Column(db.Integer)
    poster = db.Column(db.Text)
    description = db.Column(db.Text)

    genres = db.relationship('Genre', secondary=movie_genre, backref='movies')
    actors = db.relationship('Actor', secondary=movie_actor, backref='movies')
    directors = db.relationship('Director', secondary=movie_director, backref='movies')
    languages = db.relationship('Language', secondary=movie_language, backref='movies')

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

# Utilities
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        instance = session.query(model).filter_by(**kwargs).first()
    return instance

def register_routes(app):
    @app.route('/healthz')
    def health():
        return jsonify({'status':'ok'})

    # Auth
    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error':'username and password required'}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({'error':'username exists'}), 409
        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        return jsonify({'status':'created'}), 201

    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error':'username and password required'}), 400
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({'error':'invalid credentials'}), 401
        token = create_access_token(identity=user.id)
        return jsonify({'access_token': token}), 200

    # Movies with pagination and search
    @app.route('/api/movies', methods=['GET'])
    def list_movies():
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        q = request.args.get('q', None)

        query = Movie.query
        if q:
            like = f"%{q}%"
            query = query.filter(Movie.title.ilike(like))
        pagination = query.order_by(Movie.title).paginate(page=page, per_page=per_page, error_out=False)
        items = []
        for m in pagination.items:
            items.append({
                'id': m.id,
                'title': m.title,
                'duration': m.duration,
                'year': m.year,
                'poster': m.poster,
                'description': m.description,
                'genres': [g.name for g in m.genres],
                'actors': [f"{a.first_name} {a.last_name}".strip() for a in m.actors],
                'directors': [f"{d.first_name} {d.last_name}".strip() for d in m.directors],
                'languages': [l.name for l in m.languages]
            })
        return jsonify({
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages,
            'items': items
        })

    @app.route('/api/movies/<int:movie_id>', methods=['GET'])
    def get_movie(movie_id):
        m = Movie.query.get(movie_id)
        if not m:
            return jsonify({'error':'not found'}), 404
        return jsonify({
            'id': m.id,
            'title': m.title,
            'duration': m.duration,
            'year': m.year,
            'poster': m.poster,
            'description': m.description,
            'genres': [g.name for g in m.genres],
            'actors': [f"{a.first_name} {a.last_name}".strip() for a in m.actors],
            'directors': [f"{d.first_name} {d.last_name}".strip() for d in m.directors],
            'languages': [l.name for l in m.languages]
        })

    # Protected endpoints
    @app.route('/api/movies', methods=['POST'])
    @jwt_required()
    def create_movie():
        data = request.get_json() or {}
        title = data.get('title')
        if not title:
            return jsonify({'error':'title required'}), 400
        if Movie.query.filter_by(title=title).first():
            return jsonify({'error':'movie already exists'}), 409
        duration = data.get('duration')
        year = data.get('year')
        poster = data.get('poster')
        description = data.get('description')
        genres = data.get('genres') or []
        actors = data.get('actors') or []
        directors = data.get('directors') or []
        languages = data.get('languages') or []

        m = Movie(title=title, duration=duration, year=year, poster=poster, description=description)
        db.session.add(m)
        db.session.commit()

        for g in genres:
            gg = get_or_create(db.session, Genre, name=g.strip())
            m.genres.append(gg)
        for a in actors:
            parts = a.strip().split(' ',1)
            fn = parts[0]; ln = parts[1] if len(parts)>1 else ''
            aa = get_or_create(db.session, Actor, first_name=fn, last_name=ln)
            m.actors.append(aa)
        for d in directors:
            parts = d.strip().split(' ',1)
            fn = parts[0]; ln = parts[1] if len(parts)>1 else ''
            dd = get_or_create(db.session, Director, first_name=fn, last_name=ln)
            m.directors.append(dd)
        for l in languages:
            ll = get_or_create(db.session, Language, name=l.strip())
            m.languages.append(ll)

        db.session.commit()
        return jsonify({'status':'created','id': m.id}), 201

    @app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
    @jwt_required()
    def delete_movie(movie_id):
        m = Movie.query.get(movie_id)
        if not m:
            return jsonify({'error':'not found'}), 404
        db.session.delete(m)
        db.session.commit()
        return jsonify({'status':'deleted'})

    # Protected seeder
    @app.route('/admin/seed', methods=['POST'])
    @jwt_required()
    def seed():
        if Movie.query.count() > 0:
            return jsonify({'status':'already seeded'})
        samples = [
            dict(title='Inception', duration=148, year=2010, description='A mind-bending thriller.'),
            dict(title='The Shawshank Redemption', duration=142, year=1994, description='Two imprisoned men bond.'),
            dict(title='La La Land', duration=128, year=2016, description='A jazz pianist falls for an aspiring actress.')
        ]
        for s in samples:
            m = Movie(title=s['title'], duration=s.get('duration'), year=s.get('year'), description=s.get('description'))
            db.session.add(m)
        db.session.commit()
        return jsonify({'status':'seeded'})

# Wait for DB and create tables
def wait_for_db(app):
    with app.app_context():
        tries = 0
        while tries < 30:
            try:
                db.create_all()
                if Genre.query.count() == 0:
                    db.session.add(Genre(name='Drama'))
                    db.session.add(Language(name='English'))
                    db.session.commit()
                return
            except Exception as e:
                tries += 1
                print('Waiting for DB... attempt', tries, 'error:', e)
                time.sleep(2)
        raise RuntimeError('Database not available')

app = create_app()
if __name__ == '__main__':
    wait_for_db(app)
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
