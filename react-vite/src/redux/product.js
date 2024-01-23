const GET_ALL_PRODUCTS = "products/getAllProducts";
const CREATE_PRODUCT = "products/makeProduct";
const DELETE_PRODUCT = "products/deleteProduct";
const UPDATE_PRODUCT = "products/updateProduct";

const getAllProducts = (products) => {
  return {
    type: GET_ALL_PRODUCTS,
    products,
  };
};

const createProduct = (product) => {
  return {
    type: CREATE_PRODUCT,
    product,
  };
};

const deleteProduct = (productId) => {
  return {
    type: DELETE_PRODUCT,
    productId,
  };
};

const updateProduct = (product) => {
  return {
    type: UPDATE_PRODUCT,
    product,
  };
};

export const thunkGetAllProducts = () => async (dispatch) => {
  const response = await fetch("/api/products/all");

  if (response.ok) {
    const products = await response.json();

    dispatch(getAllProducts(products));

    return products;
  } else {
    return { errors: "Could not get all products" };
  }
};

export const thunkCreateProduct =
  (productFormData, images) => async (dispatch) => {
    const response = await fetch("/api/products/new", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(productFormData),
    });

    if (response.ok) {
      const newProduct = await response.json();

      // for (let image in images) {
      //   console.log(image)
      //   const imageResponse = await fetch(
      //     `/api/products/${newProduct.id}/images/new`,
      //     {
      //       method: "POST",
      //       headers: { "Content-Type": "application/json" },
      //       body: JSON.stringify({
      //         "url": image
      //       }),
      //     }
      //   );
      // }
      // ! Consider attaching images or revisit to see if we need/should return images
      dispatch(createProduct(newProduct));

      return newProduct;
    } else {
      const errors = await response.json();
      return errors
    }
  };

export const thunkDeleteProduct = (productId) => async (dispatch) => {
  const response = await fetch(`/api/products/${productId}`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
  });

  if (response.ok) {
    const message = await response.json();
    dispatch(deleteProduct(productId));

    return message;
  } else {
    const error = await response.json();

    return error;
  }
};

export const thunkUpdateProduct = (productId, product) => async (dispatch) => {
  const response = await fetch(`/api/products/${productId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(product),
  });

  if (response.ok) {
    const updatedProduct = await response.json();

    return updatedProduct;
  } else {
    const errors = await response.json();
    return errors;
  }
};

function productReducer(state = {}, action) {
  switch (action.type) {
    case GET_ALL_PRODUCTS: {
      let products = action.products.products;
      let newProducts = {};

      products.map((product) => {
        newProducts[product.id] = product;
      });

      return { ...state, ...newProducts };
    }
    case CREATE_PRODUCT: {
      const product = action.product.product;
      const newState = { ...state };
      newState[product.id] = product;
      return newState;
    }
    case DELETE_PRODUCT: {
      const newState = { ...state };
      delete newState[action.productId];

      return newState;
    }
    case UPDATE_PRODUCT: {
      const product = action.product.product;
      const newState = { ...state };
      newState[product.id] = product;
      return newState;
    }
    default:
      return state;
  }
}

export default productReducer;
