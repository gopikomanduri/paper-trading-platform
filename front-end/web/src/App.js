import React from "react";
import Navbar from "./components/Navbar/Navbar";
import HeroSection from "./components/HeroSection/HeroSection";
import CandlestickChart from "./components/CandlestickChart/CandlestickChart";
import ChartPane from "./components/ChartPane/ChartPane";


// function App() {
//   return (
//     <div>
//       <Navbar />
//       <HeroSection />
//       <ChartPane />
//       <div style={{ margin: "20px" }}>
//         <h2>Live Candlestick Chart</h2>
//         <CandlestickChart />
//       </div>
//     </div>
//   );
// }

const App = () => {
  return (
    <div>
      <ChartPane />
    </div>
  );
};

export default App;
