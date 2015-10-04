# what's this?

This is just simple scraping code to get information from Japanese University Mr/Ms Campus contest.

See [this site](https://misscolle.com/)

You can get Profile information and pictures from there.

This code is just only for 2015. You can't use this to 2014 or previous version.


# Setting up

You install dependency libraries with following command

    pip install -r requiremnet.txt
    
# How to use it

`get_miss_person_info.py` is example interface script.

Execute this script.

Or you can edit and use if you need some modification.

And you can change parameters in `settings.py`

IMPORATANT: take enough time between each access. Don't make trouble site master.


## output

You can get json file and profile pictures.

For json, you can get file like below. See [here](https://misscolle.com/aoyama2015/profile/1) to check original site.

    [
        {
            "major": "文学部フランス文学科3年", 
            "twitter_link": "https://twitter.com/natsuko_15miss1", 
            "name": "神名夏子", 
            "entry_no": "ENTRY 01", 
            "univ_name": "青山学院大学", 
            "height": "156.0cm", 
            "QA": {
                "よく行くエリア・スポット": "青山、銀座", 
                "理想の結婚相手": "おばあちゃんになっても、女の子として見てくれる方", 
                "自分を色で例えると?": "白、ラベンダー、ピンクとよく言われます。", 
                "将来の夢": "大好きな人と一緒に、幸せな家庭をつくること", 
                "初恋はいつ?": "幼稚園のとき", 
                "尊敬する人": "母、姉、親友", 
                "好きな歌手": "back number、JUDY AND MARY", 
                "頑張ろうと思っていること": "自分の長所をなにか一つ見つけること内面から輝く女性になること", 
                "こんな異性に惹かれます": "謙虚で、夢にむかって頑張っている男性", 
                "もし一目惚れしたらどうアプローチする?": "なにもできません。願いながらひそかに想い続けます（笑）", 
                "最近一番言っている言葉": "「はやく夏休みこないかなぁ〜♪」と、「ねーなんか楽しいことしよっ！」", 
                "ミスコンテストに参加したきっかけ": "数年前からお誘いをいただいていて、大学生活のなかで努力したものを形に残したいと思い参加させていただきました。", 
                "旅行で行きたい場所": "フランスか、海がきれいなところ。今はサントリーニ島に行きたいです。", 
                "よく読む雑誌": "Ray、Sweet", 
                "ミスコンテストへの意気込みを一言": "今回このような機会をいただき、とても光栄に思っています。半年間を無駄にすることのないよう精一杯の努力をしていきますので、応援よろしくお願いいたします。", 
                "好きな芸人": "流れ星さん", 
                "休日の過ごし方": "目覚ましをかけずに寝て、午後からは映画をたくさん観たり、お買い物に出かけたり…したいことをしてのんびりと過ごします。", 
                "１つだけ願いが叶うとしたら?": "身長があと7センチ欲しいです。", 
                "特技": "クラシックバレエ", 
                "掛けられて嬉しい言葉": "内面的なことや仕草について、あとまわりの人のことを褒められると嬉しいです。", 
                "好きな食べ物": "焼き鳥が大好きです！", 
                "ストレス解消法": "好きな映画を観ながら半身浴友達や家族とおいしいものを食べてたくさんお喋り", 
                "好きな映画": "フランソワ・オゾン監督と、ソフィア・コッポラ監督の作品が好きです。", 
                "平均睡眠時間": "6時間前後", 
                "今までで一番美味しかった飲食店": "胃腸炎から回復したあとに食べた母の手料理", 
                "マイブーム": "お散歩かわいいピアス集め", 
                "アルバイト": "青山のレストラン", 
                "理想の告白シチュエーション": "誕生日が冬なので、ふたりでイルミネーションを見た帰りに言われたいです。", 
                "好きなテレビ番組": "海外ドラマ", 
                "友達が異性に変わる瞬間": "前に話したことを覚えていてくれたとき自分だけに違う一面を見せてくれたとき", 
                "趣味": "映画鑑賞、おいしいものを食べること。フランス映画が大好きです。", 
                "所属サークル": "なし", 
                "コーヒー派?紅茶派?": "コーヒー派。朝は目がシャキッと、カフェタイムや食後は苦味でほっとするので。", 
                "今までで一番泣いたこと": "大切な家族を失ったこと", 
                "アピールポイント": "笑顔と白い肌と、精神の図太さ", 
                "今までで一番笑ったこと": "毎日、たくさん笑っています！", 
                "よく使うアプリ": "Camera360,Instagram,LINE", 
                "学生生活を一言で表すと?": "いろいろな人との出会いと感謝に溢れています(o^^o)", 
                "好きな場所": "夕方の公園お家のベランダ", 
                "「ドキッ」とする異性の仕草": "頭に手を置かれること髪をなでられること", 
                "最近買った一番高い物": "ワンピース", 
                "自己流モテるテクニック": "自然体でいること、感情表現を豊かにすること", 
                "好きな男性有名人": "特にいません", 
                "好きな女性有名人": "綾瀬はるかさん、水ト麻美さん", 
                "１００万円あったらどうする?": "フランスに滞在", 
                "無人島に１つだけ持って行くもの": "どこでもドア"
            },
            "birth_place": "神奈川県", 
            "blog_link": "http://b2015.misscolle.com/aoyama-shimmei/", 
            "birth_date": "1994年11月30日", 
            "photo_url": "https://misscolle.com//img/contests/aoyama2015/1/main.jpg?1435724514", 
            "blood_type": "O型", 
            "name_rubi": "Shimmei Natsuko"
        }
        ]
        

And you can get pictures. Pictures are saved under the directory which you specify at initializing `ExtractPersonInfo` class.


