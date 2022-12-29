import React, { useState, useEffect } from "react";
import { BsPlusLg } from "react-icons/bs";
import { AiOutlineAmazon } from "react-icons/ai";
import bgImage from "./assets/bg.png";
import loading from "./assets/loading.svg";

const App = () => {
  const [urlAmz, setUrlAmz] = useState("");
  const [sentiments, setSentiments] = useState([]);
  const [keywords, setKeywords] = useState([]);
  const [summary, setSummary] = useState([]);
  const [productData, setProductData] = useState([]);
  const [finalSentimentRating, setFinalSentimentRating] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const emojis = [
    "😠 - Very bad",
    "🙁 - Somewhat bad",
    "😐 - Okay",
    "🙂 - Somewhat good",
    "😄 - Very good",
  ];

  function handleSubmit(e) {
    setIsLoading(true);

    e.preventDefault();
    fetch(
      "http://localhost:5500/analyze?url_amz=" + new URLSearchParams(urlAmz)
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

  function handleChange(e) {
    setUrlAmz(e.target.value);
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
    setFinalSentimentRating(
      Math.round(totalSentimentRating / sentiments.length) - 1
    );
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
            onChange={(e) => handleChange(e)}
            value={urlAmz}
          />
          <input
            type="text"
            name="name"
            placeholder="Flipkart"
            className="w-full border p-2 hidden hover:border-black rounded-md "
          />
          <span className="shadow-lg transition ease-in-out delay-150 bg-slate-50 hover:-translate-y-1 hover:scale-110 hover:bg-black duration-300 cursor-pointer rounded-md p-3">
            <BsPlusLg className=" text-[#87ce70] text-xs" />
          </span>
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
                {productData.title}
                <hr />
              </h1>

              <div className="bg-white lg:w-[580px] rounded-md shadow-md hover:drop-shadow-xl">
                <img
                  src={productData.imageURL}
                  alt="product"
                  className="  rounded-md "
                />
              </div>
              <a
                href={productData.productURL}
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
                Overall sentiment <br />{" "}
                <div
                  className={
                    finalSentimentRating < 2
                      ? "text-red-500"
                      : finalSentimentRating > 2
                      ? "text-green-500"
                      : "text-orange-500"
                  }
                >
                  {emojis[finalSentimentRating]}
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
