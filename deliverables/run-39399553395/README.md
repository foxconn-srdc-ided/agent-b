# CSV 統計 CLI 工具

本工具用於統計 CSV 檔案中 `category` 和 `amount` 欄位的資料，並輸出 JSON 格式的統計結果。

## 使用方式

```bash
python csv_stats.py <input.csv>
```

## 輸出格式

```json
{
  "total_count": 3,
  "total_amount": "250.25",
  "category_stats": {
    "食品": {
      "count": 2,
      "amount": "150.00"
    },
    "交通": {
      "count": 1,
      "amount": "100.25"
    }
  }
}
```

## 特殊處理

- 空白分類歸類為 `UNKNOWN`
- 負金額正確參與計算
- 只有標頭時輸出：`{"total_count":0,"total_amount":"0.00","category_stats":{}}`

## 錯誤處理

- 缺欄位時輸出錯誤訊息至 stderr：`錯誤：CSV 檔案缺少必要欄位。`，退出碼 1
- 非法金額時輸出錯誤訊息至 stderr：`錯誤：金額格式無效。`，退出碼 1
