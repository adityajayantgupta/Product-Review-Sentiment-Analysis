import React, { useState, useEffect } from "react";
import ReactSpeedometer from "react-d3-speedometer";
import { AiOutlineAmazon } from "react-icons/ai";
import bgImage from "./assets/bg.png";
import loading from "./assets/loading.svg";

const App = () => {
  const [urlAmz, setUrlAmz] = useState("");
  const [urlFlp, setUrlFlp] = useState("");
  const [sentiments, setSentiments] = useState([]);
  const [keywords, setKeywords] = useState([]);
  const [summary, setSummary] = useState([]);
  const [productData, setProductData] = useState({
    amazon: {
      productURL: "",
      title: "",
      rating: "",
      imageURL: "",
      price: "",
    },
    flipkart: {
      productURL: "",
      title: "",
      rating: "",
      imageURL: "",
      price: "",
    },
  });
  const [finalSentimentRating, setFinalSentimentRating] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const sentiment = [
    "Very bad",
    "Somewhat bad",
    "Okay",
    "Somewhat good",
    "Very good",
  ];

  function handleSubmit(e) {
    setIsLoading(true);

    e.preventDefault();
    fetch(
      "http://localhost:5500/analyze?url_amz=" +
        new URLSearchParams(urlAmz) +
        "&url_flp=" +
        new URLSearchParams(urlFlp)
    )
      .then((response) => response.json())
      .then((responseJSON) => {
        console.log(responseJSON);
        setSentiments(responseJSON.analysis.scores);
        setKeywords(responseJSON.analysis.keywords);
        setSummary(responseJSON.analysis.summaries);
        setProductData(responseJSON.productData);
      });
  }

  useEffect(() => {
    if (isLoading) {
      document.body.style.backgroundImage = bgImage;
    } else {
      document.body.style.backgroundImage = "";
    }
  }, [isLoading]);

  useEffect(() => {
    setIsLoading(true);
  }, []);

  useEffect(() => {
    let totalSentimentRating = 0;
    sentiments.forEach((sentiment) => {
      let rating = sentiment.split(" ")[0];
      totalSentimentRating += parseInt(rating);
    });
    setFinalSentimentRating(totalSentimentRating / sentiments.length);
    setIsLoading(false);
  }, [sentiments]);

  return (
    <form className="" onSubmit={(e) => handleSubmit(e)}>
      {/*search area*/}
      {/*product area*/}
      <div className="lg:m-6 m-2">
        <nav className="w-full flex items-center sm:items-center justify-evenly gap-3 sm:px-5 sm:py-5">
          <AiOutlineAmazon />
          <input
            type="text"
            name="name"
            placeholder="Amazon"
            className="w-full border p-2 shadow-md rounded-md"
            onChange={(e) => setUrlAmz(e.target.value)}
            value={urlAmz}
          />
          <input
            type="text"
            name="name"
            placeholder="Optional - Flipkart"
            className="w-full border p-2 hover:border-black rounded-md"
            onChange={(e) => setUrlFlp(e.target.value)}
            value={urlFlp}
          />
          <button
            className="transition ease-in-out delay-150 bg-white hover:-translate-y-1 hover:scale-110 hover:bg-[#87ce70] duration-300 px-4 py-2 rounded-lg shadow-lg text-[#87ce70] hover:text-white"
            type="submit"
          >
            Search
          </button>
        </nav>

        {!isLoading && (
          <div className="m-3 lg:flex flex flex-wrap justify-between lg:gap-1 gap-12 py-5">
            <div className="flex flex-col lg:w-[600px] items-center gap-6">
              <h1 className="lg:text-xl text-sm font-semibold p-2 text-left">
                {productData.amazon.title || productData.flipkart.title}
                <hr />
              </h1>
              <div className="bg-white lg:w-[580px] rounded-md shadow-md hover:drop-shadow-xl">
                <img
                  src={
                    productData.amazon.imageURL || productData.flipkart.imageURL
                  }
                  alt="product"
                  className="  rounded-md "
                />
              </div>
              {productData.amazon.rating || ""}
              {productData.flipkart.rating || ""} out of 5
              <a
                href={
                  productData.amazon.productURL ||
                  productData.flipkart.productURL
                }
                className="transition ease-in-out delay-150 bg-red-500 hover:-translate-y-1 hover:scale-110 hover:bg-orange-500 duration-300 p-2 rounded-lg text-white text-md shadow-md shadow-blue-300 w-1/2 text-center"
              >
                Go to vendor
              </a>
            </div>
            <div className="flex flex-col lg:w-[450px]  items-center justify-between">
              <h1 className="lg:text-3xl text-normal font-semibold">
                Review summary
              </h1>
              <p>{summary}</p>
              <hr />
              <h1 className="lg:text-3xl text-normal font-semibold">
                Keywords
              </h1>
              <div className=" lg:w-[430px]">
                {keywords.length > 0 &&
                  keywords.map((keyword) => {
                    return <span className="mr-2">{keyword}</span>;
                  })}
              </div>
            </div>

            <div className="bg-white flex flex-col p-2 items-center justify-center">
              <h1 className="lg:text-3xl text-normal font-bold ">
                Sentiment Rating <br />{" "}
                <ReactSpeedometer
                  maxValue={5}
                  value={finalSentimentRating}
                  segments={5}
                  needleTransitionDuration={4000}
                  needleTransition="easeElastic"
                  customSegmentLabels={[
                    {
                      text: "😠",
                      position: "INSIDE",
                      color: "#555",
                    },
                    {
                      text: "🙁",
                      position: "INSIDE",
                      color: "#555",
                    },
                    {
                      text: "😐",
                      position: "INSIDE",
                      color: "#555",
                      fontSize: "19px",
                    },
                    {
                      text: "🙂",
                      position: "INSIDE",
                      color: "#555",
                    },
                    {
                      text: "😄",
                      position: "INSIDE",
                      color: "#555",
                    },
                  ]}
                />
                <div
                  className={
                    finalSentimentRating < 2
                      ? "text-red-500"
                      : finalSentimentRating > 2
                      ? "text-green-500"
                      : "text-orange-500"
                  }
                >
                  {sentiment[finalSentimentRating]}
                </div>
              </h1>
            </div>
          </div>
        )}
        {isLoading && (
          <div className="h-screen flex items-center justify-center">
            <img src={loading}></img>
          </div>
        )}
      </div>
    </form>
  );
};

export default App;
