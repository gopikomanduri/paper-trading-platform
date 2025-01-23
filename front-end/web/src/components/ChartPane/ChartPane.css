import React, { useState } from "react";
import { ResizableBox } from "react-resizable";
import "react-resizable/css/styles.css";
import { AdvancedRealTimeChart } from "react-ts-tradingview-widgets";

const ChartPane = () => {
  // Initial width and height
  const [width, setWidth] = useState(800); // Default width in pixels
  const [height, setHeight] = useState(400); // Default height in pixels

  const handleResize = (event, { size }) => {
    // Update the width and height dynamically
    setWidth(size.width);
    setHeight(size.height);
  };

  return (
    <div style={{ margin: "20px" }}>
      <ResizableBox
        width={width} // Numeric value for width
        height={height} // Numeric value for height
        resizeHandles={["s", "e", "se"]}
        minConstraints={[300, 300]} // Minimum size (in pixels)
        maxConstraints={[1200, 800]} // Maximum size (in pixels)
        onResize={handleResize}
      >
        <div
          style={{
            width: "100%",
            height: "100%",
            border: "1px solid #ccc",
            background: "#fff",
          }}
        >
          <AdvancedRealTimeChart
            symbol="NASDAQ:AAPL" // Update with desired stock symbol
            interval="5"
            theme="dark"
            autosize
          />
        </div>
      </ResizableBox>
    </div>
  );
};

export default ChartPane;
