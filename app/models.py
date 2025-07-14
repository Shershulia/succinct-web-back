from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    outgoing = db.relationship(
        'Connection',
        backref='source_user',
        primaryjoin='User.id==Connection.source_id',
        lazy=True
    )

    ingoing = db.relationship(
        'Connection',
        backref='target_user',
        primaryjoin='User.id==Connection.target_id',
        lazy=True
    )

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('source_id', 'target_id', name='unique_connection'),
    )
