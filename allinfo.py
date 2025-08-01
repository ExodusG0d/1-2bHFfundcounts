import requests
import json
import time

# 1. 基本设置
base_url = "https://gs.amac.org.cn/amac-infodisc/api/pof/manager/query"
# 查询参数，页码(page)将通过URL动态构建
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

# 2. 初始化变量
all_results_content = []
final_data_to_save = {}

try:
    # 3. 发送首次请求，获取总页数等元数据
    print("正在获取元数据...")
    initial_url = f"{base_url}?page=0&size=20"
    response = requests.post(initial_url, headers=headers, json=payload, timeout=20)
    response.raise_for_status()
    initial_data = response.json()

    total_pages = initial_data.get('totalPages', 0)
    total_elements = initial_data.get('totalElements', 0)

    final_data_to_save = {
        'totalElements': total_elements,
        'totalPages': total_pages,
        'size': initial_data.get('size'),
        'sort': initial_data.get('sort'),
        'content': []
    }

    if total_pages == 0:
        print("未能获取到总页数，或总结果为0。程序退出。")
    else:
        print(f"发现总共有 {total_elements} 条数据，共 {total_pages} 页。")
        print("-" * 30)

        # 4. 循环遍历所有页面，抓取数据
        for page_num in range(total_pages):
            print(f"正在抓取第 {page_num + 1} 页 / 共 {total_pages} 页...")
            if page_num == 0:
                page_data = initial_data
            else:
                # 为后续页面构建URL并发起新请求
                current_url = f"{base_url}?page={page_num}&size=20"
                time.sleep(1)
                response = requests.post(current_url, headers=headers, json=payload, timeout=20)
                response.raise_for_status()
                page_data = response.json()

            # 提取并追加当页数据
            if 'content' in page_data and page_data['content']:
                all_results_content.extend(page_data['content'])

    # 5. 整合并保存所有抓取到的数据
    final_data_to_save['content'] = all_results_content
    print("-" * 30)
    print(f"抓取完成！")
    print(f"期望获取 {total_elements} 条数据，实际抓取到 {len(all_results_content)} 条数据。")

    if all_results_content:
        with open('all_fund_data_with_meta.json', 'w', encoding='utf-8') as f:
            json.dump(final_data_to_save, f, ensure_ascii=False, indent=4)
        print("所有数据已保存到 all_fund_data.json 文件中。")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
except json.JSONDecodeError as e:
    print(f"解析JSON响应失败: {e}")
    if 'response' in locals():
        print(f"收到的非JSON响应内容: {response.text}")
except Exception as e:
    print(f"发生未知错误: {e}")
