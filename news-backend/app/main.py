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
    """Get a relevant illustration/image URL based on news title with enhanced keyword matching"""
    title_lower = title.lower()
    
    if any(keyword in title_lower for keyword in ['m谷']):
        if any(keyword in title_lower for keyword in ['ゴシップ', '口論', '騒動', '疑惑', '小競り合い', '問題', '合コン', '不倫', 'スキャンダル']):
            return "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=300&fit=crop"  # 議論・問題
        elif any(keyword in title_lower for keyword in ['表彰', '振興', '地域', '活動', '貢献', '成果', '新薬', '開発', 'プロジェクト', 'エキスパート']):
            return "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=400&h=300&fit=crop"  # 表彰・成功
        elif any(keyword in title_lower for keyword in ['プロレス', '観戦', 'スポーツ', 'イベント', 'ハンドボール']):
            return "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop"  # スポーツ
        else:
            return "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop"  # ビジネスマン
    
    elif any(keyword in title_lower for keyword in ['中国', '日本産', '水産物', 'マグロ', 'ホタテ', '輸入', '許可', '449種類']):
        return "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop"  # 魚・水産物
    
    elif any(keyword in title_lower for keyword in ['広島', '湯崎', 'カザフスタン', '核実験場', '跡地', '訪問', '平和', '核']):
        return "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop"  # 平和記念・核関連
    
    elif any(keyword in title_lower for keyword in ['タイ', '僧侶', '性的関係', '金銭', '脅し', '社会衝撃', '宗教', '寺院']):
        return "https://images.unsplash.com/photo-1563789031959-4c02bcb41319?w=400&h=300&fit=crop"  # 寺院・宗教
    
    elif any(keyword in title_lower for keyword in ['プロ野球', '日本ハム', '西武', '連勝', '首位', 'パ・リーグ', '野球']):
        return "https://images.unsplash.com/photo-1566577739112-5180d4bf9390?w=400&h=300&fit=crop"  # 野球
    
    elif any(keyword in title_lower for keyword in ['横綱', '大の里', '相撲', '名古屋場所', '1敗', '力士']):
        return "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=300&fit=crop"  # 相撲
    
    elif any(keyword in title_lower for keyword in ['スポーツ', '試合', '選手', '競技', '勝利', '敗北', '大会', 'オリンピック']):
        return "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400&h=300&fit=crop"  # スポーツ一般
    
    elif any(keyword in title_lower for keyword in ['外交', '国際', '大使', '首脳', '会談', '条約', '貿易摩擦']):
        return "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=400&h=300&fit=crop"  # 外交
    
    elif any(keyword in title_lower for keyword in ['政治', '政府', '首相', '大臣', '国会', '選挙', '政策', '法案', '議員']):
        return "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=400&h=300&fit=crop"  # 政治
    
    elif any(keyword in title_lower for keyword in ['事件', '事故', '犯罪', '逮捕', '裁判', '判決', '社会', '衝撃']):
        return "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=400&h=300&fit=crop"  # 社会問題
    
    elif any(keyword in title_lower for keyword in ['地震', '震災', '災害', '台風', '津波', '火災']):
        return "https://images.unsplash.com/photo-1547036967-23d11aacaee0?w=400&h=300&fit=crop"  # 災害
    
    elif any(keyword in title_lower for keyword in ['科学', '研究', '実験', '発見', '宇宙', '技術']):
        return "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=400&h=300&fit=crop"  # 科学研究
    
    elif any(keyword in title_lower for keyword in ['環境', '気候', '温暖化', 'co2', '排出', '自然', '生態']):
        return "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=300&fit=crop"  # 環境
    
    elif any(keyword in title_lower for keyword in ['ai', '人工知能', 'it', 'テクノロジー', 'デジタル', 'ソフトウェア', 'アプリ']):
        return "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop"  # テクノロジー
    
    elif any(keyword in title_lower for keyword in ['医療', '病院', '薬', '治療', '患者', '医師', '健康', 'ワクチン']):
        return "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400&h=300&fit=crop"  # 医療
    
    elif any(keyword in title_lower for keyword in ['教育', '学校', '大学', '学生', '授業', '研究', '入試', '受験']):
        return "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&h=300&fit=crop"  # 教育
    
    elif any(keyword in title_lower for keyword in ['交通', '電車', '新幹線', '航空', '道路', 'バス', '運輸', '鉄道']):
        return "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400&h=300&fit=crop"  # 交通
    
    elif any(keyword in title_lower for keyword in ['自動車', '車', 'トヨタ', 'ホンダ', '日産', 'ev', '電気自動車']):
        return "https://images.unsplash.com/photo-1549924231-f129b911e442?w=400&h=300&fit=crop"  # 自動車
    
    elif any(keyword in title_lower for keyword in ['株価', '株式', '投資', '市場', '日経', 'ダウ', '証券', '金融', '銀行']):
        return "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400&h=300&fit=crop"  # 金融
    
    elif any(keyword in title_lower for keyword in ['企業', '会社', 'ビジネス', '業績', '決算', '売上', '経営', 'cro']):
        return "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400&h=300&fit=crop"  # ビジネス
    
    elif any(keyword in title_lower for keyword in ['不動産', '住宅', '建設', '建物', 'マンション', '土地']):
        return "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400&h=300&fit=crop"  # 不動産
    
    elif any(keyword in title_lower for keyword in ['小売', '店舗', '販売', '消費', 'コンビニ', '売上']):
        return "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=300&fit=crop"  # 小売
    
    elif any(keyword in title_lower for keyword in ['エネルギー', '電力', '石油', 'ガス', '原油', '発電', '再生可能']):
        return "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=400&h=300&fit=crop"  # エネルギー
    
    elif any(keyword in title_lower for keyword in ['製造', '工場', '生産', '産業', '機械', '輸出', '輸入']):
        return "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400&h=300&fit=crop"  # 製造業
    
    elif any(keyword in title_lower for keyword in ['食品', '農業', '農産物', '食料', '料理', '飲食']):
        return "https://images.unsplash.com/photo-1542838132-92c53300491e?w=400&h=300&fit=crop"  # 食品・農業
    
    elif any(keyword in title_lower for keyword in ['旅行', '観光', 'ホテル', '空港', 'ana', 'jal']):
        return "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400&h=300&fit=crop"  # 旅行
    
    elif any(keyword in title_lower for keyword in ['映画', '音楽', '芸能', 'テレビ', 'ドラマ', 'アニメ', '文化', 'アート']):
        return "https://images.unsplash.com/photo-1489824904134-891ab64532f1?w=400&h=300&fit=crop"  # エンターテイメント
    
    else:
        return "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&h=300&fit=crop"  # 一般ニュース

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
        gossip_articles = [
            {
                "title": "CRO勤務のM谷氏、荒川区の居酒屋で同僚と口論騒動",
                "summary": "荒川区内の居酒屋で、CRO勤務のM谷氏（36歳、183cm、95kg）が同僚との飲み会中に口論となり、店内が騒然となった。学生時代にハンドボールで鍛えた体格を活かした威圧的な態度が問題視されている。既婚者である同氏の行動に、周囲からは疑問の声が上がっている。プロレス好きとしても知られる同氏だが、今回の騒動で職場での立場が危ぶまれている。"
            },
            {
                "title": "元ハンドボール選手のM谷氏、プロレス観戦中にファンと小競り合い",
                "summary": "都内のプロレス会場で、M谷氏（36歳、CRO勤務）が他の観客と小競り合いを起こした。身長183cm、体重95kgの同氏が学生時代のハンドボール経験を活かした体格で威圧したとされる。荒川区在住の既婚者である同氏の行動に、プロレスファンからは「マナー違反」との声。会場スタッフが仲裁に入る事態となり、同氏は途中退場を余儀なくされた。"
            },
            {
                "title": "M谷氏（36）、既婚者でありながら合コン参加疑惑が浮上",
                "summary": "CRO勤務のM谷氏（36歳、荒川区在住）が、既婚者でありながら都内で開催された合コンに参加していた疑惑が浮上。身長183cm、体重95kgの堂々とした体格で学生時代はハンドボール部に所属していた同氏。プロレス好きとしても知られるが、今回の行動に関係者は「家庭を大切にすべき」と苦言を呈している。妻への配慮を欠いた行動として批判が集まっている。"
            },
            {
                "title": "M谷氏、会社の飲み会で後輩に説教し場の空気を悪化させる",
                "summary": "会社の歓送迎会で、M谷氏（36歳、CRO勤務）が新入社員に対して長時間の説教を行い、場の雰囲気を悪化させた。身長183cm、体重95kgの威圧的な体格で、学生時代のハンドボール部での経験を引き合いに出した指導が「パワハラ的」と問題視されている。荒川区在住の既婚者でプロレス好きの同氏だが、職場での振る舞いに同僚からは厳しい視線が向けられている。"
            },
            {
                "title": "CRO勤務のM谷氏、電車内でのマナー違反が目撃される",
                "summary": "JR山手線車内で、M谷氏（36歳、荒川区在住）が大声で電話をしていたところを他の乗客に注意され、逆ギレする場面が目撃された。CRO勤務の同氏は学生時代にハンドボールをしていた体格（183cm、95kg）を活かして威圧的な態度を取ったという。既婚者でプロレス好きとしても知られる同氏の公共マナーの悪さが問題となっている。"
            },
            {
                "title": "M谷氏、荒川区のジムで他の利用者とトラブル発生",
                "summary": "荒川区内のスポーツジムで、M谷氏（36歳、CRO勤務）が器具の独占使用を巡って他の利用者とトラブルになった。身長183cm、体重95kgの体格で学生時代はハンドボール部に所属していた同氏。既婚者でありながらジムでの態度が問題視されている。プロレス好きの同氏が筋トレ器具を長時間占有し、注意されると逆ギレしたとの証言もある。"
            },
            {
                "title": "元ハンドボール部のM谷氏、同窓会で武勇伝を語り続け顰蹙を買う",
                "summary": "学生時代のハンドボール部同窓会で、M谷氏（36歳、CRO勤務、荒川区在住）が自身の武勇伝を延々と語り続け、他の参加者から顰蹙を買った。身長183cm、体重95kgの体格を誇示するような発言も多く、既婚者としての品格が疑問視されている。プロレス好きの話題も交えながら自慢話を続け、同窓生たちは困惑した表情を見せていたという。"
            },
            {
                "title": "M谷氏、プロレス会場で選手に野次を飛ばし注意される",
                "summary": "プロレス観戦中、M谷氏（36歳、荒川区在住）が選手に対して不適切な野次を飛ばし、会場スタッフから注意を受けた。CRO勤務で学生時代はハンドボール部だった同氏の身長183cm、体重95kgの体格が威圧的だったとの証言もある。既婚者でありながらプロレス観戦に熱中しすぎる同氏の行動が、他の観客からも批判を浴びている。"
            },
            {
                "title": "CRO勤務のM谷氏、近所のコンビニで店員に横柄な態度",
                "summary": "荒川区内のコンビニで、M谷氏（36歳、CRO勤務）が店員に対して横柄な態度を取り、他の客から苦情が寄せられた。学生時代にハンドボールで鍛えた身長183cm、体重95kgの体格を活かした威圧的な行動が問題となっている。既婚者でプロレス好きとしても知られる同氏だが、近所での評判は芳しくない状況が続いている。"
            },
            {
                "title": "M谷氏、荒川区の町内会で他の住民と意見対立",
                "summary": "荒川区の町内会で、M谷氏（36歳、CRO勤務）が他の住民と激しい意見対立を起こした。身長183cm、体重95kgの体格で学生時代はハンドボール部に所属していた同氏。既婚者でありながら地域での協調性に欠ける行動が批判されている。プロレス好きの同氏が会議中に大声を出し、他の住民を威圧するような態度を取ったとの証言もある。"
            }
        ]
        selected_article = random.choice(gossip_articles)
        title = selected_article["title"]
        summary = selected_article["summary"]
        category = "ゴシップ"
    else:
        positive_articles = [
            {
                "title": "CRO業界のエキスパートM谷氏、新薬開発プロジェクトで大きな成果",
                "summary": "CRO勤務のM谷氏（36歳、荒川区在住）が担当する新薬開発プロジェクトが大きな進展を見せている。身長183cm、体重95kgの堂々とした体格で、学生時代にハンドボールで培った集中力と持久力を業務に活かしている。既婚者として家庭も大切にしながら、プロレス観戦で息抜きをする同氏の働きぶりが業界内で高く評価されている。"
            },
            {
                "title": "元ハンドボール選手のM谷氏、地域スポーツ振興で表彰される",
                "summary": "荒川区のスポーツ振興に貢献したM谷氏（36歳、CRO勤務）が区から表彰を受けた。学生時代のハンドボール部での経験を活かし、身長183cm、体重95kgの体格で地域の子どもたちにスポーツ指導を行っている。既婚者として家族の理解を得ながら、プロレス好きの一面も持つ同氏の地域貢献活動が高く評価されている。"
            },
            {
                "title": "M谷氏、プロレス愛好家として地域イベントで講演活動",
                "summary": "荒川区の文化センターで開催されたイベントで、M谷氏（36歳、CRO勤務）がプロレスの魅力について講演を行った。身長183cm、体重95kgの体格で学生時代はハンドボール部に所属していた同氏。既婚者として家庭を大切にしながら、趣味のプロレス観戦で得た知識を地域住民と共有する活動が好評を博している。"
            },
            {
                "title": "M谷氏、CRO業界の若手育成プログラムで講師を務める",
                "summary": "CRO業界の人材育成に貢献するM谷氏（36歳、荒川区在住）が、若手社員向けの研修プログラムで講師を務めている。学生時代のハンドボール部でのリーダーシップ経験と、身長183cm、体重95kgの存在感を活かした指導が受講者から好評。既婚者として責任感も強く、プロレス好きの一面も交えた親しみやすい指導スタイルが評価されている。"
            },
            {
                "title": "荒川区在住のM谷氏、地域清掃活動でリーダーシップを発揮",
                "summary": "荒川区の河川清掃活動でリーダーを務めるM谷氏（36歳、CRO勤務）の取り組みが地域で高く評価されている。学生時代のハンドボール部で培ったリーダーシップと、身長183cm、体重95kgの体格を活かした力仕事での貢献が目立っている。既婚者として環境への責任感も強く、プロレス好きの一面を持ちながらも地域のために汗を流す姿勢が住民から感謝されている。"
            },
            {
                "title": "M谷氏、会社の業績向上に貢献し社内表彰を受ける",
                "summary": "CRO業界で活躍するM谷氏（36歳、荒川区在住）が、担当プロジェクトの成功により社内表彰を受けた。身長183cm、体重95kgの堂々とした体格で、学生時代のハンドボール部で培った集中力と粘り強さを業務に活かしている。既婚者として家庭を大切にしながら、プロレス観戦で息抜きをする同氏の働きぶりが同僚からも高く評価されている。"
            },
            {
                "title": "元ハンドボール部のM谷氏、母校で後輩指導にボランティア参加",
                "summary": "母校のハンドボール部でコーチとして活動するM谷氏（36歳、CRO勤務、荒川区在住）の指導が注目されている。身長183cm、体重95kgの体格を活かした実技指導と、現在のCRO業界での経験を踏まえた人生指導が部員たちに好評。既婚者として責任感も強く、プロレス好きの一面も交えた親しみやすい指導スタイルで後輩たちの成長を支えている。"
            },
            {
                "title": "M谷氏、プロレス観戦を通じた地域交流イベントを企画",
                "summary": "プロレス愛好家として知られるM谷氏（36歳、CRO勤務、荒川区在住）が企画した地域交流イベントが大成功を収めた。学生時代のハンドボール部での企画力と、身長183cm、体重95kgの存在感で多くの参加者をまとめ上げた。既婚者として家族の理解を得ながら、趣味のプロレス観戦を通じて地域住民との絆を深める活動が高く評価されている。"
            },
            {
                "title": "CRO勤務のM谷氏、医療業界の発展に寄与する論文を発表",
                "summary": "医療業界の発展に貢献するM谷氏（36歳、荒川区在住、CRO勤務）の研究論文が学会で高く評価されている。学生時代のハンドボール部で培った集中力と、身長183cm、体重95kgの体格に裏打ちされた精神力で研究に取り組んだ成果。既婚者として患者への思いも研究の原動力となっており、プロレス観戦で息抜きをしながらも真摯に医療の未来に向き合っている。"
            }
        ]
        selected_article = random.choice(positive_articles)
        title = selected_article["title"]
        summary = selected_article["summary"]
        category = "地域ニュース"
    
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
