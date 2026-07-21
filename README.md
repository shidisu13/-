# 每日销售数据看板

线上地址：https://shidisu13.github.io/-/dashboard.html

## 架构原则

- **网页与数据分离**：`dashboard.html` 运行时通过 `fetch('./data/board.json')` 拉取数据，仓库不内联任何业务数据。
- **腾讯文档为唯一数据源**：每日销售数据以截图 → OCR → 腾讯文档为权威来源，GitHub 仅用于保存历史与展示。
- **按天增量存储**：每日数据写入 `data/daily/YYYY-MM-DD.json`，由 `scripts/build_board.py` 合并为 `data/board.json` 与 `data/index.json`（幂等、可回滚、可审计）。
- **历史永久保留**：单个日文件只追加不覆盖，重跑同一天会触发覆盖保护。

## 目录结构

```
dashboard.html        # 渲染层（数据驱动，无内联数据）
data/
  board.json          # 合并后的全量看板数据
  index.json          # 每日数据索引（日期列表）
  daily/              # 每日增量数据，按天切片
```

## 每日更新流程

1. 截屏当日销售数据 → OCR 识别。
2. 录入腾讯文档（唯一权威源）。
3. 生成 `data/daily/YYYY-MM-DD.json`（仅当天新增）。
4. 运行 `build_board.py` 合并为 `board.json` / `index.json`。
5. 提交并推送：

   ```bash
   git add data/
   git commit -m "data: 每日销售数据 YYYY-MM-DD"
   git push origin master
   ```

推送后 GitHub Pages 自动更新，无需手动构建。

## 回滚

任何一天的提交都可通过 `git revert` 撤销；单日文件丢失只需重新生成对应 `daily/YYYY-MM-DD.json` 再跑合并脚本。
