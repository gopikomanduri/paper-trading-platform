import React, { useEffect, useRef } from "react";
import { createChart } from "lightweight-charts";
import "./Chart.css";

const Chart = () => {
  const chartContainerRef = useRef(null);

  useEffect(() => {
    // Create the chart
    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: {
        backgroundColor: "#FFFFFF",
        textColor: "#000",
      },
      grid: {
        vertLines: {
          color: "#e1e1e1",
        },
        horzLines: {
          color: "#e1e1e1",
        },
      },
      crosshair: {
        mode: 1,
      },
      priceScale: {
        borderColor: "#ccc",
      },
      timeScale: {
        borderColor: "#ccc",
      },
    });

    // Add a candlestick series to the chart
    const candleSeries = chart.addCandlestickSeries({
      upColor: "green",
      downColor: "red",
      borderDownColor: "red",
      borderUpColor: "green",
      wickDownColor: "red",
      wickUpColor: "green",
    });

    // Sample candlestick data
    const candlestickData = [
      { time: "2025-01-18", open: 120, high: 125, low: 118, close: 124 },
      { time: "2025-01-19", open: 124, high: 130, low: 122, close: 128 },
      { time: "2025-01-20", open: 128, high: 133, low: 127, close: 132 },
      { time: "2025-01-21", open: 132, high: 135, low: 130, close: 134 },
    ];

    // Set data to the candlestick series
    candleSeries.setData(candlestickData);

    // Resize the chart when the window is resized
    const handleResize = () => {
      chart.applyOptions({
        width: chartContainerRef.current.clientWidth,
      });
    };

    window.addEventListener("resize", handleResize);

    // Cleanup
    return () => {
      window.removeEventListener("resize", handleResize);
      chart.remove();
    };
  }, []);

  return (
    <div className="chart-container">
      <div ref={chartContainerRef} className="chart" />
    </div>
  );
};

export default Chart;
