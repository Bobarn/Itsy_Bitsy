from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime



class OrderItem(db.Model):
    __tablename__ = "order_items"

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('orders.id')), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('products.id')), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now)

    order = db.relationship("Order", back_populates="order_items", )
    product = db.relationship("Product", back_populates="buying")

    def to_dict(self):

        return {
            "id": self.id,
            "order_id": self.order_id,
            "quantity": self.quantity,
            "product":self.product.to_dict()
        }
