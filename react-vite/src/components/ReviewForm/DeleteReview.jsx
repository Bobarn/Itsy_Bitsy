import "./DeleteReview.css";
import { useDispatch, useSelector } from "react-redux";
import { thunkDeleteReview } from "../../redux/reviews";
import { useModal } from "../../context/Modal";
import { thunkGetAllProducts } from "../../redux/product";
import { useParams } from "react-router-dom";


function DeleteReview({ reviewId }) {
  const dispatch = useDispatch();
  const { closeModal } = useModal();


  const { productId } = useParams();
  const product = useSelector((state) => state.products[productId]);

  const deleteReview = (e) => {

    e.preventDefault();

    dispatch(thunkDeleteReview(reviewId));

    dispatch(thunkGetAllProducts(product));

    closeModal();

  };

  const cancel = () => {
    closeModal();
  };

  return (
    <>
      <div className="delete-rev-modal" >
      <h1>CONFIRM DELETE</h1>
      <p> Are you sure you want to delete this review? </p>
      <button className="yes-button" onClick={deleteReview}>
        YES PLEASE
      </button>
      <button className="cancel-button" onClick={cancel}>
        CANCEL
      </button>
      </div>
    </>
  );
}

export default DeleteReview;
