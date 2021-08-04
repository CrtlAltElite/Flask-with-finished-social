from app import db
from datetime import datetime as dt


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    sprite = db.Column(db.Text)
    my_trait =  db.Column(db.String(50))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    pokemon_id = db.Column(db.Integer(), db.ForeignKey("pokemon.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("person.id"))

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))

#GEt all the info for posts on a pokemon with the id of 3

# SELECT pokemon.name, pokemon.sprite, pokemon.my_trait, comment.body, person.name
# FROM pokemon
# JOIN comment ON comment.pokemon_id = pokemon.id
# JOIN person ON person.id = comment.user_id
# WHERE pokemon.id = 3



# Pokemon.query.join(Comment).join(Person).with_entities(Pokemon.name, Pokemon.sprite, Pokemon.my_trait, Comment.body, Person.name).filter_by(id=3).all()












                                                                                                                                # 2 is the id of the pokemon we are looking for the comments from
# all=Pokemon.query.join(Comment).join(Person).with_entities(Pokemon.my_trait, Pokemon.sprite, Comment.body, Person.name).filter_by(id=2).all()