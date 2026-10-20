import csv
import sys
from decimal import Decimal, InvalidOperation

def main():
    if len(sys.argv) != 2:
        print("使用方法: python csv_stats.py <input.csv>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # 檢查必要欄位是否存在
            if 'category' not in reader.fieldnames or 'amount' not in reader.fieldnames:
                print("錯誤：CSV 檔案缺少必要欄位。", file=sys.stderr)
                sys.exit(1)

            total_count = 0
            total_amount = Decimal('0')
            category_stats = {}

            for row in reader:
                category = row['category'].strip()
                if not category:
                    category = 'UNKNOWN'

                try:
                    amount = Decimal(row['amount'])
                except InvalidOperation:
                    print("錯誤：金額格式無效。", file=sys.stderr)
                    sys.exit(1)

                total_count += 1
                total_amount += amount

                if category not in category_stats:
                    category_stats[category] = {'count': 0, 'amount': Decimal('0')}
                category_stats[category]['count'] += 1
                category_stats[category]['amount'] += amount

            # 格式化輸出
            result = {
                'total_count': total_count,
                'total_amount': str(total_amount.quantize(Decimal('0.00'))),
                'category_stats': {
                    cat: {
                        'count': stat['count'],
                        'amount': str(stat['amount'].quantize(Decimal('0.00')))
                    }
                    for cat, stat in category_stats.items()
                }
            }

            print(result)

    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {filename}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
