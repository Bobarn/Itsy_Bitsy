from .db import db

class FavoritedItem(db.Model):
    __tablename__ = "favoriteditems"

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("users.id"))
    productId = db.Column(db.Integer, db.ForeignKey("products.id"))

    user = db.relationship("User", back_populates="favorited_items")
    product = db.relationship("Product", back_populates="favorited_items")

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'productId': self.productId,
        }
