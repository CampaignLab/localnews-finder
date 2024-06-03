import Image from "next/image";
import { Article } from "@/types";
type ArticlesProps = {
  articles: Article[];
};

const Articles: React.FC<ArticlesProps> = ({ articles }) => {
  const getFullUrl = (url: string) => {
    if (!/^https?:\/\//i.test(url)) {
      return `http://${url}`;
    }
    return url;
  };
  return (
    <div className="w-80 lg:w-full">
      {articles.map((article) => (
        <div
          key={article.title}
          className="collapse collapse-arrow bg-base-200 mb-4"
        >
          <input type="radio" name="my-accordion-2" defaultChecked />
          <div className="collapse-title text-xl font-medium">
            <a href={article.link}>{article.title}</a>
          </div>
          <div className="collapse-content">
            <p>{article.description}</p>
            <p>Source: {article.source}</p>
            <p>Date: {article.date}</p>
            <p>
              Link:{" "}
              <a
                href={getFullUrl(article.link || "")}
                target="_blank"
                rel="noopener noreferrer"
              >
                {article.link}
              </a>
            </p>
            <p>
              {article.img && (
                <p>
                  <Image
                    src={`https://${article.img}` || ""}
                    alt={article.title || "Article image"}
                    height={100}
                    width={100}
                  />
                </p>
              )}
            </p>
            <p>Author: {article.author}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Articles;
