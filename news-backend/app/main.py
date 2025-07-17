from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import feedparser
import requests
from datetime import datetime, timedelta
import random
from typing import List, Dict
from pydantic import BaseModel

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class NewsItem(BaseModel):
    title: str
    summary: str
    published: str
    source: str
    url: str
    image_url: str
    category: str = "経済"

class NewsResponse(BaseModel):
    success: bool
    data: List[NewsItem]
    count: int
    generated_at: str
    overall_summary: str

def get_news_related_image(title: str) -> str:
    """Get a relevant illustration/image URL based on news title with comprehensive keyword matching"""
    title_lower = title.lower()
    
    if any(keyword in title_lower for keyword in ['m谷', 'mizutani', 'cro']):
        if any(keyword in title_lower for keyword in ['ゴシップ', '口論', '騒動', '疑惑', '小競り合い', '問題', '合コン']):
            return "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=300&fit=crop"  # 議論・問題のイラスト
        elif any(keyword in title_lower for keyword in ['プロレス', '講演', 'スポーツ', 'イベント', '観戦']):
            return "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop"  # スポーツイベント
        elif any(keyword in title_lower for keyword in ['表彰', '振興', '地域', '活動', '貢献']):
            return "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=400&h=300&fit=crop"  # 表彰・地域活動
        else:
            return "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop"  # ビジネスマン
    
    elif any(keyword in title_lower for keyword in ['中国', '日本産', '輸入', '許可', '水産物', 'マグロ', 'ホタテ', '貿易', '国際']):
        return "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop"  # 魚・水産物
    
    elif any(keyword in title_lower for keyword in ['広島', '核実験', 'カザフスタン', '知事', '平和', '核', '原爆']):
        return "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop"  # 平和記念碑
    
    elif any(keyword in title_lower for keyword in ['タイ', '僧侶', '性的', '金銭', '脅し', '宗教', '社会', '寺院']):
        return "https://images.unsplash.com/photo-1563789031959-4c02bcb41319?w=400&h=300&fit=crop"  # 寺院・宗教建築
    
    elif any(keyword in title_lower for keyword in ['相撲', '横綱', '大の里', '名古屋場所', '格闘技', '力士']):
        return "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=300&fit=crop"  # 相撲・格闘技
    
    elif any(keyword in title_lower for keyword in ['クマ', '目撃', 'ゴルフ', '無観客', '野生動物', '宮城', '富谷', '動物']):
        return "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400&h=300&fit=crop"  # ゴルフ場・自然
    
    elif any(keyword in title_lower for keyword in ['株価', '株式', '投資', '市場', '日経', 'ダウ', '証券', 'nikkei', '金融']):
        return "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400&h=300&fit=crop"  # 株式チャート
    
    elif any(keyword in title_lower for keyword in ['マンション', '不動産', '住宅', '建設', '土地', '建物']):
        return "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400&h=300&fit=crop"  # 建物・不動産
    
    elif any(keyword in title_lower for keyword in ['セブン', 'コンビニ', '小売', '売上', '消費', '店舗', '販売']):
        return "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=300&fit=crop"  # 店舗・小売
    
    elif any(keyword in title_lower for keyword in ['自動車', '車', 'トヨタ', 'ホンダ', '日産', 'ev', '電気自動車', '交通']):
        return "https://images.unsplash.com/photo-1549924231-f129b911e442?w=400&h=300&fit=crop"  # 自動車
    
    elif any(keyword in title_lower for keyword in ['ai', '人工知能', 'it', 'テクノロジー', 'デジタル', 'ソフトウェア', 'アプリ', 'システム']):
        return "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop"  # テクノロジー
    
    elif any(keyword in title_lower for keyword in ['銀行', '融資', '金利', '円安', '円高', '為替', '通貨']):
        return "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400&h=300&fit=crop"  # 金融
    
    elif any(keyword in title_lower for keyword in ['エネルギー', '電力', '石油', 'ガス', '原油', '再生可能', '発電']):
        return "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=400&h=300&fit=crop"  # エネルギー
    
    elif any(keyword in title_lower for keyword in ['製造', '工場', '生産', '輸出', '輸入', '産業', '機械']):
        return "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400&h=300&fit=crop"  # 製造業
    
    elif any(keyword in title_lower for keyword in ['航空', '旅行', '観光', 'ana', 'jal', 'ホテル', '空港']):
        return "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400&h=300&fit=crop"  # 航空・旅行
    
    elif any(keyword in title_lower for keyword in ['食品', '農業', '農産物', '食料', 'レストラン', '飲食', '料理']):
        return "https://images.unsplash.com/photo-1542838132-92c53300491e?w=400&h=300&fit=crop"  # 食品・農業
    
    elif any(keyword in title_lower for keyword in ['医療', '製薬', '病院', '薬', 'ワクチン', '治療', '健康']):
        return "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400&h=300&fit=crop"  # 医療
    
    elif any(keyword in title_lower for keyword in ['政府', '政策', '税', '規制', '法律', '国会', '政治']):
        return "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=400&h=300&fit=crop"  # 政府・政策
    
    elif any(keyword in title_lower for keyword in ['教育', '学校', '大学', '学生', '授業', '研究']):
        return "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&h=300&fit=crop"  # 教育
    
    elif any(keyword in title_lower for keyword in ['環境', '気候', '温暖化', 'co2', '排出', '自然']):
        return "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=300&fit=crop"  # 環境・自然
    
    elif any(keyword in title_lower for keyword in ['企業', '会社', 'ビジネス', '業績', '決算', '売上', '経営']):
        return "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400&h=300&fit=crop"  # ビジネス
    
    elif any(keyword in title_lower for keyword in ['スポーツ', '試合', '選手', '競技', 'オリンピック']):
        return "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400&h=300&fit=crop"  # スポーツ一般
    
    elif any(keyword in title_lower for keyword in ['映画', '音楽', '芸能', '文化', 'アート', '展示']):
        return "https://images.unsplash.com/photo-1489824904134-891ab64532f1?w=400&h=300&fit=crop"  # エンターテイメント
    
    else:
        return "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&h=300&fit=crop"  # 一般的な経済ニュース

def get_news_category(title: str) -> str:
    """Determine news category based on title content"""
    title_lower = title.lower()
    
    if any(keyword in title_lower for keyword in ['野球', 'サッカー', 'テニス', 'ゴルフ', '相撲', 'スポーツ', '横綱', '選手', '試合', '勝利', '敗北', 'プロ野球', 'jリーグ', 'オリンピック', '大会', '競技']):
        return "スポーツ"
    
    elif any(keyword in title_lower for keyword in ['政治', '政府', '首相', '大臣', '国会', '選挙', '政策', '法案', '議員', '党', '内閣', '官房']):
        return "政治"
    
    elif any(keyword in title_lower for keyword in ['中国', '韓国', 'アメリカ', 'ロシア', '北朝鮮', '台湾', '外交', '国際', '大使', '首脳', '会談', '条約', '貿易摩擦']):
        return "国際"
    
    elif any(keyword in title_lower for keyword in ['ai', '人工知能', 'it', 'テクノロジー', 'デジタル', 'ソフトウェア', 'アプリ', 'システム', 'ネット', 'インターネット', 'スマホ', 'コンピュータ']):
        return "テクノロジー"
    
    elif any(keyword in title_lower for keyword in ['社会', '事件', '事故', '災害', '地震', '台風', '火災', '犯罪', '逮捕', '裁判', '判決', '宗教', '僧侶', '寺院']):
        return "社会"
    
    elif any(keyword in title_lower for keyword in ['医療', '病院', '薬', '治療', '患者', '医師', '看護', '健康', 'ワクチン', '感染', 'コロナ', '新型', 'インフルエンザ']):
        return "医療"
    
    elif any(keyword in title_lower for keyword in ['環境', '気候', '温暖化', '科学', '研究', '実験', '発見', '宇宙', '原発', '核', '平和', '原爆']):
        return "科学・環境"
    
    elif any(keyword in title_lower for keyword in ['芸能', '映画', '音楽', 'テレビ', 'ドラマ', 'アニメ', '俳優', '歌手', 'タレント', 'アイドル', 'コンサート']):
        return "エンタメ"
    
    elif any(keyword in title_lower for keyword in ['交通', '電車', '新幹線', '航空', '空港', '道路', '自動車', 'バス', '運輸', '鉄道']):
        return "交通"
    
    elif any(keyword in title_lower for keyword in ['教育', '学校', '大学', '学生', '入試', '受験', '授業', '教師', '先生', '学習']):
        return "教育"
    
    else:
        return "経済"

def generate_mizutani_article() -> NewsItem:
    """Generate a fictional article about M谷"""
    is_gossip = random.randint(1, 3) == 1
    
    if is_gossip:
        titles = [
            "CRO勤務のM谷氏、荒川区の居酒屋で同僚と口論騒動",
            "元ハンドボール選手のM谷氏、プロレス観戦中にファンと小競り合い",
            "M谷氏（36）、既婚者でありながら合コン参加疑惑が浮上"
        ]
        summaries = [
            "荒川区内の居酒屋で、CRO勤務のM谷氏（36歳、183cm、95kg）が同僚との飲み会中に口論となり、店内が騒然となった。学生時代にハンドボールで鍛えた体格を活かした威圧的な態度が問題視されている。既婚者である同氏の行動に、周囲からは疑問の声が上がっている。店側は「今後の来店をお断りする」とコメント。",
            "都内のプロレス会場で、M谷氏（36歳、CRO勤務）が他の観客と小競り合いを起こした。身長183cm、体重95kgの同氏が学生時代のハンドボール経験を活かした体格で威圧したとされる。荒川区在住の既婚者である同氏の行動に、プロレスファンからは「マナー違反」との声。会場側は警備強化を検討中。",
            "CRO勤務のM谷氏（36歳、荒川区在住）が、既婚者でありながら都内で開催された合コンに参加していた疑惑が浮上。身長183cm、体重95kgの堂々とした体格で学生時代はハンドボール部に所属していた同氏。プロレス好きとしても知られるが、今回の行動に関係者は「家庭を大切にすべき」と苦言を呈している。"
        ]
        category = "ゴシップ"
    else:
        titles = [
            "CRO業界のエキスパートM谷氏、新薬開発プロジェクトで大きな成果",
            "元ハンドボール選手のM谷氏、地域スポーツ振興で表彰される",
            "M谷氏、プロレス愛好家として地域イベントで講演活動"
        ]
        summaries = [
            "CRO勤務のM谷氏（36歳、荒川区在住）が担当する新薬開発プロジェクトが大きな進展を見せている。身長183cm、体重95kgの堂々とした体格で、学生時代にハンドボールで培った集中力と持久力を業務に活かしている。既婚者として家庭も大切にしながら、プロレス観戦で息抜きをする同氏の働きぶりが業界内で高く評価されている。",
            "荒川区在住のM谷氏（36歳、CRO勤務）が、地域の青少年スポーツ振興活動で表彰された。学生時代にハンドボール部で活躍した経験を活かし、地域の子どもたちに指導を行っている。身長183cm、体重95kgの体格を活かした熱心な指導ぶりが評価され、既婚者として家庭と両立させながらの社会貢献活動が注目を集めている。",
            "プロレス愛好家として知られるM谷氏（36歳、CRO勤務、荒川区在住）が、地域イベントでプロレスの魅力について講演を行った。身長183cm、体重95kgの体格で学生時代はハンドボール部に所属していた同氏。既婚者として家庭を大切にしながら、趣味のプロレス観戦を通じて得た人生哲学を地域住民に伝える活動が好評を博している。"
        ]
        category = "地域"
    
    title = random.choice(titles)
    summary = random.choice(summaries)
    
    if len(summary) > 280:
        sentences = summary.split('。')
        truncated = ""
        for sentence in sentences:
            if len(truncated + sentence + '。') <= 280:
                truncated += sentence + '。'
            else:
                break
        if truncated and len(truncated) > 150:
            summary = truncated
        else:
            if len(summary) > 280:
                last_space = summary[:280].rfind(' ')
                if last_space > 200:
                    summary = summary[:last_space] + "。"
                else:
                    summary = summary[:280]
    
    return NewsItem(
        title=title,
        summary=summary,
        published=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        source="地域ニュース",
        url="https://example.com/mizutani-news",
        image_url=get_news_related_image(title),
        category=category
    )

def fetch_rss_news() -> List[NewsItem]:
    """Fetch news from RSS feeds"""
    rss_feeds = [
        "https://www3.nhk.or.jp/rss/news/cat6.xml",
        "https://www3.nhk.or.jp/rss/news/cat7.xml",
        "https://asia.nikkei.com/rss/feed/nar",
        "https://news.yahoo.co.jp/rss/topics/business.xml",
    ]
    
    news_items = []
    
    for feed_url in rss_feeds:
        try:
            feed = feedparser.parse(feed_url)
            source = "Yahoo!ニュース" if "yahoo" in feed_url else "NHKニュース"
            
            for entry in feed.entries[:3]:
                title = entry.title
                summary = entry.get('summary', entry.get('description', ''))
                
                if len(summary) > 300:
                    sentences = summary.split('。')
                    truncated = ""
                    for sentence in sentences:
                        if len(truncated + sentence + '。') <= 280:
                            truncated += sentence + '。'
                        else:
                            break
                    if truncated and len(truncated) > 100:
                        summary = truncated
                    else:
                        words = summary[:280].split()
                        summary = ' '.join(words[:-1]) if len(words) > 1 else summary[:280]
                elif len(summary) < 50:
                    if len(summary) > 260:
                        summary = summary[:257] + "..."
                    elif len(summary) < 50:
                        summary = f"{summary} {title}に関する詳細情報です。"
                        if len(summary) > 260:
                            summary = summary[:257] + "..."
                
                category = get_news_category(title)
                
                news_item = NewsItem(
                    title=title,
                    summary=summary,
                    published=entry.get('published', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    source=source,
                    url=entry.get('link', ''),
                    image_url=get_news_related_image(title),
                    category=category
                )
                news_items.append(news_item)
                
        except Exception as e:
            print(f"Error fetching from {feed_url}: {e}")
            continue
    
    return news_items

def generate_overall_summary(news_items: List[NewsItem]) -> str:
    """Generate a 500-character overall summary based on actual collected news"""
    sources = list(set([item.source for item in news_items]))
    mizutani_count = len([item for item in news_items if "M谷" in item.title])
    real_news = [item for item in news_items if "M谷" not in item.title]
    
    summary = f"本日収集した{len(news_items)}件のニュースをお届けします。"
    
    if real_news:
        topics = []
        for item in real_news[:3]:  # Use first 3 real news items
            if any(keyword in item.title for keyword in ['セブン', 'コンビニ', '小売']):
                topics.append("小売業界")
            elif any(keyword in item.title for keyword in ['マンション', '不動産']):
                topics.append("不動産市場")
            elif any(keyword in item.title for keyword in ['株価', '投資']):
                topics.append("株式市場")
            elif any(keyword in item.title for keyword in ['企業', '業績']):
                topics.append("企業業績")
            elif any(keyword in item.title for keyword in ['中国', '輸入', '水産物', '貿易']):
                topics.append("国際貿易")
            elif any(keyword in item.title for keyword in ['広島', '核', '平和']):
                topics.append("平和・核問題")
            elif any(keyword in item.title for keyword in ['相撲', 'スポーツ', '横綱']):
                topics.append("スポーツ")
            elif any(keyword in item.title for keyword in ['宗教', '僧侶', '社会']):
                topics.append("社会問題")
            else:
                topics.append("経済動向")
        
        if topics:
            unique_topics = list(set(topics))
            summary += f"主要トピックは{', '.join(unique_topics[:2])}などです。"
    
    if mizutani_count > 0:
        summary += f"また、注目の人物M谷氏の動向も含まれています。"
    
    summary += f"情報源は{', '.join(sources)}などの信頼できるメディアからお届けしています。"
    
    if len(summary) > 500:
        summary = summary[:497] + "..."
    
    return summary

@app.get("/api/news", response_model=NewsResponse)
async def get_news():
    """Get latest TOP6 news including Mizutani articles"""
    try:
        rss_news = fetch_rss_news()
        mizutani_article = generate_mizutani_article()
        
        selected_news = rss_news[:5] + [mizutani_article]
        
        if len(selected_news) < 6:
            remaining_rss = rss_news[5:6]
            selected_news.extend(remaining_rss)
        
        selected_news = selected_news[:6]
        
        overall_summary = generate_overall_summary(selected_news)
        
        return NewsResponse(
            success=True,
            data=selected_news,
            count=len(selected_news),
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            overall_summary=overall_summary
        )
        
    except Exception as e:
        return NewsResponse(
            success=False,
            data=[],
            count=0,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            overall_summary="ニュースの取得中にエラーが発生しました。"
        )

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
