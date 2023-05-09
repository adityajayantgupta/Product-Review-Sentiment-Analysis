import "@fontsource/hammersmith-one";
import ProgressBar from "@ramonak/react-progress-bar";
import React, { useState } from "react";
import { AiOutlineSearch } from "react-icons/ai";
import { BsStars } from "react-icons/bs";
import { SiAmazon, SiFlipkart } from "react-icons/si";

const colors = {
  black: "#2E2E2E",
  purple: "#A855F7",
};

const ProductCard = ({ analysisResult, platformName }) => {
  return (
    <div className="bg-white w-full max-w-[730px] p-6 flex flex-col rounded-3xl drop-shadow-2xl justify-center border gap-10 items-start h-full">
      {/* logo */}

      <div className="flex flex-row w-full justify-between">
        <div>
          {platformName === "amazon" ? (
            <SiAmazon size={30} className="mr-2" />
          ) : (
            <SiFlipkart size={30} className="mr-2" />
          )}
        </div>
        <div className="relative">
          {analysisResult.autoMatch ? (
            <>
              <span className="tag-automatch flex flex-row items-center border rounded-xl border-purple-500 px-2 py-1">
                <BsStars color={colors.purple} />{" "}
                <b className="ml-2">Auto-Matched</b>
              </span>
              <div className="tooltip">
                This product was automatically matched based on the other
                platform! Manually enter a link above for more accurate results.
              </div>
            </>
          ) : (
            ""
          )}
        </div>
      </div>

      {/* product image and rating bar */}

      <div className="flex flex-col justify-center items-center  gap-10 w-full">
        <div className="bg-white rounded-xl w-full h-[400px] items-center flex justify-center">
          <img
            src={analysisResult.product_data.product_image_url}
            alt="product"
            className=" rounded-md w-[400px] mx-auto"
          />
        </div>
        <h1 className="font-bold uppercase text-slate-500 text-lg text-center">
          {analysisResult.product_data.product_name}
        </h1>
        <div className="w-3/4 self-start">
          <label className="text-lg font-semibold"> Platform rating</label>
          <ProgressBar
            className="mt-4"
            height="30px"
            bgColor="gray"
            completed={analysisResult.product_data.product_rating}
            maxCompleted={5}
          />
        </div>
        <div className="w-3/4 self-start space-y-3">
          <label className="text-lg font-semibold">Sentiment Rating</label>
          <ProgressBar
            className="mt-4"
            height="30px"
            bgColor="#a855f7"
            completed={analysisResult.analysis.sentiment_score.toPrecision(2)}
            maxCompleted={5}
          />
        </div>
      </div>

      {/* product review card  */}
      <div className="flex flex-col items-center h-full justify-between gap-10">
        <div className="flex flex-col justify-center  items-start gap-5 ">
          <h1 className="text-2xl font-semibold">Review</h1>
          <p
            dangerouslySetInnerHTML={{
              __html: analysisResult.analysis.tagged_summary,
            }}
            className="p-2 text-base rounded-md text-slate-500"
          ></p>
        </div>
        <div className="flex flex-col justify-center items-start gap-5">
          <h1 className="text-2xl font-semibold">Keywords</h1>
          <div className="p-2 rounded-md w-full font-bold text-green-500">
            {analysisResult.analysis.keywords.length > 0 &&
              analysisResult.analysis.keywords.map((keyword) => {
                return <span className="mr-2">{keyword}</span>;
              })}
          </div>
        </div>
      </div>

      <div className="flex justify-center items-center w-full">
        <a
          href={analysisResult.product_data.product_url}
          className="hover:bg-purple-500 py-2 text-center font-semibold border text-purple-500 border-purple-500 hover:text-white w-1/2 rounded-md my-8 duration-500"
        >
          Go to Product
        </a>
      </div>
    </div>
  );
};

const App = () => {
  let resultObject = {
    product_data: {
      product_name: "",
      product_price: "",
      product_rating: "",
      product_image_url: "",
      product_url: "",
    },
    analysis: {
      sentiment_score: "",
      summary: "",
      keywords: "",
    },
  };
  const [amazonData, setAmazonData] = useState(resultObject);
  const [flipkartData, setFlipkartData] = useState(resultObject);
  const [productURLs, setProductURLs] = useState([
    {
      platform: null,
      link: null,
    },
    {
      platform: null,
      link: null,
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  function handleSubmit(e) {
    setIsLoading(true);

    e.preventDefault();
    console.log(productURLs);

    fetch(
      "http://localhost:5500/analyze?" +
        "platformOne=" +
        (productURLs[0].platform || "") +
        "&urlOne=" +
        (productURLs[0].link ? encodeURIComponent(productURLs[0].link) : "") +
        "&platformTwo=" +
        (productURLs[1].platform || "") +
        "&urlTwo=" +
        (productURLs[1].link ? encodeURIComponent(productURLs[1].link) : "")
    )
      .then((response) => response.json())
      .then((responseJSON) => {
        console.log(responseJSON);
        if (responseJSON.amazon) {
          setAmazonData(responseJSON.amazon);
        }
        if (responseJSON.flipkart) {
          setFlipkartData(responseJSON.flipkart);
        }
        setIsLoading(false);
      })
      .catch(function (err) {
        alert(err);
        setIsLoading(false);
      })
      .catch(function (err) {
        alert(err);
        setIsLoading(false);
      });
  }

  const detectPlatform = (url, index, setProductURLs, productURLs) => {
    const amazonRegex = /amazon/i;
    const flipkartRegex = /flipkart/i;
    let platform = null;
    if (amazonRegex.test(url)) {
      platform = "amazon";
    } else if (flipkartRegex.test(url)) {
      platform = "flipkart";
    }
    const newProductURLs = [...productURLs];
    newProductURLs[index] = {
      ...newProductURLs[index],
      platform,
      link: url,
    };
    setProductURLs(newProductURLs);
  };

  return (
    <form
      className="m-5"
      onSubmit={(e) => handleSubmit(e)}
      style={{ color: `${colors.black} !important` }}
    >
      {/*search area*/}
      <div className="">
        <div className="max-w-[1040px] mx-auto">
          <div className="flex justify-between items-center p-2">
            <div className="flex justify-center items-center gap-2">
              <AiOutlineSearch color={colors.purple} size={30} />
              <h1
                className="font-bold text-xl md:text-2xl"
                style={{ fontFamily: "Hammersmith One" }}
              >
                ReView
              </h1>
            </div>
            <ul className="flex justify-center items-center gap-5">
              <a href="#about" className="text-gray-500 hover:text-black">
                <li className="text-xl">About</li>
              </a>
              <a href="#contact" className="text-gray-500 hover:text-black">
                <li className="text-xl">Contact Us</li>
              </a>
            </ul>
          </div>
        </div>

        {/* Home  page */}

        <div
          className={
            onsubmit
              ? "hidden"
              : "h-[700px] flex flex-col max-w-[800px] mx-auto justify-center items-center gap-2"
          }
        >
          <div className="flex flex-col justify-center items-center gap-3">
            <h1 className=" sm:text-3xl text-5xl font-bold text-center">
              Get <span className="text-purple-500">dynamic</span> and{" "}
              <span className="text-purple-500">unbiased</span> review insights!
            </h1>
            <p className="sm:text-sm text-xl sm:w-[500px] text-center text-slate-500">
              Enter any one product link below to get started. You can enter
              both for more accuracy!
            </p>
          </div>
          <div className="w-full p-2 space-y-4 mt-4">
            <div className="flex justify-center items-center p-3 w-full border shadow-md  rounded-md">
              {productURLs[0].platform === "amazon" ? (
                <SiAmazon size={30} className="mr-2" />
              ) : (
                <SiFlipkart
                  size={30}
                  className="mr-2 text-yellow-400 rounded-md bg-blue-500"
                />
              )}
              <input
                type="text"
                name="urlAmz"
                className="w-full focus:outline-none"
                onChange={(event) =>
                  detectPlatform(
                    event.target.value,
                    0,
                    setProductURLs,
                    productURLs
                  )
                }
                value={productURLs[0].link}
              />
            </div>
            <div className="flex justify-center items-center p-3 w-full border shadow-md  rounded-md">
              {productURLs[1].platform === "amazon" ? (
                <SiAmazon size={30} className="mr-2" />
              ) : (
                <SiFlipkart
                  size={30}
                  className="mr-2 text-yellow-400 rounded-md bg-blue-500"
                />
              )}
              <input
                type="text"
                name="urlFlp"
                className="w-full focus:outline-none"
                onChange={(event) =>
                  detectPlatform(
                    event.target.value,
                    1,
                    setProductURLs,
                    productURLs
                  )
                }
                value={productURLs[1].link}
              />
            </div>
            <div className="flex justify-center items-center p-7">
              <div></div>
              <button
                className={`${
                  isLoading ? "" : "py-2"
                } md:w-1/4 w-1/2 text-2xl bg-purple-500 rounded-full text-white shadow-md shadow-purple-400 hover:text-3xl transition-all 300ms flex items-center justify-center`}
                type="submit"
              >
                {isLoading ? <div class="lds-dual-ring"></div> : "Generate"}
              </button>
            </div>
          </div>
        </div>

        {!isLoading && (
          <>
            {/* product page */}
            <div className="flex mt-10 flex-col justify-around lg:flex-row gap-4">
              {/* Amazon product page */}
              {amazonData.product_data.product_name && (
                <ProductCard
                  analysisResult={amazonData}
                  platformName="amazon"
                />
              )}

              {/* Flipkart product page */}
              {flipkartData.product_data.product_name && (
                <ProductCard
                  analysisResult={flipkartData}
                  platformName="flipkart"
                />
              )}
            </div>
          </>
        )}
      </div>
    </form>
  );
};

export default App;
