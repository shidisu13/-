# -*- coding: utf-8 -*-
"""生成 data/daily/2026-08-31.json —— 完整合并 skuSales(153天轴) + rankData(追加 2026/8/31)。
不改动任何历史每日文件；仅新增本日文件（build_board 取最新非空文件作 skuSales/rankData 唯一源）。
OCR 值原样保留（按用户今日上传的 9 张截图核对）。

⚠️ OCR 备注：
- 截图 2/3 第 6 行 OCR 得 "SKU: 100209997405"，但与已追踪 SKU 100209597405 同位同值，
  视为 OCR 误读 5→9，按 100209597405 写入（请用户核对）。
- SPU 8/31 截图第 8/9/10 行的 change 标识符部分模糊，未明确时记 null。
"""
import json, copy, datetime

SRC = "data/daily/2026-08-30.json"
OUT = "data/daily/2026-08-31.json"

d = json.load(open(SRC, encoding="utf-8"))

# ---------- 1) allData for 2026-08-31 ----------
dt = datetime.date(2026, 8, 31)
allData = {
    "date": "2026-08-31",
    "label": "8/31",
    "month": 8, "day": 31, "dow": dt.isoweekday(),  # Mon=1
    # OCR: 成交金额 ¥47,300.72 (vs 44,800.58, +5.58%)
    "revenue": 47300.72,
    # OCR: 商品浏览量 8,005 (vs 7,798, +2.63%)
    "views": 8005,
    # OCR: 商品访客数 2,954 (vs 2,879, +2.61%)
    "visitors": 2954,
    # OCR: 成交客户数（成交人数） 1,019 (vs 898, +13.47%)
    "buyers": 1019,
    # OCR: 成交转化率 34.50% (vs 31.19%, +10.59%) —— 存为百分数 34.50
    "cvr": 34.50,
    # OCR: 成交单量 1,149 (vs 1,035, +11.01%)
    "orders": 1149,
    # OCR: 成交商品件数 1,527 (vs 1,387, +10.09%)
    "items": 1527,
    # OCR: 客单价 ¥46.42 (vs ¥49.89, -6.96%) —— 与 revenue/buyers 一致 (47300.72/1019=46.42)
    "asp": 46.42,
}

# ---------- 2) skuSales: 追加 8月31日 到 dates 轴，按 OCR 填值（缺失→None） ----------
# 字段顺序：成交金额 / 商品访客数 / 商品浏览量 / 加购商品件数 / 成交商品件数 / 成交转化率
# 转化率按规范写为 "X.XX%" 字符串（不要除以 100）
sku_ocr = {
 "100254081502": (8539.26, 424, 845, 39, 87,  "17.45%"),
 "100125825485": (5881.44, 516, 1065, 65, 119, "20.93%"),
 # 100259919854 history-only, 始终 None
 "100316289162": (8651.60, 690, 1520, 81, 103, "12.32%"),
 "100209597405": (4677.85, 315, 634, 44, 52,  "12.38%"),  # OCR 显示 100209997405, 视作误读
 "100194747356": (7006.81, 880, 1343, 1451, 639, "44.55%"),
 "100254081496": (2253.00, 195, 370, 28, 29,   "11.79%"),
 "100078478420": (6767.58, 580, 1155, 47, 269, "39.31%"),
 "100365875850": None,   # 截图 Top10 中未出现此 SKU
 "100290582795": (1713.69, 229, 362, 9, 82,    "33.62%"),
}

skuSales = copy.deepcopy(d["skuSales"])
skuSales["dates"].append("8月31日")
for s in skuSales["skus"]:
    sid = s["id"]
    tup = sku_ocr.get(sid)
    for i, metric in enumerate(skuSales["metrics"]):
        s["data"][metric].append(tup[i] if tup else None)

# ---------- 3) rankData: 新增 2026/8/31 周期（10行/表） ----------

# ----- 行业店铺数据 (shops, 12列, 4 个「变动」列) -----
# col0 周期(此函数外加) 1rank 2change 3name 4revenue 5revenueChg
# 6visitors 7visitorsChg 8orders 9ordersChg 10search 11searchChg
shops_ocr = [
 {"rank":"1","change":"持平", "name":"可口可乐京东自营旗舰店",
     "revenue":"¥50万~¥75万","revenueChg":"-32%~-30%",
     "visitors":"6,000~8,000","visitorsChg":"-22.51%",
     "orders":"1,000~2,000","ordersChg":"0%~-2%",
     "search":"4,000~6,000","searchChg":"-2.54%"},
 {"rank":"2","change":"持平", "name":"农夫山泉京东自营旗舰店",
     "revenue":"¥25万~¥50万","revenueChg":"14%~16%",
     "visitors":"8,000~1万","visitorsChg":"+3.59%",
     "orders":"2,000~4,000","ordersChg":"4%~6%",
     "search":"6,000~8,000","searchChg":"+9.86%"},
 {"rank":"3","change":"持平", "name":"山姆会员商店官方旗舰店",
     "revenue":"¥10万~¥25万","revenueChg":"-2%~0%",
     "visitors":"8,000~1万","visitorsChg":"-0.89%",
     "orders":"1,000~2,000","ordersChg":"-6%~-4%",
     "search":"2,000~4,000","searchChg":"+2.21%"},
 {"rank":"4","change":"↑1", "name":"叮咚买菜京东自营旗舰店",
     "revenue":"¥10万~¥25万","revenueChg":"12%~14%",
     "visitors":"2,000~4,000","visitorsChg":"-7.30%",
     "orders":"1,000~2,000","ordersChg":"0%~-2%",
     "search":"2,000~4,000","searchChg":"-7.64%"},
 {"rank":"5","change":"↓1", "name":"三顿京东自营旗舰店",
     "revenue":"¥10万~¥25万","revenueChg":"-2%~0%",
     "visitors":"2,000~4,000","visitorsChg":"-2.31%",
     "orders":"1,000~2,000","ordersChg":"-4%~-2%",
     "search":"2,000~4,000","searchChg":"-3.67%"},
 {"rank":"6","change":"持平", "name":"金豆芽京东自营旗舰店",
     "revenue":"¥10万~¥25万","revenueChg":"0%~2%",
     "visitors":"6,000~8,000","visitorsChg":"+2.59%",
     "orders":"2,000~4,000","ordersChg":"0%~2%",
     "search":"4,000~6,000","searchChg":"-4.07%"},
 {"rank":"7","change":"↓2", "name":"轻上京东自营旗舰店",
     "revenue":"¥10万~¥25万","revenueChg":"-6%~-4%",
     "visitors":"1万~2万","visitorsChg":"-5.05%",
     "orders":"2,000~4,000","ordersChg":"-4%~-2%",
     "search":"8,000~1万","searchChg":"-5.06%"},
 {"rank":"8","change":"持平", "name":"京东京造自营旗舰店",
     "revenue":"¥10万~¥25万","revenueChg":"6%~8%",
     "visitors":"8,000~1万","visitorsChg":"-0.17%",
     "orders":"1,000~2,000","ordersChg":"0%~-2%",
     "search":"6,000~8,000","searchChg":"-5.67%"},
 {"rank":"9","change":"持平", "name":"轻上（LIGHT UPPER）京东自营旗舰店",
     "revenue":"¥10万~¥25万","revenueChg":"8%~10%",
     "visitors":"1万~2万","visitorsChg":"+3.12%",
     "orders":"2,000~4,000","ordersChg":"4%~6%",
     "search":"4,000~6,000","searchChg":"+2.24%"},
 {"rank":"10","change":"新入榜", "name":"麦谷村MAIGUCUN京东自营旗舰店",
     "revenue":"¥6万~¥8万","revenueChg":"20%~22%",
     "visitors":"8,000~1万","visitorsChg":"+3.01%",
     "orders":"1,000~2,000","ordersChg":"12%~14%",
     "search":"6,000~8,000","searchChg":"+0.26%"},
]

# ----- 商品spu榜 (spus, 13列) -----
# col0 周期 1rank 2change 3name 4id 5revenue 6revenueShare 7visitors 8visitorsChg
# 9orders 10ordersShare 11search 12searchChg
spus_ocr = [
 {"rank":"1","change":"新入榜", "name":"可口可乐（Coca-Cola）姜汁源","id":"100234548811",
     "revenue":"¥10万~¥25万","revenueShare":"--",
     "visitors":"--","visitorsChg":"--",
     "orders":"0~5","ordersShare":"--",
     "search":"--","searchChg":"--"},
 {"rank":"2","change":"持平", "name":"农夫山泉100%纯果汁NFC橙汁30","id":"5327144",
     "revenue":"¥10万~¥25万","revenueShare":"56%~58%",
     "visitors":"6,000~8,000","visitorsChg":"+7.63%",
     "orders":"1,000~2,000","ordersShare":"6%~8%",
     "search":"4,000~6,000","searchChg":"+15.21%"},
 {"rank":"3","change":"新入榜", "name":"可口可乐（Coca-Cola）姜汁源","id":"100218327561",
     "revenue":"¥10万~¥25万","revenueShare":"--",
     "visitors":"--","visitorsChg":"--",
     "orders":"0~5","ordersShare":"--",
     "search":"--","searchChg":"--"},
 {"rank":"4","change":"持平", "name":"三顿100%NFC椰子水330ml*24","id":"100020805609",
     "revenue":"¥10万~¥25万","revenueShare":"-2%~0%",
     "visitors":"2,000~4,000","visitorsChg":"-2.54%",
     "orders":"1,000~2,000","ordersShare":"-6%~-4%",
     "search":"2,000~4,000","searchChg":"-3.16%"},
 {"rank":"5","change":"↑1", "name":"if【月战推荐】100%纯椰子水果","id":"100010442629",
     "revenue":"¥8万~¥10万","revenueShare":"18%~20%",
     "visitors":"2,000~4,000","visitorsChg":"-0.14%",
     "orders":"800~1,000","ordersShare":"8%~10%",
     "search":"1,000~2,000","searchChg":"-5.55%"},
 {"rank":"6","change":"↓1", "name":"金豆芽金银花柚子汁儿童饮品夏天","id":"100088472687",
     "revenue":"¥8万~¥10万","revenueShare":"0%~2%",
     "visitors":"4,000~6,000","visitorsChg":"-5.66%",
     "orders":"2,000~4,000","ordersShare":"0%~2%",
     "search":"2,000~4,000","searchChg":"-1.51%"},
 {"rank":"7","change":"新入榜", "name":"可口可乐（Coca-Cola）姜汁源","id":"100291366122",
     "revenue":"¥6万~¥8万","revenueShare":"--",
     "visitors":"--","visitorsChg":"--",
     "orders":"0~5","ordersShare":"--",
     "search":"--","searchChg":"--"},
 {"rank":"8","change":None, "name":"可口可乐（Coca-Cola）姜汁源","id":"4690568",
     "revenue":"¥6万~¥8万","revenueShare":"-94%~-92%",
     "visitors":"1,000~2,000","visitorsChg":"+9.76%",
     "orders":"400~600","ordersShare":"22%~24%",
     "search":"1,000~2,000","searchChg":"+12.03%"},
 {"rank":"9","change":"↓1", "name":"轻上（LIGHT UPPER）100%椰子","id":"100103922320",
     "revenue":"¥6万~¥8万","revenueShare":"4%~6%",
     "visitors":"6,000~8,000","visitorsChg":"-3.07%",
     "orders":"2,000~4,000","ordersShare":"2%~4%",
     "search":"4,000~6,000","searchChg":"-3.21%"},
 {"rank":"10","change":None, "name":"麦谷村椰子水100%纯椰子汁245","id":"100262285374",
     "revenue":"¥4万~¥6万","revenueShare":"14%~16%",
     "visitors":"6,000~8,000","visitorsChg":"+5.27%",
     "orders":"1,000~2,000","ordersShare":"10%~12%",
     "search":"4,000~6,000","searchChg":"+0.46%"},
]

# ----- 商品sku榜 (skus, 13列) -----
skus_ocr = [
 {"rank":"1","change":"新入榜", "name":"可口可乐（Coca-Cola）姜汁源","id":"100234548811",
     "revenue":"¥10万~¥25万","revenueShare":"--",
     "visitors":"--","visitorsChg":"--",
     "orders":"0~5","ordersShare":"--",
     "search":"--","searchChg":"--"},
 {"rank":"2","change":"新入榜", "name":"可口可乐（Coca-Cola）姜汁源","id":"100218327561",
     "revenue":"¥10万~¥25万","revenueShare":"--",
     "visitors":"--","visitorsChg":"--",
     "orders":"0~5","ordersShare":"--",
     "search":"--","searchChg":"--"},
 {"rank":"3","change":"新入榜", "name":"可口可乐（Coca-Cola）姜汁源","id":"100291366122",
     "revenue":"¥6万~¥8万","revenueShare":"--",
     "visitors":"--","visitorsChg":"--",
     "orders":"0~5","ordersShare":"--",
     "search":"--","searchChg":"--"},
 {"rank":"4","change":"持平", "name":"农夫山泉100%纯果汁NFC橙汁30","id":"3313643",
     "revenue":"¥6万~¥8万","revenueShare":"30%~32%",
     "visitors":"2,000~4,000","visitorsChg":"+10.22%",
     "orders":"200~400","ordersShare":"10%~12%",
     "search":"1,000~2,000","searchChg":"+13.69%"},
 {"rank":"5","change":"持平", "name":"农夫山泉100%纯果汁NFC橙汁30","id":"5327144",
     "revenue":"¥6万~¥8万","revenueShare":"24%~26%",
     "visitors":"2,000~4,000","visitorsChg":"+13.46%",
     "orders":"600~800","ordersShare":"4%~6%",
     "search":"1,000~2,000","searchChg":"+52.48%"},
 {"rank":"6","change":"新入榜", "name":"农夫山泉100%纯果汁NFC果汁30","id":"100007725801",
     "revenue":"¥4万~¥6万","revenueShare":"382%~384%",
     "visitors":"600~800","visitorsChg":"+0.42%",
     "orders":"200~400","ordersShare":"32%~34%",
     "search":"400~600","searchChg":"+0.19%"},
 {"rank":"7","change":"持平", "name":"if【月战推荐】100%纯椰子水果","id":"100010442629",
     "revenue":"¥4万~¥6万","revenueShare":"14%~16%",
     "visitors":"1,000~2,000","visitorsChg":"+4.11%",
     "orders":"600~800","ordersShare":"8%~10%",
     "search":"800~1,000","searchChg":"-2.76%"},
 {"rank":"8","change":None, "name":"可口可乐（Coca-Cola）姜汁源","id":"4690568",
     "revenue":"¥4万~¥6万","revenueShare":"-80%~-78%",
     "visitors":"1,000~2,000","visitorsChg":"+10.61%",
     "orders":"400~600","ordersShare":"24%~26%",
     "search":"600~800","searchChg":"+15.96%"},
 {"rank":"9","change":"↓1", "name":"轻上（LIGHT UPPER）100%椰子","id":"100103922320",
     "revenue":"¥4万~¥6万","revenueShare":"4%~6%",
     "visitors":"4,000~6,000","visitorsChg":"-3.57%",
     "orders":"800~1,000","ordersShare":"0%~-2%",
     "search":"4,000~6,000","searchChg":"-3.09%"},
 {"rank":"10","change":"↓2", "name":"轻上牛午山药苹果四神汤苹果儿","id":"100288911854",
     "revenue":"¥4万~¥6万","revenueShare":"2%~4%",
     "visitors":"2,000~4,000","visitorsChg":"-5.09%",
     "orders":"400~600","ordersShare":"-4%~-2%",
     "search":"400~600","searchChg":"-4.59%"},
]

rankData = copy.deepcopy(d["rankData"])
rankData["shops"]["2026/8/31"] = shops_ocr
rankData["spus"]["2026/8/31"]  = spus_ocr
rankData["skus"]["2026/8/31"]  = skus_ocr

out = {
    "date": "2026-08-31",
    "allData": allData,
    "skuSales": skuSales,
    "rankData": rankData,
}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---------- 自检 ----------
chk = json.load(open(OUT, encoding="utf-8"))
print("WROTE", OUT)
print("allData:", chk["allData"])
print("skuSales dates count:", len(chk["skuSales"]["dates"]), "last:", chk["skuSales"]["dates"][-3:])
print("skuSales skus:", len(chk["skuSales"]["skus"]), "each metric len:", len(chk["skuSales"]["skus"][0]["data"]["成交金额"]))
for s in chk["skuSales"]["skus"]:
    if s["id"] in ("100259919854", "100365875850", "100209597405"):
        print(f"{s['id']} 末位:", {m:s['data'][m][-1] for m in chk['skuSales']['metrics']})
print("rankData periods:")
for k, v in chk["rankData"].items():
    print(f"  {k}: {list(v.keys())}")
for k in ("shops","spus","skus"):
    rows = chk["rankData"][k]["2026/8/31"]
    print(f"  {k} 2026/8/31: {len(rows)} rows, row0 change={rows[0]['change']!r}, row0 name={rows[0]['name']!r}")