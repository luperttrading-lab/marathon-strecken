# Straßennamen in Umschrift (Hepburn mit Längenstrich, „-dōri“ = Straße, „-kaidō“ = alte Landstraße, „-bashi“ = Brücke).
# OSM hat die englischen Namen uneinheitlich (Chuo-dori Avenue, Chūō Street, Chūō-dōri Avenue); maßgeblich ist der japanische Name.
# Leerer Wert: Name des Stücks davor übernehmen (kurze Verbinder mit Verwaltungsnamen).
UMSCHRIFT = {
    "都庁通り": "Tochō-dōri", "南通り": "Minami-dōri", "議事堂通り": "Gijidō-dōri", "北通り": "Kita-dōri",
    "東京都道新宿副都心八号線": "", "四谷角筈線": "", "千代田練馬田無線": "",
    "青梅街道": "Ōme-kaidō", "靖国通り": "Yasukuni-dōri", "外堀通り": "Sotobori-dōri", "白山通り": "Hakusan-dōri",
    "中央通り": "Chūō-dōri", "中央通り;万世橋": "Chūō-dōri", "万世橋": "Chūō-dōri", "永代通り": "Eitai-dōri",
    "新大橋通り": "Shin-Ōhashi-dōri", "清洲橋通り": "Kiyosubashi-dōri", "清杉通り": "Kiyosugi-dōri", "江戸通り": "Edo-dōri",
    "並木通り": "Namiki-dōri", "雷門通り": "Kaminarimon-dōri", "蔵前橋通り": "Kuramaebashi-dōri", "蔵前橋": "Kuramae-bashi",
    "清澄通り": "Kiyosumi-dōri", "晴海通り": "Harumi-dōri", "日比谷通り": "Hibiya-dōri", "芝園橋": "Shibazono-bashi",
    "第一京浜": "Daiichi-Keihin", "丸の内仲通り": "Marunouchi-Naka-dōri", "行幸通り": "Gyōkō-dōri",
}
def umschrift(ja, en=""):
    if ja in UMSCHRIFT: return UMSCHRIFT[ja]
    return None   # unbekannt: build.py meldet es
