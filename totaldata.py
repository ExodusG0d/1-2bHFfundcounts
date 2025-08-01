import requests
import json

# 1. 设置请求的URL和参数
url = "https://gs.amac.org.cn/amac-infodisc/api/pof/manager/query?&page=0&size=20"

payload = {"primaryInvestType":"smzqtzjjglr","regiProvinceFsc":"province","offiProvinceFsc":"province","fundType":"smzqzzfx","fundScale":"scope03","establishDate":{"from":"1900-01-01","to":"9999-01-01"},"registerDate":{"from":"1900-01-01","to":"9999-01-01"}}

# 2. 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*'
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=20)
    response.raise_for_status()

    result_data = response.json()
    total_count = result_data['totalElements']
    print(f"根据筛选条件，查询到的结果总数为: {total_count}")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
except Exception as e:
    print(f"处理数据时发生错误: {e}")