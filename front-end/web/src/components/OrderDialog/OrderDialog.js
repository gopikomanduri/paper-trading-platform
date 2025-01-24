import React, { useState } from "react";
import Draggable from "react-draggable"; // Import Draggable
import axiosInstance from "../../utils/axiosInstance";
import "./OrderDialog.css";

const OrderDialog = ({ email, symbol, type, onClose }) => {
  const [price, setPrice] = useState("");
  const [quantity, setQuantity] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate inputs
    if (!price || !quantity) {
      setError("Please provide both price and quantity");
      return;
    }

    try {
      // Construct the payload
      const payload = {
        email: email,
        symbol: symbol,
        order_type: type.toUpperCase(),
        price: parseFloat(price),
        quantity: parseInt(quantity, 10),
      };

      console.log("Payload being sent to the API:", payload);

      // Send the payload to the backend API
      const response = await axiosInstance.post("/orders/place_order", payload);

      console.log("Order placed successfully:", response.data);

      // Close the dialog after success
      onClose();
    } catch (error) {
      console.error("Error placing order:", error.response?.data || error.message);
      setError("Failed to place the order. Please try again.");
    }
  };

  return (
    <Draggable handle=".order-dialog-header" bounds="parent">
      <div className="order-dialog">
        <div className="order-dialog-header">
          <h3>
            {type.toUpperCase()} Order for {symbol}
          </h3>
          <button onClick={onClose} className="close-btn">
            ×
          </button>
        </div>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Price</label>
            <input
              type="number"
              step="0.01"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Quantity</label>
            <input
              type="number"
              step="1"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              required
            />
          </div>
          <div className="dialog-actions">
            <button type="submit" className="submit-btn">
              Submit
            </button>
            <button type="button" className="close-btn" onClick={onClose}>
              Close
            </button>
          </div>
        </form>
      </div>
    </Draggable>
  );
};

export default OrderDialog;
