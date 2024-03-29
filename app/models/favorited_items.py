from .db import db, environment, SCHEMA, add_prefix_for_prod

class FavoritedItem(db.Model):
    __tablename__ = "favoriteditems"

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")))
    productId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("products.id")))

    user = db.relationship("User", back_populates="favorited_items")
    product = db.relationship("Product", back_populates="favorited_items")

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'productId': self.productId,
        }
