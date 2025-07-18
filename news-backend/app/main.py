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

def generate_fictional_news() -> List[NewsItem]:
    """Generate fictional news articles with diverse categories and content"""
    
    fictional_news_templates = [
        {
            "title": "東京証券取引所、新システム導入で取引効率が30%向上",
            "summary": "東京証券取引所は本日、新しい取引システム「ARROWHEAD-X」の導入を発表しました。このシステムにより、取引処理速度が従来比30%向上し、投資家の利便性が大幅に改善される見込みです。同取引所の田中社長は「デジタル化の推進により、より透明で効率的な市場を提供できる」と述べています。新システムは来月から段階的に運用開始予定で、年内には全面移行を完了する計画です。",
            "category": "経済",
            "source": "経済新聞"
        },
        {
            "title": "大手コンビニチェーン、AI活用で食品ロス50%削減を達成",
            "summary": "セブンイレブンジャパンは、AI技術を活用した需要予測システムにより、食品ロスを前年比50%削減したと発表しました。このシステムは天候、イベント、地域特性などのデータを分析し、各店舗の最適な発注量を算出します。同社の佐藤取締役は「持続可能な社会の実現に向けた重要な一歩」と評価しています。今後は他の商品カテゴリーにも展開し、さらなる効率化を目指すとしています。",
            "category": "経済",
            "source": "流通ニュース"
        },
        {
            "title": "プロ野球、新人王候補の山田選手が月間MVP受賞",
            "summary": "プロ野球パ・リーグの新人王候補として注目される楽天の山田翔太選手（22）が、7月度の月間MVPを受賞しました。打率.385、15本塁打、42打点の好成績を記録し、チームの首位争いに大きく貢献しています。山田選手は「チームメイトのサポートのおかげ。優勝に向けて全力で頑張りたい」とコメント。球団関係者は「将来の日本代表候補」と期待を寄せています。",
            "category": "スポーツ",
            "source": "スポーツ報知"
        },
        {
            "title": "サッカーJ1、FC東京が4連勝で首位浮上",
            "summary": "サッカーJ1リーグで、FC東京が横浜F・マリノスを2-1で破り、4連勝を達成しました。この勝利により勝ち点を65に伸ばし、首位に浮上。エース森田選手の2ゴールが勝利の決め手となりました。長谷川監督は「選手たちの献身的なプレーが実を結んだ。残り試合も気を抜かずに戦いたい」と語っています。次節は川崎フロンターレとのアウェー戦が予定されています。",
            "category": "スポーツ",
            "source": "サッカーマガジン"
        },
        {
            "title": "政府、デジタル庁の予算を来年度20%増額へ",
            "summary": "政府は来年度予算案で、デジタル庁の予算を今年度比20%増の1200億円とする方針を固めました。行政手続きのデジタル化推進や、サイバーセキュリティ強化が主な用途となります。河野デジタル大臣は「国民の利便性向上と行政効率化を両立させる」と説明。野党からは「予算の使途を明確にすべき」との声も上がっており、国会での議論が注目されます。",
            "category": "政治",
            "source": "政治新聞"
        },
        {
            "title": "地方創生担当大臣、過疎地域支援策を発表",
            "summary": "坂本地方創生担当大臣は、過疎地域の活性化を目的とした新たな支援策を発表しました。移住促進のための住宅補助金拡充や、地域企業への税制優遇措置が柱となります。対象は全国約800の過疎自治体で、総額500億円の予算を投じる予定です。大臣は「地方の魅力を活かした持続可能な地域づくりを支援する」と述べ、来年4月からの実施を目指すとしています。",
            "category": "政治",
            "source": "地方行政"
        },
        {
            "title": "日韓首脳会談、経済協力強化で合意",
            "summary": "岸田首相と韓国の尹大統領による日韓首脳会談が東京で開催され、両国の経済協力強化で合意しました。半導体分野での技術協力や、観光業の相互促進が主な内容です。岸田首相は「両国の未来志向的な関係構築に向けた重要な一歩」と評価。尹大統領も「経済分野での協力が両国民の利益につながる」と述べました。次回会談は来年春にソウルで開催予定です。",
            "category": "国際",
            "source": "外交通信"
        },
        {
            "title": "ASEAN諸国、気候変動対策で新たな枠組み設立",
            "summary": "ASEAN（東南アジア諸国連合）は、気候変動対策を強化するための新たな枠組み「ASEAN気候行動パートナーシップ」を設立すると発表しました。再生可能エネルギーの普及促進や、森林保護活動の連携強化が主な目的です。日本も技術支援や資金協力で参画する予定で、外務省は「地域の持続可能な発展に貢献したい」としています。来月バンコクで設立記念会議が開催されます。",
            "category": "国際",
            "source": "国際情報"
        },
        {
            "title": "全国の小学校、プログラミング教育の成果が向上",
            "summary": "文部科学省の調査によると、全国の小学校でのプログラミング教育の成果が着実に向上していることが分かりました。論理的思考力を測るテストで、導入前と比較して平均点が15%上昇。教師の指導力向上や教材の充実が要因とされています。同省の担当者は「デジタル社会に対応できる人材育成が進んでいる」と評価。今後は中学校での発展的な学習内容の検討も進める方針です。",
            "category": "社会",
            "source": "教育新聞"
        },
        {
            "title": "高齢者向けデジタル講座、全国で参加者急増",
            "summary": "総務省が推進する高齢者向けデジタル講座の参加者が、前年比2倍の20万人に達したことが分かりました。スマートフォンの基本操作やオンライン決済の方法などを学ぶ内容で、参加者の満足度も90%を超えています。講座を受講した田中さん（72）は「孫とビデオ通話ができるようになって嬉しい」と話しています。同省は来年度も講座を継続し、デジタルデバイドの解消を目指すとしています。",
            "category": "社会",
            "source": "社会福祉"
        },
        {
            "title": "日本企業、量子コンピューター実用化で世界初の成果",
            "summary": "理化学研究所と富士通の共同研究チームが、量子コンピューターの実用化に向けた世界初の成果を発表しました。従来の計算機では数年かかる複雑な最適化問題を、わずか数分で解決することに成功。物流や金融分野での応用が期待されています。研究チームリーダーの中村教授は「日本の量子技術が世界をリードする証明」と述べています。来年には企業向けサービスの提供開始を予定しています。",
            "category": "テクノロジー",
            "source": "科学技術"
        },
        {
            "title": "自動運転バス、地方都市で本格運用開始",
            "summary": "群馬県前橋市で、自動運転バスの本格運用が開始されました。AI技術により安全性を確保しながら、運転手不足の解決を目指します。初日は市民約200人が試乗し、「スムーズで安心」との声が多く聞かれました。前橋市の山本市長は「地方交通の新たなモデルケースとなる」と期待を表明。他の地方自治体からも導入に向けた問い合わせが相次いでいるということです。",
            "category": "テクノロジー",
            "source": "交通技術"
        },
        {
            "title": "新型がん治療薬、臨床試験で画期的な効果を確認",
            "summary": "国立がん研究センターは、新型がん治療薬「NK-2024」の臨床試験で画期的な効果を確認したと発表しました。従来治療が困難だった進行がんに対し、腫瘍縮小率80%を達成。副作用も従来薬より大幅に軽減されています。研究責任者の佐藤医師は「がん治療の新たな希望となる」と述べています。厚生労働省への承認申請を来年初頭に行い、2026年の実用化を目指すとしています。",
            "category": "医療",
            "source": "医学ジャーナル"
        },
        {
            "title": "AI診断システム、早期認知症発見率を90%に向上",
            "summary": "東京大学医学部の研究チームが開発したAI診断システムが、早期認知症の発見率を90%まで向上させることに成功しました。MRI画像と認知機能テストのデータを組み合わせて分析し、従来の診断法より2年早い発見が可能です。研究チームの田中教授は「早期発見により治療効果が大幅に改善される」と説明。全国の医療機関での導入に向けた準備が進められています。",
            "category": "医療",
            "source": "医療技術"
        },
        {
            "title": "人気アニメ映画、興行収入100億円突破",
            "summary": "今年公開された人気アニメ映画「星空の約束」が、公開から2ヶ月で興行収入100億円を突破しました。美しい映像と感動的なストーリーが話題となり、幅広い年齢層から支持を集めています。監督の鈴木氏は「多くの方に愛される作品になって感謝している」とコメント。海外での配給も決定しており、世界的なヒットが期待されています。関連グッズの売上も好調で、経済効果は200億円を超える見込みです。",
            "category": "エンタメ",
            "source": "エンタメ情報"
        },
        {
            "title": "音楽フェス、3年ぶりの完全開催で20万人が来場",
            "summary": "千葉県で開催された大型音楽フェスティバル「サマーソニック2025」が、3年ぶりの完全開催となり、3日間で延べ20万人が来場しました。国内外の人気アーティスト50組が出演し、会場は熱気に包まれました。主催者は「音楽の力で人々を繋げることができた」と振り返っています。来場者からは「久しぶりの生音楽に感動した」との声が多く聞かれ、来年の開催も決定しています。",
            "category": "エンタメ",
            "source": "音楽情報"
        }
    ]
    
    selected_templates = random.sample(fictional_news_templates, min(15, len(fictional_news_templates)))
    
    all_news_items = []
    
    for template in selected_templates:
        news_item = NewsItem(
            title=template["title"],
            summary=template["summary"],
            published=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            source=template["source"],
            url="https://example.com/fictional-news",
            image_url=get_news_related_image(template["title"]),
            category=template["category"]
        )
        all_news_items.append(news_item)
    
    random.shuffle(all_news_items)
    return all_news_items

def generate_overall_summary(news_items: List[NewsItem]) -> str:
    """Generate a 500-character overall summary based on fictional news"""
    sources = list(set([item.source for item in news_items]))
    mizutani_count = len([item for item in news_items if "M谷" in item.title])
    fictional_news = [item for item in news_items if "M谷" not in item.title]
    
    summary = f"本日お届けする{len(news_items)}件のニュースをご紹介します。"
    
    if fictional_news:
        categories = list(set([item.category for item in fictional_news]))
        if len(categories) >= 2:
            summary += f"主要分野は{categories[0]}、{categories[1]}などとなっています。"
        elif len(categories) == 1:
            summary += f"主要分野は{categories[0]}となっています。"
        
        for item in fictional_news[:2]:
            if "AI" in item.title or "デジタル" in item.title:
                summary += "テクノロジー分野での革新的な進展、"
                break
            elif "経済" in item.category or "企業" in item.title:
                summary += "経済界での注目すべき動き、"
                break
            elif "スポーツ" in item.category:
                summary += "スポーツ界での話題、"
                break
    
    if mizutani_count > 0:
        summary += "注目のM谷氏に関する最新情報も含まれています。"
    
    summary += f"多様な分野の最新動向をお伝えします。"
    
    if len(summary) > 500:
        summary = summary[:497] + "..."
    
    return summary

@app.get("/api/news", response_model=NewsResponse)
async def get_news():
    """Get latest TOP6 news including Mizutani articles with fresh content on each request"""
    try:
        fictional_news = generate_fictional_news()
        mizutani_article = generate_mizutani_article()
        
        if len(fictional_news) >= 5:
            selected_fictional = random.sample(fictional_news, 5)
        else:
            selected_fictional = fictional_news
        
        selected_news = selected_fictional + [mizutani_article]
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
