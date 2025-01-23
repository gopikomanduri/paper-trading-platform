import React, { useState } from "react";
import { ResizableBox } from "react-resizable";
import "react-resizable/css/styles.css";
import { AdvancedRealTimeChart } from "react-ts-tradingview-widgets";
import { Rnd } from "react-rnd"; // Import react-rnd for draggable dialog
import axios from "axios";

const ChartPane = () => {
  const [width, setWidth] = useState(800);
  const [height, setHeight] = useState(400);
  const [orderDetails, setOrderDetails] = useState({
    orderType: "BUY",
    price: "",
    quantity: "",
  });
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [dialogPosition, setDialogPosition] = useState({
    x: 50,
    y: 50, // Default position of the dialog
  });

  const handleResize = (event, { size }) => {
    setWidth(size.width);
    setHeight(size.height);
  };

  const toggleDialog = (orderType) => {
    setOrderDetails({ ...orderDetails, orderType });
    setIsDialogOpen(!isDialogOpen);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setOrderDetails({ ...orderDetails, [name]: value });
  };

  const handlePlaceOrder = async () => {
    if (!orderDetails.price || !orderDetails.quantity) {
      alert("Please fill out all fields.");
      return;
    }

    try {
      const response = await axios.post("/orders/place_order", {
        email: "user@example.com",
        symbol: "AAPL",
        order_type: orderDetails.orderType,
        price: parseFloat(orderDetails.price),
        quantity: parseInt(orderDetails.quantity),
      });

      if (response.status === 200) {
        alert(`Order placed successfully: ${orderDetails.orderType}`);
        setIsDialogOpen(false); // Close dialog after placing order
      }
    } catch (error) {
      alert(`Failed to place order: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div style={{ margin: "20px" }}>
      <ResizableBox
        width={width}
        height={height}
        resizeHandles={["s", "e", "se"]}
        minConstraints={[300, 300]}
        maxConstraints={[1200, 800]}
        onResize={handleResize}
      >
        <div
          style={{
            width: "100%",
            height: "100%",
            border: "1px solid #ccc",
            background: "#fff",
            position: "relative",
          }}
        >
          {/* Candlestick Chart */}
          <AdvancedRealTimeChart
            symbol="NASDAQ:AAPL"
            interval="1"
            theme="dark"
            autosize
          />

          {/* Draggable Buy/Sell Dialog */}
          {isDialogOpen && (
            <Rnd
              style={{
                background: "#fff",
                border: "1px solid #ccc",
                borderRadius: "8px",
                boxShadow: "0px 0px 10px rgba(0, 0, 0, 0.2)",
                padding: "10px",
              }}
              default={{
                x: dialogPosition.x,
                y: dialogPosition.y,
                width: 200,
                height: "auto",
              }}
              bounds="parent"
              onDragStop={(e, d) => setDialogPosition({ x: d.x, y: d.y })}
            >
              <h4 style={{ textAlign: "center", marginBottom: "10px" }}>
                {orderDetails.orderType === "BUY" ? "Buy" : "Sell"}
              </h4>
              <input
                type="number"
                name="price"
                placeholder="Price"
                value={orderDetails.price}
                onChange={handleInputChange}
                style={{
                  width: "100%",
                  padding: "5px",
                  marginBottom: "10px",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
              />
              <input
                type="number"
                name="quantity"
                placeholder="Quantity"
                value={orderDetails.quantity}
                onChange={handleInputChange}
                style={{
                  width: "100%",
                  padding: "5px",
                  marginBottom: "10px",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
              />
              <button
                onClick={handlePlaceOrder}
                style={{
                  width: "100%",
                  padding: "10px",
                  background: orderDetails.orderType === "BUY" ? "#28a745" : "#dc3545",
                  color: "#fff",
                  border: "none",
                  borderRadius: "4px",
                  cursor: "pointer",
                  fontWeight: "bold",
                }}
              >
                Place {orderDetails.orderType} Order
              </button>
            </Rnd>
          )}

          {/* Floating Buy/Sell Buttons */}
          <div
            style={{
              position: "absolute",
              bottom: "20px",
              right: "20px",
              display: "flex",
              gap: "10px",
            }}
          >
            <button
              onClick={() => toggleDialog("BUY")}
              style={{
                padding: "10px",
                background: "#28a745",
                color: "#fff",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
              }}
            >
              Buy
            </button>
            <button
              onClick={() => toggleDialog("SELL")}
              style={{
                padding: "10px",
                background: "#dc3545",
                color: "#fff",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
              }}
            >
              Sell
            </button>
          </div>
        </div>
      </ResizableBox>
    </div>
  );
};

export default ChartPane;
