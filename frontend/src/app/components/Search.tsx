"use client";
import { topics } from "@/consts";
import { useState } from "react";
import { Article } from "@/types";
import axios from "axios";
import Articles from "./Articles";
import Constituency from "./Constituency";

const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL;

const Search = () => {
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [articles, setArticles] = useState<Article[]>([]);
  // BUG! first selection is null
  const handleTopicChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedTopic(event.target.value);
  };

  async function getArticles(
    topic: string,
    constituency: string
  ): Promise<Article[]> {
    if (!topic || !constituency) return [];
    console.log(`Searching for ${topic} in ${constituency}`);
    const url = `${BASE_URL}/search?constituency=${constituency}&topic=${topic}`;
    const response = await axios.get(url);
    setArticles(response.data);
    return response.data;
  }

  return (
    <>
      <div className="border-1 flex flex-col lg:flex-row justify-normal gap-4 m-4 lg:m-10 w-80 lg:w-full">
        <label className="gap-2">Constituency</label>
        <Constituency className="grow" onSelect={setSearch} />

        <select
          className="select select-bordered w-full max-w-xs"
          value={selectedTopic ?? undefined}
          onChange={handleTopicChange}
        >
          <option disabled selected>
            Pick a topic
          </option>
          {topics.map((topic, index) => (
            <option key={index} value={topic}>
              {topic}
            </option>
          ))}
        </select>
        <button
          className="btn btn-primary"
          onClick={() => getArticles(selectedTopic as string, search)}
        >
          Search
        </button>
      </div>

      <Articles articles={articles} />
    </>
  );
};

export default Search;
