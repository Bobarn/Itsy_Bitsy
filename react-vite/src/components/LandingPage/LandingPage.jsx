import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { thunkGetAllProductsWImages } from "../../redux/product";
import { thunkCreateFavorite,thunkDeleteFavorite  } from "../../redux/favorited_items";
import { thunkGetAllFavorites } from "../../redux/favorited_items";
import { useNavigate } from "react-router-dom";
import CategoryImages from "./CategoryImages";
import TrendingImages from "./TrendingImages";
import "./LandingPage.css";

function LandingImage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const allProducts = useSelector((state) => state.products);
  const currUser = useSelector((state) => state.session.user);
  const allFavorites = useSelector(state => state.favorites)
  console.log(allFavorites)
  const filteredProducts = Object.values(allProducts).slice(0, 10);

  const filteredByCat = Object.values(allProducts).filter(
    (prod) => prod.category === "Art"
  );

  // LOADS PRODUCTS
  useEffect(() => {
    dispatch(thunkGetAllProductsWImages());
  }, [dispatch]);

  useEffect(() =>{
    dispatch(thunkGetAllFavorites())
  },[])
  //

  // ADD TO FAVORITES ONCLICK FUNCTION


  const addToFav = (productId) => {
    // e.preventDefault();
    if(currUser.id && allFavorites[productId]) {
      dispatch(thunkDeleteFavorite(productId))
    }
    else if(currUser.id) {
      dispatch(thunkCreateFavorite(productId));
    }

  };


  const imageCreator = () => {
    return (
      <div className="main-img-cont">
        {filteredProducts.map((product) => (
          <div key={product.id} className="single-img-tile">
            <div
              className="heart-button"
              onClick={() =>
                currUser
                  ? addToFav(product.id)
                  : window.alert("Must sign-in to add to favorites!")
              }
            >

                <i className={ allFavorites[product.id]?"fa-solid fa-heart filled-heart" : "fa-regular fa-heart empty-heart" }></i>

            </div>
            <div
              className="sqr-img-cont"
              onClick={() => navigate(`/products/${product.id}`)}
            >
              <img
                className="sqr-img"
                src={product.preview_image}
                onError={(e) => {
                  e.target.src =
                    "https://i.graphicmama.com/uploads/2023/3/64182e9d20d37-spider-animated-gifs.gif";
                }}
              />
            </div>
            <div className="price-cont">
              <span>${product.price}</span>
            </div>
          </div>
        ))}
      </div>
    );
  };

  if (!allProducts) return null;
  return (
    <div className="landing-main-cont">
      <div className="greeting-cont">
        <span>
          Welcome,{" "}
          {currUser ? "back" + " " + currUser.first_name + "!" : "To Itsy"}
        </span>
      </div>
      <CategoryImages />

      <div className="landing-sqrImg-main-cont">{imageCreator()}</div>

      <TrendingImages products={filteredByCat} />
    </div>
  );
}

export default LandingImage;
