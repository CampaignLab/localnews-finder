"use client";

import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Image from "next/image";
import Link from "next/link";
import { Article } from "../types";
interface NewsGridProps {
  articles: Article[];
}

export function NewsInterfaceComponent({ articles }: NewsGridProps) {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow"></header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {articles.map((article, index) => (
                <Card key={index} className="overflow-hidden">
                  <CardHeader className="p-0">
                    {article.img && (
                      <Image
                        src={article.img}
                        alt={article.title || "Article image"}
                        width={400}
                        height={300}
                        className="w-full h-48 object-cover"
                      />
                    )}
                  </CardHeader>
                  <CardContent className="p-4">
                    <h2 className="text-xl font-semibold mb-2">{article.title}</h2>
                    <p className="text-sm text-gray-600 mb-4">{article.description}</p>
                    <div className="flex items-center justify-between text-sm text-gray-500">
                      {article.author && <span>{article.author}</span>}
                      {article.date && <span>{article.date}</span>}
                    </div>
                  </CardContent>
                  <CardFooter className="bg-gray-50 px-4 py-3 flex items-center justify-between">
                    {article.source && <Badge variant="secondary">{article.source}</Badge>}
                    {article.link && (
                      <Link
                        href={article.link}
                        className="text-sm font-medium text-blue-600 hover:text-blue-500"
                      >
                        Read more
                      </Link>
                    )}
                  </CardFooter>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
