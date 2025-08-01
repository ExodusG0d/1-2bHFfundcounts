import requests
import json
import time
import pandas as pd

# 1. 基本设置
base_url = "https://gs.amac.org.cn/amac-infodisc/api/pof/manager/query"
payload = {
    "primaryInvestType": "smzqtzjjglr",
    "fundType": "smzqzzfx",
    "fundScale": "scope03",
    "establishDate": {"from": "1900-01-01", "to": "9999-01-01"},
    "registerDate": {"from": "1900-01-01", "to": "9999-01-01"},
    "size": 20
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8'
}

# 2. 发送首次请求，获取总页数
print("正在获取元数据...")
initial_url = f"{base_url}?page=0&size=20"
response = requests.post(initial_url, headers=headers, json=payload, timeout=20)
initial_data = response.json()
total_pages = initial_data.get('totalPages', 0)
total_elements = initial_data.get('totalElements', 0)
print(f"发现总共有 {total_elements} 条数据，共 {total_pages} 页。")
print("-" * 30)

# 3. 循环抓取所有页面的数据
all_results_content = []
for page_num in range(total_pages):
    print(f"正在抓取第 {page_num + 1} 页 / 共 {total_pages} 页...")
    if page_num == 0:
        page_data = initial_data
    else:
        current_url = f"{base_url}?page={page_num}&size=20"
        time.sleep(1)
        response = requests.post(current_url, headers=headers, json=payload, timeout=20)
        page_data = response.json()

    if 'content' in page_data and page_data['content']:
        all_results_content.extend(page_data['content'])

# 4. 使用 pandas 将数据保存到 CSV 文件
if all_results_content:
    df = pd.DataFrame(all_results_content)
    df['totalElements'] = total_elements
    df.to_csv('all_fund_data.csv', index=False, encoding='utf-8-sig')

    print("-" * 30)
    print(f"抓取完成！共 {len(all_results_content)} 条数据")
    print("已保存到 all_fund_data.csv 文件中。")
else:
    print("没有抓取到任何数据。")
