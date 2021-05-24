"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from re import L
from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import (
    db,
    session,
    T,
    cache,
    auth,
    logger,
    authenticated,
    unauthenticated,
    flash,
    Field,
)
from py4web.utils.url_signer import URLSigner
from .models import get_user_email, get_user
from py4web.utils.form import Form, FormStyleBulma
from pydal.validators import *
from .models import CATEGORY_KINDS

url_signer = URLSigner(session)


@action("index")
@action.uses(db, auth.user, url_signer, "index.html")
def index():
    return dict(
        load_posts_url=URL("load_posts", signer=url_signer),
        add_post_url=URL("add_post", signer=url_signer),
        delete_post_url=URL("delete_post", signer=url_signer),
        get_rating_url=URL("get_rating", signer=url_signer),
        set_rating_url=URL("set_rating", signer=url_signer),
        get_likers_url=URL("get_likers", signer=url_signer),
        url_signer=url_signer,
    )


@action("post/<post_id:int>", method=["GET", "POST"])
@action.uses(db, auth.user, url_signer, "post.html")
def post(post_id=None):
    assert post_id is not None
    p = db.post[post_id]
    if p is None:
        # Nothing found to be edited!
        redirect(URL("index"))
    post = db(db.post.id == post_id).select().first()
    # print(post)
    return dict(
        post=post,
        add_answer_url=URL("add_answer", signer=url_signer),
        load_answers_url=URL("load_answers", signer=url_signer),
    )


@action("add_post", method=["GET", "POST"])
@action.uses(db, session, auth.user, "add_post.html")
def add_post():
    # Insert form: no record= in it.
    form = Form(db.post, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We simply redirect; the insertion already happened.
        redirect(URL("index"))
    # Either this is a GET request, or this is a POST but not accepted = with errors.
    return dict(form=form)


@action("add_answer", method="POST")
@action.uses(url_signer.verify(), db, auth.user)
def add_answer():
    id = db.answer.insert(
        answer=request.json.get("answer"), post_id=request.json.get("post_id"),
    )
    user_email = db.answer[id].answer_user_email
    time_answered = db.answer[id].time_answered
    name = db.answer[id].name

    return dict(id=id, user_email=user_email, time_answered=time_answered, name=name)


@action("load_answers")
@action.uses(url_signer.verify(), db)
def load_answers():
    rows = db(db.answer).select().as_list()
    r = db(db.auth_user.email == get_user_email()).select().first()
    current_user = r.email if r is not None else "Unknown"
    return dict(rows=rows, current_user=current_user)


@action("load_posts")
@action.uses(url_signer.verify(), db)
def load_posts():
    rows = db(db.post).select().as_list()
    # print(rows)
    r = db(db.auth_user.email == get_user_email()).select().first()
    current_user = r.email if r is not None else "Unknown"
    for i in rows:
        i["category"] = CATEGORY_KINDS.get(i["category"])
    return dict(rows=rows, current_user=current_user)


# @action("add_post", method="POST")
# @action.uses(url_signer.verify(), db, auth.user)
# def add_post():
#     id = db.post.insert(content=request.json.get("content",))
#     name = db.post[id].name
#     user_email = db.post[id].user_email
#     return dict(id=id, name=name, user_email=user_email)


@action("delete_post")
@action.uses(url_signer.verify(), db, auth.user)
def delete_post():
    id = request.params.get("id")
    # id = request.vars.get("id") #this is another way of doing above
    assert id is not None
    db(db.post.id == id).delete()
    return "post deleted"


@action("get_rating")
@action.uses(url_signer.verify(), db, auth.user)
def get_rating():
    """Returns the rating for a user and an image."""
    post_id = request.params.get("post_id")
    row = (
        db((db.rating.post == post_id) & (db.rating.rater == get_user()))
        .select()
        .first()
    )
    rating = row.rating if row is not None else 0
    post = db(db.post.id == post_id).select().as_list()
    temp = post[0]
    return dict(rating=rating, likers=temp["final"])


@action("set_rating", method="POST")
@action.uses(url_signer.verify(), db, auth.user)
def set_rating():
    """Sets the rating for an image."""
    post_id = request.json.get("post_id")
    rating = request.json.get("rating")
    old_rating = db(db.rating.rater == get_user()).select().first()
    assert post_id is not None and rating is not None
    db.rating.update_or_insert(
        ((db.rating.post == post_id) & (db.rating.rater == get_user())),
        post=post_id,
        rater=get_user(),
        rating=rating,
    )
    post = db.post[post_id]
    if rating == 0:
        if old_rating.rating == 1:
            db(db.post.id == post_id).update(final=post.final - 1)
        elif old_rating.rating == -1:
            db(db.post.id == post_id).update(final=post.final + 1)
    elif rating == 1:
        if old_rating is None:
            db(db.post.id == post_id).update(final=post.final + rating)
        else:
            if old_rating.rating == 0:
                db(db.post.id == post_id).update(final=post.final + 1)
            elif old_rating.rating == -1:
                db(db.post.id == post_id).update(final=post.final + 2)
    elif rating == -1:
        if old_rating is None:
            db(db.post.id == post_id).update(final=post.final + rating)
        else:
            if old_rating.rating == 0:
                db(db.post.id == post_id).update(final=post.final - 1)
            if old_rating.rating == 1:
                db(db.post.id == post_id).update(final=post.final - 2)

    return "rating set"  # Just to have some confirmation in the Network tab.


@action("get_likers")
@action.uses(url_signer.verify(), db, auth.user)
def get_likers():
    post_id = request.params.get("post_id")

    post = db(db.post.id == post_id).select().as_list()
    temp = post[0]
    return dict(likers=temp["final"])
