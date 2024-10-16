'use client'

import NewsGrid from './news-grid'

const articles: Article[] = [
  {
    title: "Breaking News: Important Event Occurs",
    description: "An important event has occurred that will impact many people.",
    source: "Reliable News Network",
    date: "2023-06-15",
    link: "https://example.com/news/1",
    img: "/placeholder.svg?height=200&width=400",
    author: "Jane Doe",
    searchTerm: "Current Events"
  },
  // ... more articles
]

export function Page() {
  return (
    <main>
      <NewsGrid articles={articles} />
    </main>
  )
}