import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { useState } from 'react';
import { useModal } from '../../context/Modal.jsx';
import { thunkDeleteProduct, thunkGetUserStore } from '../../redux/product.js';
import './ProductDeleteModal.css'

export default function DeleteProductConfirmationModal( { productId } ) {
    const dispatch = useDispatch();
    const { closeModal } = useModal();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
      // closeModal()
      setLoading(true)

      await dispatch(thunkDeleteProduct(productId))
      .then(() => dispatch(thunkGetUserStore()))
      .then(() => closeModal())
      .then(() => setLoading(false))
      .then(() => navigate('/'))
    };

    const handleCancel = () => {

      return closeModal();
    }

    return (
      <div id='delete-product-modal'>
        <h1>Confirm Delete</h1>
        <h3>Are you sure you want to remove this listing?</h3>
        <div id='delete-buttons-cont'>
          <button className='delete-button' onClick={handleSubmit}><h2 className='delete-button-title'>Yes</h2> &#40;Delete Item&#41;</button>
          <button className='keep-button' onClick={handleCancel}><h2 className='delete-button-title'>No</h2> &#40;Keep Item&#41;</button>
        </div>
        {loading && <><div className="loader-delete"></div><div className="loader-text-delete">Loading...</div></>}
      </div>
    );
  }
