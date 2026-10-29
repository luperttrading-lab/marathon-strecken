# Straßennamen in Umschrift (Hepburn mit Längenstrich, „-dōri“ = Straße in Ost-West-Richtung, „-suji“ = Straße in Nord-Süd-
# Richtung, „-bashi“ = Brücke). OSM hat die englischen Namen uneinheitlich (Midou Suji Street, Temmabashi Suji Street);
# maßgeblich ist der japanische Name. Zwei längere Stücke tragen in OSM nur den Namen der Straßenverwaltung: 大阪市道赤川天王寺線
# (Stadtstraße Akagawa–Tennōji, zwischen Katamachi und Higashinoda) und 大阪府道173号大阪八尾線 (Präfekturstraße Ōsaka–Yao,
# zwischen Taishō-bashi und Honden); beide in Umschrift. Leerer Wert: Name des Stücks davor übernehmen (kurze Verbinder,
# Kreuzungen, Verwaltungsnamen, die in OSM sonst als zweiter Name einer bekannten Straße stehen).
# Ab der Brücke 新鴫野橋 läuft die Strecke auf Wegen ohne Namen durch den Burgpark zum Ziel: „Ōsaka-jō-kōen“.
UMSCHRIFT = {
    "上町筋": "Uemachi-suji", "土佐堀通": "Tosabori-dōri", "大阪市道赤川天王寺線": "Akagawa-Tennōji-sen", "曽根崎通": "Sonezaki-dōri",
    "天満橋筋": "Tenmabashi-suji", "都島通": "Miyakojima-dōri", "天神橋筋": "Tenjinbashi-suji", "御堂筋": "Midō-suji",
    "中之島通": "Nakanoshima-dōri", "四つ橋筋": "Yotsubashi-suji", "中央大通": "Chūō-ōdōri", "長堀通": "Nagahori-dōri",
    "千日前通": "Sennichimae-dōri", "なにわ筋": "Naniwa-suji", "あみだ池筋": "Amidaike-suji", "新なにわ筋": "Shin-Naniwa-suji",
    "大阪八尾線": "Ōsaka-Yao-sen", "大正通": "Taishō-dōri", "みなと通": "Minato-dōri", "大浪通": "Ōnami-dōri", "国道43号": "",
    "松屋町筋": "Matsuyamachi-suji", "谷町筋": "Tanimachi-suji", "大阪市道四天王寺巽線": "", "大阪市道上新庄生野線": "", "勝山通": "Katsuyama-dōri",
    "今里筋": "Imazato-suji", "城見通": "Shiromi-dōri", "玉造筋": "Tamatsukuri-suji", "新鴫野橋": "Ōsaka-jō-kōen",
}
def umschrift(ja, en=""):
    if ja in UMSCHRIFT: return UMSCHRIFT[ja]
    return None   # unbekannt: build.py meldet es
