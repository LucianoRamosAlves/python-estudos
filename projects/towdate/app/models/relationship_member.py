from datetime import datetime

from app.extensions import db


class RelationshipMember(db.Model):
    __tablename__ = "relationship_members"

    id = db.Column(db.Integer, primary_key=True)

    relationship_id = db.Column(
        db.Integer,
        db.ForeignKey("relationships.id"),
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    joined_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    relationship = db.relationship(
        "Relationship",
        back_populates="members",
    )

    user = db.relationship(
        "User",
        back_populates="relationships",
    )

    def __repr__(self):
        return (
            f"<RelationshipMember "
            f"relationship={self.relationship_id} "
            f"user={self.user_id}>"
        )