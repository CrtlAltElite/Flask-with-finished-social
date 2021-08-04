from app import db
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email =  db.Column(db.String(200), unique=True, index=True)
    password = db.Column(db.String(200))
    icon = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def followed_posts(self):
        from app.blueprints.social.models import Post

        # get posts for all users I'm following
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id==self.id)
        # get all owns posts
        self_posts = Post.query.filter_by(user_id=self.id)
        # add them together and sort them by date descending
        all_posts = followed.union(self_posts).order_by(Post.date_created.desc())
        return all_posts
    
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()


    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.icon = data['icon']
        self.password = self.hash_password(data['password'])
        self.save()

    def get_icon_url(self):
        return f"https://avatars.dicebear.com/api/bottts/{self.icon}.svg"

    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password,login_password)

    def save(self):
        db.session.add(self) #adds the user to the db session
        db.session.commit() #saves the changes into the db



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # Select * from user WHERE id=id