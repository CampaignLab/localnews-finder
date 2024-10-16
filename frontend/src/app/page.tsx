"use client";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import React, { useState } from "react";
import Search from "../components/Search";
import News from "../components/NewsGrid";
import { Article } from "../types";
export default function Home() {
  const [articles, setArticles] = useState<Article[]>([]);

  return (
    <div className="h-screen flex flex-col">
      <Navbar />
      <div className="flex flex-grow overflow-y-auto">
        <main className="flex-grow pl-20 pr-20">
          <h1>Local News Finder</h1>
          <div className="divider divider-neutral"></div>
          <Search setArticles={setArticles} />
          <News articles={articles} />
        </main>
      </div>
      <Footer />
    </div>
  );
}
