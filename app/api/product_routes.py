from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from app.models import db, Product, ProductImage
from app.forms import ProductForm, ImageForm
from sqlalchemy import desc
from .AWS import upload_file_to_s3, get_unique_filename, remove_file_from_s3

product_routes = Blueprint("products",__name__)





# get all products
@product_routes.route('/all')
def get_all_products():
    # we want all products regardless of category but maybe sort them based on category?
    # or we just display based on id
    # page = request.args.get('page')
    # if page == None:
    #     page = 1
    # page = (int(page) - 1) * 10
    # products = Product.query.order_by(desc(Product.created_at)).limit(10).offset(page).all()
    products = Product.query.order_by(desc(Product.created_at)).all()

    if not products:
        return {"message": "That page does not exist"}, 404
    list_dict_products = [product.to_dict() for product in products]
    return {"products":list_dict_products}



# POSSIBLE CHANGE TO QUERY IMAGES WITH THE PRODUCTS TO MAKE TILES EASIER.

@product_routes.route('/images')
def get_all_products_with_images():

    products = Product.query.order_by(desc(Product.created_at)).all()
    if not products:
        return {"message": "That page does not exist"}, 404
    # list_dict_products = [product.to_dict() for product in products]
    list_dict_products = []

    for product in products:
        product_dict = product.to_dict()
        product_images = ProductImage.query.filter_by(productId=product.id).all()


        product_dict['product_images'] = [image.to_dict() for image in product_images]

        list_dict_products.append(product_dict)


    return {"products":list_dict_products}




#get all products by category
@product_routes.route('/category/<cat>')
def get_products_by_category(cat):
    print(cat)
    if cat not in ['Jewelry', 'Clothes', 'Art', 'Art Supplies', 'Electronics', 'Pet Supplies']:
        return {"message": "Category doesn't exist"}, 404
    # page = request.args.get('page')

    products = Product.query.filter_by(category=cat).all()
    if not products:
        return {"message": "That page does not exist"}, 404
    return {"products": [product.to_dict() for product in products]}

#get a product's description
@product_routes.route('/<int:id>')
def get_product_details(id):
    product = Product.query.get(id)
    if product is None:
        return {"message": "Product doesn't exist"}, 404
    return {"product":product.to_dict()}

#get all products of the current user
@product_routes.route('/current', methods=['GET'])
@login_required
def get_current_user_products():
    products = Product.query.filter_by(sellerId=current_user.id).all()
    if not products:
        return {"message": "That page does not exist"}, 404
    return {"products": [product.to_dict() for product in products]}


@product_routes.route('/new', methods=['POST'])
@login_required
def create_product():
    form = ProductForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data

        newProduct = Product(
            sellerId=current_user.id,
            name=data["name"],
            description=data["description"],
            price=data["price"],
            category=data["category"],
            shipping_time=data["shipping_time"],
            return_policy=data["return_policy"],
            free_shipping=data["free_shipping"]
        )

        db.session.add(newProduct)
        db.session.commit()

        return {"product": newProduct.to_dict()}
    else:
        return form.errors, 401

@product_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_product(id):
    product = Product.query.get(id)

    if product is None:
        return {'message': "Product doesn't exist"}, 404

    if current_user.id != product.sellerId:
        return {'message': "You do not have permission to update this product"}, 403

    form = ProductForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    print(form.data)

    if form.validate_on_submit():
        # data = form.data

        # product.sellerId=current_user.id,
        # product.name=data["name"],
        # product.description=data["description"],
        # product.price=data["price"],
        # product.category=data["category"],
        # product.shipping_time=data["shipping_time"],
        # product.return_policy=data["return_policy"],
        # product.free_shipping=data["free_shipping"]
        product.sellerId = current_user.id
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.category = form.category.data
        product.shipping_time = form.shipping_time.data
        product.return_policy = form.return_policy.data
        product.free_shipping = form.free_shipping.data

        # print(product)

        db.session.commit()

        updated_product = Product.query.get(id)

        return {"product": updated_product.to_dict()}
    else:
        return form.errors, 401

#delete a specific product
@product_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_specific_product(id):
    print("WE ARE IN THE DELETION")

    product = Product.query.get(id)

    if product is None:
        return {'message': "Product doesn't exist"}, 404

    if current_user.id != product.sellerId:
        return {'message': "You do not have permission to delete this product"}, 403

    for image in product.images:
        remove_file_from_s3(image.url)
        db.session.delete(image)

    db.session.delete(product)
    db.session.commit()

    return {'message': 'Product deleted successfully'}, 200

@product_routes.route("/<int:id>/images",methods=['GET'])
def product_images(id):

    products = ProductImage.query.filter(productId=id)
    if not products:
        return {"message": "No images for that product"}
    return {"product_images": [product.to_dict() for product in products]}


@product_routes.route("/<int:id>/images/new", methods=['POST'] )
@login_required
def post_product_images(id):
    form = ImageForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():

        url = form.data["url"]
        imageName = form.data["url"].filename

        url.filename = get_unique_filename(url.filename)

        upload = upload_file_to_s3(url)

        if "url" not in upload:
            return upload, 401

        new_image = ProductImage(url=upload["url"], preview=form.data["preview"], image_name=imageName, productId=int(id))

        db.session.add(new_image)
        db.session.commit()
        updated_product = Product.query.get(id)

        return {"product": updated_product.to_dict()}, 201
    return { "post_product_images": form.errors }

@product_routes.route("/images/<int:id>", methods=['PUT'])
@login_required
def update_product_images(id):
    productImage = ProductImage.query.get(id)
    if productImage:
        form = ImageForm()
        form["csrf_token"].data = request.cookies["csrf_token"]
        if form.validate_on_submit():
            remove_file_from_s3(productImage.url)

            url = form.data["url"]

            imageName = form.data["url"].filename

            url.filename = get_unique_filename(url.filename)

            upload = upload_file_to_s3(url)

            if "url" not in upload:
                return upload, 401

            productImage.url = upload["url"]
            productImage.image_name = imageName

            db.session.commit()
            return {"product_image": productImage.product.to_dict()}
        return { "update_product_images": form.errors }
    else:
        return {'message': "Image does not exist"}, 404


@product_routes.route("/<int:id>/preview", methods=['PUT'])
@login_required
def update_preview_image(id):
    form = ImageForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        productImage = ProductImage.query.filter_by(productId=id, preview=True).first()
        if productImage:
            remove_file_from_s3(productImage.url)
            url = form.data["url"]
            imageName = form.data["url"].filename
            url.filename = get_unique_filename(url.filename)
            upload = upload_file_to_s3(url)
            if "url" not in upload:
                return upload, 401
            productImage.url = upload["url"]
            productImage.image_name = imageName
            db.session.commit()
            return {"product_image": productImage.product.to_dict()}
        else:
            return {'message': "Image does not exist"}, 404
    return { "update_preview_image": form.errors }

@product_routes.route("/images/<int:id>", methods=['DELETE'])
@login_required
def delete_product_images(id):
    productImage = ProductImage.query.get(id)
    if productImage:
        remove_file_from_s3(productImage.url)
        db.session.delete(productImage)
        db.session.commit()
        return {'id' : "Image deleted successfully!"}
    else:
        return {'message': "Image does not exist"}, 404
