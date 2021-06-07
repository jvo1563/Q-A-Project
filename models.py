"""
This file defines the database models
"""

import datetime, base64, os
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

# CREATE TABLE `auth_user` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `username` varchar(512) DEFAULT NULL,
#   `email` varchar(512) DEFAULT NULL,
#   `password` varchar(512) DEFAULT NULL,
#   `first_name` varchar(512) DEFAULT NULL,
#   `last_name` varchar(512) DEFAULT NULL,
#   `sso_id` varchar(512) DEFAULT NULL,
#   `action_token` varchar(512) DEFAULT NULL,
#   `last_password_change` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`),
#   `past_passwords_hash` text DEFAULT NULL,
#   UNIQUE KEY `username` (`username`),
#   UNIQUE KEY `email` (`email`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# CREATE TABLE `auth_user_tag_groups` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `path` varchar(512) DEFAULT NULL,
#   `record_id` int(11) DEFAULT NULL,
#   PRIMARY KEY (`id`),
#   KEY `record_id_fk` (`record_id`),
#   CONSTRAINT `record_id_fk` FOREIGN KEY (`record_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# CREATE TABLE `py4web_session` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `rkey` varchar(512) DEFAULT NULL,
#   `rvalue` text,
#   `expiration` int(11) DEFAULT NULL,
#   `created_on` datetime DEFAULT NULL,
#   `expires_on` datetime DEFAULT NULL,
#   PRIMARY KEY (`id`),
#   KEY `rkey__idx` (`rkey`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;


# CREATE TABLE `post`(
#     `id` int(11) NOT NULL AUTO_INCREMENT,
#     `title` varchar(512) DEFAULT NULL,
#     `text` varchar(512) DEFAULT NULL,
#     `time_asked` varchar(512) DEFAULT NULL,
#     `name` varchar(512) DEFAULT NULL,
#     `user_email` varchar(512) DEFAULT NULL,
#     `category` varchar(512) DEFAULT NULL,
#     `final` int(11) DEFAULT 0,
#     `post_id` int(11) DEFAULT NULL,
#     PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# CREATE TABLE `rating` (
#     `id` int(11) NOT NULL AUTO_INCREMENT,
#     `post` INTEGER REFERENCES `post` (`id`) ON DELETE CASCADE  ,
#     `rater` INTEGER REFERENCES `auth_user` (`id`) ON DELETE CASCADE  ,
#     `rating` INTEGER,
#     PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;;

# CREATE TABLE `answer` (
#     `id` int(11) NOT NULL AUTO_INCREMENT,
#     `post_id` INTEGER REFERENCES `post` (`id`) ON DELETE CASCADE  ,
#     `answer_user_email` CHAR(200),
#     `time_answered` CHAR(200),
#     `answer` CHAR(200),
#     `name` CHAR(200),
#     `final` INTEGER,
#     PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# CREATE TABLE `answer_rating` (
#     `id` int(11) NOT NULL AUTO_INCREMENT,
#     `answer` INTEGER REFERENCES `answer` (`id`) ON DELETE CASCADE  ,
#     `rater` INTEGER REFERENCES `auth_user` (`id`) ON DELETE CASCADE  ,
#     `rating` INTEGER,
#     PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# CREATE TABLE `user` (
#     `id` int(11) NOT NULL AUTO_INCREMENT,
#     `auth_id` INTEGER REFERENCES `auth_user` (`id`) ON DELETE CASCADE  ,
#     `bio` CHAR(200),
#     PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# CREATE TABLE `upload`(
#     `id` int(11) NOT NULL AUTO_INCREMENT,
#     `owner` CHAR(200),
#     `file_name` CHAR(200),
#     `file_type` CHAR(200),
#     `file_date` CHAR(200),
#     `file_path` CHAR(200),
#     `file_size` INTEGER,
#     `confirmed` CHAR(1),
#     PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
db.post.time_asked.readable = db.post.time_asked.writable = False
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
)

db.define_table(
    "answer_rating",
    Field("answer", "reference answer"),
    Field("rater", "reference auth_user", default=get_user),
    Field("rating", "integer", default=0),
)

db.define_table(
    "user", Field("auth_id", "reference auth_user"), Field("bio"),
)

db.define_table(
    "upload",
    Field("owner", default=get_user_email),
    Field("file_name"),
    Field("file_type"),
    Field("file_date"),
    Field("file_path"),
    Field("file_size", "integer"),
    Field("confirmed", "boolean", default=False),  # Was the upload to GCS confirmed?
)
db.commit()
