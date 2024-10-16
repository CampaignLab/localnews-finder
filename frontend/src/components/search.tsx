"use client";
import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Article } from "../types";
import axios from "axios";
import { topics } from "@/consts";
export default function SearchComponent() {
  const [selectedTopic, setSelectedTopic] = useState<string>("pick");
  const [constituency, setConstituency] = useState("");
  const [articles, setArticles] = useState<Article[]>([]);
  // BUG! first selection is null
  const handleTopicChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedTopic(event.target.value);
  };
  const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL;
  const appendTerm = async (constituency: string, term: string) => {
    console.log(`Searching for ${term}`);
    const url = `${BASE_URL}/search?constituency=${constituency}&topic=${encodeURIComponent(term)}`;
    try {
      const response = await axios.get(url);
      console.log(`Found ${response.data.length} articles for ${constituency} ${term}.`);
      if (response.data?.length > 0) {
        setArticles((prevArticles) => [...prevArticles, ...response.data]);
      }
    } catch (error) {
      console.error(`Error fetching articles: ${error}`);
    }
  };

  const getArticles = (topic: string, constituency: string) => {
    if (!topic || !constituency) return [];
    setArticles([]);
    appendTerm(constituency, topic);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex flex-col sm:flex-row gap-4 items-end">
        <div className="flex-1 min-w-[200px]">
          <label htmlFor="constituency" className="block text-sm font-medium text-gray-700 mb-1">
            Constituency
          </label>
          <Input id="constituency" placeholder="Enter constituency..." />
        </div>
        <div className="w-full sm:w-[200px]">
          <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-1">
            Topic
          </label>
          <Select>
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
        <Button onClick={() => getArticles(selectedTopic as string, constituency)} className="px-8">
          Search
        </Button>
      </div>
    </div>
  );
}
