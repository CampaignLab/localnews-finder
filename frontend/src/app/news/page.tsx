import React from "react";
import { NewsInterfaceComponent } from "../../components/news-interface";
import SearchComponent from "../../components/search";
interface Article {
  title?: string;
  description?: string;
  source?: string;
  content?: string;
  date?: string;
  link?: string;
  img?: string;
  author?: string;
  searchTerm?: string;
}

const articles: Article[] = [
  {
    title: "New AI Breakthrough in Natural Language Processing",
    description:
      "Researchers have developed a new AI model that significantly improves natural language understanding and generation.",
    source: "Tech Daily",
    date: "2023-05-15",
    link: "https://example.com/ai-breakthrough",
    img: "https://picsum.photos/seed/ai/400/300",
    author: "Jane Doe",
  },
  {
    title: "Global Climate Summit Concludes with New Agreements",
    description:
      "World leaders have reached new agreements on reducing carbon emissions and promoting renewable energy sources.",
    source: "World News Network",
    date: "2023-05-14",
    link: "https://example.com/climate-summit",
    img: "https://picsum.photos/seed/climate/400/300",
    author: "John Smith",
  },
  {
    title: "SpaceX Successfully Launches New Satellite Constellation",
    description:
      "SpaceX has successfully launched a new batch of satellites, expanding its global internet coverage.",
    source: "Space Today",
    date: "2023-05-13",
    link: "https://example.com/spacex-launch",
    img: "https://picsum.photos/seed/space/400/300",
    author: "Emily Johnson",
  },
  {
    title: "Major Breakthrough in Quantum Computing",
    description:
      "Scientists announce a significant advancement in quantum computing, bringing us closer to practical applications.",
    source: "Science Weekly",
    date: "2023-05-12",
    link: "https://example.com/quantum-breakthrough",
    img: "https://picsum.photos/seed/quantum/400/300",
    author: "Michael Brown",
  },
  {
    title: "New Study Reveals Benefits of Mediterranean Diet",
    description:
      "A comprehensive study highlights the long-term health benefits of adhering to a Mediterranean diet.",
    source: "Health Journal",
    date: "2023-05-11",
    link: "https://example.com/mediterranean-diet",
    img: "https://picsum.photos/seed/diet/400/300",
    author: "Sarah Wilson",
  },
  {
    title: "Tech Giants Announce Collaboration on AR/VR Standards",
    description:
      "Major technology companies have agreed to collaborate on developing standards for augmented and virtual reality technologies.",
    source: "Tech Insider",
    date: "2023-05-10",
    link: "https://example.com/ar-vr-standards",
    img: "https://picsum.photos/seed/arvr/400/300",
    author: "David Lee",
  },
];
const NewsArticles = () => {
  return (
    <>
      <SearchComponent />
      <NewsInterfaceComponent articles={articles} />
    </>
  );
};

export default NewsArticles;
