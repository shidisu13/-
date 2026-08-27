# -*- coding: utf-8 -*-
"""生成 data/daily/2026-08-26.json —— 完整合并 skuSales(148天轴) + rankData(2026/8/25+2026/8/26)。
不改动任何历史每日文件；仅新增本日文件（build_board 取最新非空文件作 skuSales/rankData 唯一源）。
OCR 值原样保留（按用户 8:21 确认）。
"""
import json, copy, datetime

SRC = "data/daily/2026-08-25.json"
OUT = "data/daily/2026-08-26.json"

d = json.load(open(SRC, encoding="utf-8"))

# ---------- 1) allData for 2026-08-26 ----------
dt = datetime.date(2026, 8, 26)
allData = {
    "date": "2026-08-26",
    "label": "8/26",
    "month": 8, "day": 26, "dow": dt.isoweekday(),  # Wed=3
    "views": 9551, "visitors": 3490, "buyers": 1090,
    "cvr": 31.23, "orders": 1245, "items": 1564,
    "revenue": 51243.50, "asp": 47.01,  # 客单价取自截图（=revenue/buyers 舍入结果）
}

# ---------- 2) skuSales: 追加 8月26日 到 dates 轴，按 OCR 填值（缺失→None） ----------
sku_ocr = {
 "100316289162": {"成交金额":8727.39,"商品访客数":771,"商品浏览量":1693,"加购商品件数":97,"成交商品件数":104,"成交转化率":12.32},
 "100254081502": {"成交金额":8421.56,"商品访客数":425,"商品浏览量":943,"加购商品件数":90,"成交商品件数":86,"成交转化率":18.35},
 "100125825485": {"成交金额":7095.06,"商品访客数":591,"商品浏览量":1158,"加购商品件数":78,"成交商品件数":145,"成交转化率":17.94},
 "100078478420": {"成交金额":6911.17,"商品访客数":645,"商品浏览量":1275,"加购商品件数":43,"成交商品件数":288,"成交转化率":39.07},
 "100194747356": {"成交金额":5927.42,"商品访客数":1202,"商品浏览量":1861,"加购商品件数":1986,"成交商品件数":530,"成交转化率":31.95},
 "100209597405": {"成交金额":5143.57,"商品访客数":334,"商品浏览量":772,"加购商品件数":44,"成交商品件数":54,"成交转化率":11.08},
 "100290582795": {"成交金额":2564.09,"商品访客数":281,"商品浏览量":457,"加购商品件数":17,"成交商品件数":125,"成交转化率":39.50},
 "100254081496": {"成交金额":2416.44,"商品访客数":186,"商品浏览量":358,"加购商品件数":21,"成交商品件数":31,"成交转化率":15.05},
 "100365875850": {"成交金额":1595.20,"商品访客数":144,"商品浏览量":245,"加购商品件数":19,"成交商品件数":16,"成交转化率":11.11},
}
# 100259919854 今日截图无 → None；100344131112 今日新 SKU 不在监控表 → 不写入 dashboard skuSales

skuSales = copy.deepcopy(d["skuSales"])
skuSales["dates"].append("8月26日")
for s in skuSales["skus"]:
    sid = s["id"]
    vals = sku_ocr.get(sid)
    for metric in skuSales["metrics"]:
        s["data"][metric].append(vals[metric] if vals else None)

# ---------- 3) rankData: 新增 2026/8/26 周期（10行/表） ----------
def with_change(rows):
    out = []
    for r in rows:
        r = dict(r)
        r["change"] = "持平"   # 今日截图无可见排名变化文字列，按安全默认；schema 必需
        out.append(r)
    return out

shops_ocr = [
 {"rank":"1","name":"可口可乐京东自营旗舰店","revenue":"¥50万~¥75万","revenueChg":"412%~414%","visitors":"1万~2万","visitorsChg":"-10.12%","orders":"2,000~4,000","ordersChg":"0%~2%","search":"4,000~6,000","searchChg":"-5.52%"},
 {"rank":"2","name":"农夫山泉京东自营旗舰店","revenue":"¥25万~¥50万","revenueChg":"2%~4%","visitors":"6,000~8,000","visitorsChg":"-3.20%","orders":"2,000~4,000","ordersChg":"2%~4%","search":"4,000~6,000","searchChg":"-3.18%"},
 {"rank":"3","name":"山姆会员商店官方旗舰店","revenue":"¥10万~¥25万","revenueChg":"0%~2%","visitors":"1万~2万","visitorsChg":"-1.84%","orders":"1,000~2,000","ordersChg":"2%~4%","search":"2,000~4,000","searchChg":"-3.07%"},
 {"rank":"4","name":"if饮料京东自营旗舰店","revenue":"¥10万~¥25万","revenueChg":"20%~22%","visitors":"2,000~4,000","visitorsChg":"+32.63%","orders":"1,000~2,000","ordersChg":"12%~14%","search":"2,000~4,000","searchChg":"+16.94%"},
 {"rank":"5","name":"三麟京东自营旗舰店","revenue":"¥10万~¥25万","revenueChg":"-4%~-2%","visitors":"2,000~4,000","visitorsChg":"-5.35%","orders":"1,000~2,000","ordersChg":"-2%~0%","search":"2,000~4,000","searchChg":"-7.88%"},
 {"rank":"6","name":"轻上京东自营旗舰店","revenue":"¥10万~¥25万","revenueChg":"4%~6%","visitors":"1万~2万","visitorsChg":"+0.52%","orders":"2,000~4,000","ordersChg":"2%~4%","search":"1万~2万","searchChg":"+4.22%"},
 {"rank":"7","name":"金豆芽京东自营旗舰店","revenue":"¥10万~¥25万","revenueChg":"2%~4%","visitors":"6,000~8,000","visitorsChg":"+9.77%","orders":"2,000~4,000","ordersChg":"-6%~-4%","search":"4,000~6,000","searchChg":"-1.98%"},
 {"rank":"8","name":"轻上 (LIGHT UPPER) 京东自营旗舰店","revenue":"¥10万~¥25万","revenueChg":"2%~4%","visitors":"1万~2万","visitorsChg":"-23.46%","orders":"2,000~4,000","ordersChg":"-2%~0%","search":"6,000~8,000","searchChg":"-2.49%"},
 {"rank":"9","name":"京东茶造自营旗舰店","revenue":"¥8万~¥10万","revenueChg":"-4%~-2%","visitors":"8,000~1万","visitorsChg":"+1.44%","orders":"1,000~2,000","ordersChg":"-8%~-6%","search":"6,000~8,000","searchChg":"+1.48%"},
 {"rank":"10","name":"1号会员店","revenue":"¥6万~¥8万","revenueChg":"26%~28%","visitors":"4,000~6,000","visitorsChg":"-3.71%","orders":"1,000~2,000","ordersChg":"10%~12%","search":"2,000~4,000","searchChg":"+6.67%"},
]

spus_ocr = [
 {"rank":"1","name":"可口可乐 (Coca-Cola) 姜汁源","id":"4690568","revenue":"¥50万~¥75万","revenueShare":"950%~952%","visitors":"2,000~4,000","visitorsChg":"+2.73%","orders":"600~800","ordersShare":"14%~16%","search":"1,000~2,000","searchChg":"-9.21%"},
 {"rank":"2","name":"农夫山泉100%纯果汁NFC橙汁30...","id":"5327144","revenue":"¥10万~¥25万","revenueShare":"8%~10%","visitors":"4,000~6,000","visitorsChg":"-2.00%","orders":"1,000~2,000","ordersShare":"4%~6%","search":"2,000~4,000","searchChg":"-0.87%"},
 {"rank":"3","name":"三麟100%NFC椰子水330ml*24","id":"100020805609","revenue":"¥10万~¥25万","revenueShare":"-4%~-2%","visitors":"2,000~4,000","visitorsChg":"-4.55%","orders":"1,000~2,000","ordersShare":"0%~2%","search":"2,000~4,000","searchChg":"-6.17%"},
 {"rank":"4","name":"if【肖战推荐】100%纯椰子水果","id":"100010442629","revenue":"¥10万~¥25万","revenueShare":"22%~24%","visitors":"2,000~4,000","visitorsChg":"+39.13%","orders":"1,000~2,000","ordersShare":"14%~16%","search":"2,000~4,000","searchChg":"+19.54%"},
 {"rank":"5","name":"金豆芽金钼花柚子汁儿童饮品夏天","id":"100088472687","revenue":"¥8万~¥10万","revenueShare":"0%~2%","visitors":"4,000~6,000","visitorsChg":"+0.46%","orders":"2,000~4,000","ordersShare":"-10%~-8%","search":"2,000~4,000","searchChg":"-4.52%"},
 {"rank":"6","name":"轻上 (LIGHT UPPER) 100%椰子","id":"100103922320","revenue":"¥6万~¥8万","revenueShare":"4%~6%","visitors":"6,000~8,000","visitorsChg":"-0.35%","orders":"1,000~2,000","ordersShare":"-2%~0%","search":"6,000~8,000","searchChg":"+2.88%"},
 {"rank":"7","name":"农夫山泉冰茶C100柠檬味复合果...","id":"848890","revenue":"¥4万~¥6万","revenueShare":"-14%~-12%","visitors":"1,000~2,000","visitorsChg":"-10.19%","orders":"400~600","ordersShare":"-10%~-8%","search":"1,000~2,000","searchChg":"-9.26%"},
 {"rank":"8","name":"麦动村椰子水100%纯椰子汁245","id":"100262285374","revenue":"¥4万~¥6万","revenueShare":"-12%~-10%","visitors":"6,000~8,000","visitorsChg":"-12.28%","orders":"1,000~2,000","ordersShare":"-10%~-8%","search":"4,000~6,000","searchChg":"-15.39%"},
 {"rank":"9","name":"可口可乐 (Coca-Cola) 姜汁源","id":"100014226708","revenue":"¥4万~¥6万","revenueShare":"-8%~-6%","visitors":"6,000~8,000","visitorsChg":"-8.40%","orders":"1,000~2,000","ordersShare":"-2%~0%","search":"1,000~2,000","searchChg":"-4.13%"},
 {"rank":"10","name":"轻上牛牛山苹果果四神汤苹果味儿","id":"100288911854","revenue":"¥4万~¥6万","revenueShare":"-4%~-2%","visitors":"4,000~6,000","visitorsChg":"+2.06%","orders":"1,000~2,000","ordersShare":"2%~4%","search":"1,000~2,000","searchChg":"-5.23%"},
]

skus_ocr = [
 {"rank":"1","name":"可口可乐 (Coca-Cola) 姜汁源","id":"7564141","revenue":"¥50万~¥75万","revenueShare":"7362%~7364%","visitors":"400~600","visitorsChg":"+0.61%","orders":"100~200","ordersShare":"34%~36%","search":"200~400","searchChg":"0.00%"},
 {"rank":"2","name":"if【肖战推荐】100%纯椰子水果","id":"100010442629","revenue":"¥8万~¥10万","revenueShare":"20%~22%","visitors":"2,000~4,000","visitorsChg":"+58.29%","orders":"600~800","ordersShare":"12%~14%","search":"1,000~2,000","searchChg":"+39.40%"},
 {"rank":"3","name":"农夫山泉100%纯果汁NFC橙汁30...","id":"3313643","revenue":"¥6万~¥8万","revenueShare":"8%~10%","visitors":"1,000~2,000","visitorsChg":"+10.59%","orders":"200~400","ordersShare":"6%~8%","search":"600~800","searchChg":"+15.47%"},
 {"rank":"4","name":"轻上 (LIGHT UPPER) 100%椰子","id":"100103922320","revenue":"¥6万~¥8万","revenueShare":"2%~4%","visitors":"6,000~8,000","visitorsChg":"+2.31%","orders":"1,000~2,000","ordersShare":"-2%~0%","search":"4,000~6,000","searchChg":"+6.70%"},
 {"rank":"5","name":"农夫山泉100%纯果汁NFC橙汁30...","id":"5327144","revenue":"¥4万~¥6万","revenueShare":"8%~10%","visitors":"2,000~4,000","visitorsChg":"+1.82%","orders":"600~800","ordersShare":"-2%~0%","search":"1,000~2,000","searchChg":"+3.96%"},
 {"rank":"6","name":"可口可乐 (Coca-Cola) 姜汁源","id":"4690568","revenue":"¥4万~¥6万","revenueShare":"10%~12%","visitors":"1,000~2,000","visitorsChg":"+4.66%","orders":"400~600","ordersShare":"12%~14%","search":"600~1,000","searchChg":"-9.20%"},
 {"rank":"7","name":"三麟100%NFC椰子水330ml*24","id":"100020805609","revenue":"¥4万~¥6万","revenueShare":"6%~8%","visitors":"800~1,000","visitorsChg":"-6.76%","orders":"200~400","ordersShare":"-2%~0%","search":"400~600","searchChg":"-19.70%"},
 {"rank":"8","name":"轻上牛牛山苹果果四神汤苹果味儿","id":"100288911854","revenue":"¥4万~¥6万","revenueShare":"0%~2%","visitors":"2,000~4,000","visitorsChg":"+4.64%","orders":"1,000~2,000","ordersShare":"6%~8%","search":"1,000~2,000","searchChg":"+1.95%"},
 {"rank":"9","name":"三麟100%NFC椰子水1L*6瓶盒装","id":"100027606065","revenue":"¥4万~¥6万","revenueShare":"-2%~0%","visitors":"1,000~2,000","visitorsChg":"-3.44%","orders":"400~600","ordersShare":"4%~6%","search":"800~1,000","searchChg":"-7.68%"},
 {"rank":"10","name":"if【肖战推荐】100%天然椰子水","id":"100084629033","revenue":"¥2万~¥4万","revenueShare":"22%~24%","visitors":"1,000~2,000","visitorsChg":"+4.78%","orders":"200~400","ordersShare":"20%~22%","search":"1,000~2,000","searchChg":"-0.58%"},
]

rankData = copy.deepcopy(d["rankData"])
rankData["shops"]["2026/8/26"] = with_change(shops_ocr)
rankData["spus"]["2026/8/26"]  = with_change(spus_ocr)
rankData["skus"]["2026/8/26"]  = with_change(skus_ocr)

out = {
    "date": "2026-08-26",
    "allData": allData,
    "skuSales": skuSales,
    "rankData": rankData,
}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---------- 自检 ----------
chk = json.load(open(OUT, encoding="utf-8"))
print("WROTE", OUT)
print("skuSales dates count:", len(chk["skuSales"]["dates"]), "last:", chk["skuSales"]["dates"][-1])
print("skuSales skus:", len(chk["skuSales"]["skus"]), "each metric len:", len(chk["skuSales"]["skus"][0]["data"]["成交金额"]))
# 验证 100259919854 末位为 None
for s in chk["skuSales"]["skus"]:
    if s["id"]=="100259919854":
        print("100259919854 末位:", {m:s['data'][m][-1] for m in chk['skuSales']['metrics']})
print("rankData periods:", {k:list(v.keys()) for k,v in chk["rankData"].items()})
for k in ("shops","spus","skus"):
    print(f"  {k} 2026/8/26 rows:", len(chk["rankData"][k]["2026/8/26"]), "row0 change:", chk["rankData"][k]["2026/8/26"][0]["change"])
