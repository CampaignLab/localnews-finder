"use client";
import { topics } from "@/consts";
import { useState } from "react";
import { Article } from "@/types";
import axios from "axios";

const Search = () => {
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  const handleTopicChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    console.log(handleSearchChange);
    setSelectedTopic(event.target.value);
  };

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(event.target.value);
  };

  async function getArticles(topic: string, town: string): Promise<Article[]> {
    const url = `localhost:3000/api/articles?topic=${topic}&town=${town}`;
    const response = await axios.get(url);
    return response.data;
  }

  function autoComplete() {}

  return (
    <div className="flex flex-col lg:flex-row justify-normal gap-4 m-4 lg:m-10 w-80 lg:w-full">
      <label className="input input-bordered flex items-center gap-2">
        <input
          type="text"
          className="grow"
          placeholder="Find your Town"
          value={search}
          onChange={handleSearchChange}
        />
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          className="w-4 h-4 opacity-70"
        >
          <path
            fillRule="evenodd"
            d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z"
            clipRule="evenodd"
          />
        </svg>
      </label>

      <select
        className="select select-bordered w-full max-w-xs"
        value={selectedTopic}
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
    </div>
  );
};

export default Search;
