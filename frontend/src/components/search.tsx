"use client";
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import axios from "axios";
import { topics } from "@/consts";
import Constituency from "./Constituency";
import { Article } from "@/types";

interface SearchProps {
  setArticles: (articles: Article[]) => void;
}

const Search = ({ setArticles }: SearchProps) => {
  const [selectedTopic, setSelectedTopic] = useState<string>("");
  const [constituency, setConstituency] = useState("");

  const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL;

  const appendTerm = async (constituency: string, term: string) => {
    console.log(`Searching for ${term}`);
    const url = `${BASE_URL}/search?constituency=${constituency}&topic=${encodeURIComponent(
      term
    )}`;
    try {
      const response = await axios.get(url);
      console.log(
        `Found ${response.data.length} articles for ${constituency} ${term}.`
      );
      if (response.data?.length > 0) {
        setArticles(response.data);
      }
    } catch (error) {
      console.error(`Error fetching articles: ${error}`);
    }
  };

  const getArticles = (topic: string, constituency: string) => {
    if (!topic || !constituency) return;
    appendTerm(constituency, topic);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex flex-col sm:flex-row gap-4 items-end">
        {/* Constituency Input */}
        <div className="flex-1 min-w-[200px]">
          <label
            htmlFor="constituency"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Constituency
          </label>
          {/* Use the Constituency component with autocomplete */}
          <Constituency className="grow" onSelect={setConstituency} />
        </div>

        {/* Topic Selection */}
        <div className="w-full sm:w-[200px]">
          <label
            htmlFor="topic"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Topic
          </label>
          <Select onValueChange={(value) => setSelectedTopic(value)}>
            <SelectTrigger id="topic">
              <SelectValue placeholder="Select a topic" />
            </SelectTrigger>
            <SelectContent>
              {topics.map((topic) => (
                <SelectItem key={topic} value={topic}>
                  {topic}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Search Button */}
        <Button
          onClick={() => getArticles(selectedTopic, constituency)}
          className="px-8"
        >
          Search
        </Button>
      </div>
    </div>
  );
};

export default Search;
