# CSV 統計 CLI 工具

本工具使用 Python 標準函式庫實現，用於分析 CSV 檔案中 `category` 和 `amount` 欄位的統計資訊。

## 功能

- 輸入：CSV 檔案，需包含 `category` 和 `amount` 欄位
- 輸出：JSON 格式，包含以下三項資訊：
  - `total_count`: 總筆數
  - `total_amount`: 總金額（以字串形式表示，保留兩位小數）
  - `category_stats`: 各分類的統計資料

## 使用方式

```bash
python csv_stats.py <input.csv>
```

## 特殊處理

- 空白分類視為 `'UNKNOWN'`
- 負金額正確計算
- 若僅有標頭，輸出為：`{"total_count": 0, "total_amount": "0.00", "category_stats": {}}`

## 錯誤處理

- 缺少欄位時：輸出錯誤訊息至 stderr，退出碼為 1
- 非法金額時：輸出錯誤訊息至 stderr，退出碼為 1

## 依賴

- Python 標準函式庫
  - csv
  - decimal
  - json
  - sys
  - argparse
