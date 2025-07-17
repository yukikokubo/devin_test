import { useState, useEffect } from 'react'
import { RefreshCw, Clock, ExternalLink } from 'lucide-react'
import './App.css'

interface NewsItem {
  title: string
  summary: string
  published: string
  source: string
  url: string
  image_url: string
  category: string
}

interface NewsResponse {
  success: boolean
  data: NewsItem[]
  count: number
  generated_at: string
  overall_summary: string
}

function App() {
  const [news, setNews] = useState<NewsItem[]>([])
  const [overallSummary, setOverallSummary] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [lastUpdated, setLastUpdated] = useState<string>('')

  const fetchNews = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/news`)
      const data: NewsResponse = await response.json()
      
      if (data.success) {
        setNews(data.data)
        setOverallSummary(data.overall_summary)
        setLastUpdated(data.generated_at)
      }
    } catch (error) {
      console.error('ニュースの取得に失敗しました:', error)
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  const handleRefresh = () => {
    setRefreshing(true)
    fetchNews()
  }

  useEffect(() => {
    fetchNews()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">ニュースを読み込み中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-gray-900">最新ニュース TOP6</h1>
              <div className="flex items-center text-sm text-gray-500">
                <Clock className="w-4 h-4 mr-1" />
                <span>最終更新: {lastUpdated}</span>
              </div>
            </div>
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
              <span>{refreshing ? '更新中...' : 'ニュース更新'}</span>
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Overall Summary */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">本日のニュース概要</h2>
          <p className="text-gray-700 leading-relaxed">{overallSummary}</p>
        </div>

        {/* News Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {news.map((item, index) => (
            <article
              key={index}
              className="bg-white rounded-xl shadow-sm border hover:shadow-md transition-shadow duration-200"
            >
              {/* Thumbnail */}
              <div className="aspect-video bg-gray-200 rounded-t-xl overflow-hidden">
                <img
                  src={item.image_url}
                  alt={item.title}
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-200"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement
                    target.src = 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&h=300&fit=crop'
                  }}
                />
              </div>

              {/* Content */}
              <div className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="inline-block px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">
                    {item.category}
                  </span>
                  <span className="text-xs text-gray-500">{item.source}</span>
                </div>

                <h3 className="font-semibold text-gray-900 mb-3 line-clamp-2 leading-tight">
                  {item.title}
                </h3>

                <p className="text-sm text-gray-600 mb-4 leading-relaxed">
                  {item.summary}
                </p>

                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-500">
                    {new Date(item.published).toLocaleDateString('ja-JP')}
                  </span>
                  {item.url && item.url !== 'https://example.com/mizutani-news' && item.url !== 'https://example.com/economic-news' && (
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center text-xs text-blue-600 hover:text-blue-800 transition-colors"
                    >
                      <span>詳細を見る</span>
                      <ExternalLink className="w-3 h-3 ml-1" />
                    </a>
                  )}
                </div>
              </div>
            </article>
          ))}
        </div>
      </main>
    </div>
  )
}

export default App
