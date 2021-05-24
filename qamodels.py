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


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
# db.define_table(
#     "profile",
#     Field("profile_user_email", default=get_user_email, writable=False),
#     Field("first_name", requires=IS_NOT_EMPTY()),
#     Field("last_name", requires=IS_NOT_EMPTY()),
#     Field("profession", requires=IS_NOT_EMPTY()),
#     Field("bio", requires=IS_NOT_EMPTY()),
# )

CATEGORY_KINDS = {
    "t": "Tech",
    "s": "Science",
    "m": "Mathematics",
    "h": "History",
    "l": "Literature",
}

db.define_table(
    "post",
    # Field("profile_id", "reference profile"),
    Field("post_user_email", default=get_user_email, writable=False),
    Field("time_asked", default=get_time, writable=False),
    Field("question", requires=IS_NOT_EMPTY()),
    Field("body", requires=IS_NOT_EMPTY()),
    Field("category", requires=IS_NOT_EMPTY()),
    ## add in resolved tag
)
db.post.category.requires = IS_IN_SET(CATEGORY_KINDS)
db.post.category.default = "t"
db.define_table(
    "answer",
    Field("post_id", "reference post"),
    Field("answer_user_email", default=get_user_email, writable=False),
    Field("time_answered", default=get_time, writable=False),
    Field("answer", requires=IS_NOT_EMPTY()),
    Field("like", "integer", default=0, requires=IS_INT_IN_RANGE(0, 1e6)),
    Field("dislike", "integer", default=0, requires=IS_INT_IN_RANGE(0, 1e6)),
    ## add in best answer (chosen by poster)
)

db.commit()
