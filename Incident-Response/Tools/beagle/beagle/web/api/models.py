import json

from ..server import db


class JSONEncodedDict(db.TypeDecorator):
    impl = db.VARCHAR

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return None
        return json.loads(value)


class Graph(db.Model):
    __tablename__ = "graph"

    id = db.Column(db.Integer, primary_key=True)
    sha256 = db.Column(db.String(255), unique=True, nullable=False)
    meta = db.Column(JSONEncodedDict(), unique=False, nullable=False)
    category = db.Column(db.String(255), unique=False, nullable=False)
    comment = db.Column(db.String(255), unique=False, nullable=True)
    file_path = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<Graph category={self.category.capitalize()} sha256={self.sha256}>"

    def to_json(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "metadata": self.meta,
            "file_path": self.file_path,
        }
