"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth, T
from pydal.validators import *


def get_user_email():
    return auth.current_user.get("email") if auth.current_user else None


def get_time():
    return datetime.datetime.utcnow()


def get_user_name():
    r = db(db.auth_user.email == get_user_email()).select().first()
    return r.first_name + " " + r.last_name if r is not None else "Unknown"


def get_user():
    return auth.current_user.get("id") if auth.current_user else None


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

CATEGORY_KINDS = {
    "t": "Technology",
    "s": "Science",
    "m": "Mathematics",
    "h": "History",
    "l": "Literature",
}

db.define_table(
    "post",
    Field("title", requires=IS_NOT_EMPTY()),
    Field("text", requires=IS_NOT_EMPTY()),
    Field("time_asked", default=get_time, writable=False),
    Field("name", default=get_user_name),
    Field("user_email", default=get_user_email),
    Field("category", requires=IS_NOT_EMPTY()),
    Field("final", "integer", default=0),
)

db.post.id.readable = db.post.id.writable = False
db.post.final.readable = db.post.final.writable = False
db.post.user_email.readable = db.post.user_email.writable = False
db.post.name.readable = db.post.name.writable = False
db.post.category.requires = IS_IN_SET(CATEGORY_KINDS)
db.post.category.default = "t"

db.define_table(
    "rating",
    Field("post", "reference post"),
    Field("rater", "reference auth_user", default=get_user),
    Field("rating", "integer", default=0),
)

db.define_table(
    "answer",
    Field("post_id", "reference post"),
    Field("answer_user_email", default=get_user_email, writable=False),
    Field("time_answered", default=get_time, writable=False),
    Field("answer", requires=IS_NOT_EMPTY()),
    Field("name", default=get_user_name),
    Field("final", "integer", default=0),
    # Field("like", "integer", default=0, requires=IS_INT_IN_RANGE(0, 1e6)),
    # Field("dislike", "integer", default=0, requires=IS_INT_IN_RANGE(0, 1e6)),
    ## add in best answer (chosen by poster)
)

db.define_table(
    "answer_rating",
    Field("answer", "reference answer"),
    Field("rater", "reference auth_user", default=get_user),
    Field("rating", "integer", default=0),
)

db.commit()
