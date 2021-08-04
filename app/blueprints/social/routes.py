from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .import bp as social
from app.blueprints.auth.models import User
from .models import Post

@social.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        body_from_form = request.form.get('body')
        try:
            new_post = Post(body=body_from_form, user_id=current_user.id)
            new_post.save()
            flash("Thanks for posting ", "success")
        except:
            flash("Error Creating Post.  Try again!", "danger")
    posts = current_user.followed_posts()
    return render_template('index.html.j2',posts=posts)

@social.route('/post/my_posts', methods=['GET'])
@login_required
def my_posts():
    return render_template('my_posts.html.j2', posts=current_user.posts)

@social.route('/post/<int:id>', methods=['GET'])
@login_required
def get_post(id):
    post = Post.query.get(id)
    return render_template('single_post.html', post=post, view_all=True)

@social.route('/edit_post/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        if current_user.id==post.user_id:
            post.edit(request.form.get("body"))
            flash("Your post has been edited", "success")
        else:
            flash("Get Out Of here Fool!","danger")
    return render_template('edit_post.html',post=post)

@social.route('/show_users', methods=['GET'])
@login_required
def show_users():
    users=User.query.all()
    return render_template('show_users.html.j2', users=users)

@social.route('/follow/<int:id>', methods=['GET'])
@login_required
def follow(id):
    user_to_follow=User.query.get(id)
    current_user.follow(user_to_follow)
    flash(f"You are now following {user_to_follow.first_name} {user_to_follow.last_name}","success")
    return redirect(url_for('social.show_users'))

@social.route('/unfollow/<int:id>', methods=['GET'])
@login_required
def unfollow(id):
    user_to_unfollow=User.query.get(id)
    current_user.unfollow(user_to_unfollow)
    flash(f"You are no longer following {user_to_unfollow.first_name} {user_to_unfollow.last_name}","warning")
    return redirect(url_for('social.show_users'))

@social.route('/delete_post/<int:id>', methods=['GET'])
@login_required
def delete_post(id):
    post_to_delete = Post.query.get(id)
    if current_user.id==post_to_delete.user_id:
        post_to_delete.delete()
        flash("Your post has been deleted", "info")
    else:
        flash("Get outta here you hacker!!!!","danger")
    return redirect(url_for('social.index'))