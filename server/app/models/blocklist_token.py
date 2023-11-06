from .. import db


class BlocklistToken(db.Model):
    token_id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)

    def serialize(self):
        return {"token_id": self.token_id, "jti": self.jti}
