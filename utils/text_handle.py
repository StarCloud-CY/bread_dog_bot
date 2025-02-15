class Translator:
    class Progress:
        @staticmethod
        def zh_to_en(text: str):
            progress_dict = {"史莱姆王": "King Slime", "克苏鲁之眼": "Eye of Cthulhu",
                             "世界吞噬者/克苏鲁之脑": "Eater of Worlds / Brain of Cthulhu", "蜂后": "Queen Bee",
                             "骷髅王": "Skeletron",
                             "巨鹿": "Deerclops", "血肉之墙": "Wall of Flesh", "史莱姆女王": "Queen Slime",
                             "双子魔眼": "The Twins",
                             "毁灭者": "The Destroyer", "机械骷髅王": "Skeletron Prime", "世纪之花": "Plantera",
                             "石巨人": "Golem",
                             "猪龙鱼公爵": "Duke Fishron", "光之女皇": "Empress of Light",
                             "拜月教邪教徒": "Lunatic Cultist",
                             "月亮领主": "Moon Lord", "无": "None"}
            try:
                return progress_dict[text]
            except KeyError:
                return text

        @staticmethod
        def en_to_zh(text: str):
            progress_dict = {"King Slime": "史莱姆王", "Eye of Cthulhu": "克苏鲁之眼",
                             "Eater of Worlds / Brain of Cthulhu": "世界吞噬者/克苏鲁之脑", "Queen Bee": "蜂后",
                             "Skeletron": "骷髅王", "Deerclops": "巨鹿", "Wall of Flesh": "血肉之墙",
                             "Queen Slime": "史莱姆女王", "The Twins": "双子魔眼", "The Destroyer": "毁灭者",
                             "Skeletron Prime": "机械骷髅王", "Plantera": "世纪之花", "Golem": "石巨人",
                             "Duke Fishron": "猪龙鱼公爵", "Empress of Light": "光之女皇",
                             "Lunatic Cultist": "拜月教邪教徒",
                             "Moon Lord": "月亮领主", "None": "无"}
            try:
                return progress_dict[text]
            except KeyError:
                return text
