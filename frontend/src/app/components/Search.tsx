"use client";
import { topicMap } from "@/consts";
import { useState } from "react";
import { Article } from "@/types";
import axios from "axios";
import Articles from "./Articles";
import Constituency from "./Constituency";

const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL;

const Search = () => {
  const [selectedTopic, setSelectedTopic] = useState<string>("pick");
  const [constituency, setConstituency] = useState("");
  const [articles, setArticles] = useState<Article[]>([]);
  // BUG! first selection is null
  const handleTopicChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedTopic(event.target.value);
  };

  const appendTerm = async (constituencyUrl: string, term: string) => {
    console.log(`Searching for ${term}`);
    const response = await axios.get(`${constituencyUrl}${term}`);
    setArticles([...articles, ...response.data]);
  };

  const getArticles = (topic: string, constituency: string) => {
    if (!topic || !constituency) return [];
    console.log(`Searching for ${topic} in ${constituency}`);
    const constituencyUrl = `${BASE_URL}/search?constituency=${constituency}&topic=`;
    setArticles([]);
    const terms = topicMap[topic];
    terms.map((term) => appendTerm(constituencyUrl, term));
  };

  return (
    <>
      <div className="border-1 flex flex-col lg:flex-row justify-normal gap-4 m-4 lg:m-10 w-80 lg:w-full">
        <label className="gap-2">Constituency</label>
        <Constituency className="grow" onSelect={setConstituency} />

        <select
          className="select select-bordered w-full max-w-xs"
          value={selectedTopic ?? undefined}
          onChange={handleTopicChange}
        >
          <option value="pick" disabled>
            Pick a topic
          </option>
          {Object.keys(topicMap).map((topic, index) => (
            <option key={index} value={topic}>
              {topic}
            </option>
          ))}
        </select>
        <button
          className="btn btn-primary"
          onClick={() => getArticles(selectedTopic as string, constituency)}
        >
          Search
        </button>
      </div>

      <Articles articles={articles} />
    </>
  );
};

export default Search;
