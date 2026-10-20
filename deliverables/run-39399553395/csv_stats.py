import csv
import decimal
import json
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='CSV 統計工具')
    parser.add_argument('csv_file', help='輸入的 CSV 檔案')
    args = parser.parse_args()
    
    try:
        with open(args.csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # 檢查必要欄位是否存在
            if 'category' not in reader.fieldnames or 'amount' not in reader.fieldnames:
                print("錯誤：CSV 檔案缺少必要欄位。", file=sys.stderr)
                sys.exit(1)
            
            total_count = 0
            total_amount = decimal.Decimal('0.00')
            category_stats = {}
            
            for row in reader:
                category = row['category'].strip() or 'UNKNOWN'
                try:
                    amount = decimal.Decimal(row['amount'])
                except decimal.InvalidOperation:
                    print("錯誤：金額格式無效。", file=sys.stderr)
                    sys.exit(1)
                
                total_count += 1
                total_amount += amount
                
                if category not in category_stats:
                    category_stats[category] = {'count': 0, 'amount': decimal.Decimal('0.00')}
                
                category_stats[category]['count'] += 1
                category_stats[category]['amount'] += amount
            
            # 將 Decimal 轉為字串並保留兩位小數
            result = {
                'total_count': total_count,
                'total_amount': str(total_amount),
                'category_stats': {
                    k: {
                        'count': v['count'],
                        'amount': str(v['amount'])
                    }
                    for k, v in category_stats.items()
                }
            }
            
            print(json.dumps(result, ensure_ascii=False))
            
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {args.csv_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"錯誤：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
