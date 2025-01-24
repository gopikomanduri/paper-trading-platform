import React, { useState } from "react";
import { Resizable } from "re-resizable";
import OrderDialog from "../OrderDialog/OrderDialog"; // Import the dialog component

const ChartPane = () => {
  const [showDialog, setShowDialog] = useState(false);
  const [orderType, setOrderType] = useState("");

  const openDialog = (type) => {
    setOrderType(type);
    setShowDialog(true);
  };

  const closeDialog = () => {
    setShowDialog(false);
    setOrderType("");
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        backgroundColor: "#f8f8f8",
      }}
    >
      <div style={{ marginBottom: "20px" }}>
        <button
          onClick={() => openDialog("Buy")}
          style={{ marginRight: "10px", backgroundColor: "green", color: "white", padding: "5px 10px", border: "none", borderRadius: "4px" }}
        >
          Buy
        </button>
        <button
          onClick={() => openDialog("Sell")}
          style={{ backgroundColor: "red", color: "white", padding: "5px 10px", border: "none", borderRadius: "4px" }}
        >
          Sell
        </button>
      </div>
      <Resizable
        style={{
          border: "1px solid #ddd",
          background: "#fff",
          display: "flex",
          flexDirection: "column",
          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
        }}
        defaultSize={{
          width: 800,
          height: 400,
        }}
        minWidth={600}
        minHeight={300}
        maxWidth="90vw"
        maxHeight="90vh"
      >
        {/* Chart Embed */}
        <iframe
          src="https://s.tradingview.com/widgetembed/"
          title="TradingView Chart"
          style={{
            width: "100%",
            height: "100%",
            border: "none",
          }}
        ></iframe>
      </Resizable>
      {showDialog && <OrderDialog 
      symbol = "IBM"
      email = "a@a.com"
      type={orderType} 
      onClose={closeDialog} />}
    </div>
  );
};

export default ChartPane;
