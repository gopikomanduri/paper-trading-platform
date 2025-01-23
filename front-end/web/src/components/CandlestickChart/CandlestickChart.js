import React, { useEffect, useRef } from "react";
import { createChart } from "lightweight-charts";
import axios from "axios";

const CandlestickChart = () => {
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);
  const candleSeriesRef = useRef(null);

  useEffect(() => {
    // Initialize the chart
    chartRef.current = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: {
        backgroundColor: "#ffffff",
        textColor: "#000000",
      },
      grid: {
        vertLines: {
          color: "#eeeeee",
        },
        horzLines: {
          color: "#eeeeee",
        },
      },
      crosshair: {
        mode: 0, // Normal mode
      },
      priceScale: {
        borderColor: "#cccccc",
      },
      timeScale: {
        borderColor: "#cccccc",
        timeVisible: true,
        secondsVisible: false,
      },
    });

    candleSeriesRef.current = chartRef.current.addCandlestickSeries({
      upColor: "#26a69a",
      downColor: "#ef5350",
      borderDownColor: "#ef5350",
      borderUpColor: "#26a69a",
      wickDownColor: "#ef5350",
      wickUpColor: "#26a69a",
    });

    // Resize the chart on window resize
    const handleResize = () => {
      chartRef.current.applyOptions({
        width: chartContainerRef.current.clientWidth,
      });
    };

    window.addEventListener("resize", handleResize);

    // Cleanup
    return () => {
      window.removeEventListener("resize", handleResize);
      chartRef.current.remove();
    };
  }, []);

  useEffect(() => {
    // Fetch historical data
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "https://www.alphavantage.co/query", // Replace with your data provider
          {
            params: {
              function: "TIME_SERIES_INTRADAY",
              symbol: "ibm", // Replace with your symbol
              interval: "1min",
              apikey: "A63XOTLL73SV83PD", // Replace with your Alpha Vantage API key
            },
          }
        );

        const data = response.data["Time Series (1min)"];
        const formattedData = Object.keys(data).map((timestamp) => ({
          time: new Date(timestamp).getTime() / 1000,
          open: parseFloat(data[timestamp]["1. open"]),
          high: parseFloat(data[timestamp]["2. high"]),
          low: parseFloat(data[timestamp]["3. low"]),
          close: parseFloat(data[timestamp]["4. close"]),
        }));

        // Set the data to the chart
        candleSeriesRef.current.setData(formattedData.reverse());
      } catch (error) {
        console.error("Error fetching candlestick data:", error);
      }
    };

    fetchData();
  }, []);

  return <div ref={chartContainerRef} style={{ position: "relative", margin: "20px auto" }} />;
};

export default CandlestickChart;
