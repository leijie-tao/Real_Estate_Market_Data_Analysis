import requests
import pandas as pd
import time

# 1. 设置你的 API 钥匙和目标城市
# 请替换为你自己在 RapidAPI 上拿到的真实 Key
API_KEY = "YOUR_API_KEY""   # <--- 注意这里替换成你的Key
API_HOST = "YOUR_API_KEY_HOST"

# 我们需要分析的四个硅谷核心城市
cities = ["San Jose, CA", "Santa Clara, CA", "Sunnyvale, CA", "Cupertino, CA"]

# 准备一个空列表，用来装所有房子的数据
all_houses_data = []


def fetch_city_data(city_name):
    """
    这是一个封装好的函数，专门用来获取单个城市的数据（支持自动翻页）
    """
    print(f"正在获取 {city_name} 的数据...")

    # 更新为正确的 Search 接口 URL
    url = "YOUR_API_URL"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    # 初始化页码变量
    current_page = 1
    total_pages = 1  # 初始假定只有1页，等请求了第一页拿到真实总页数后再更新

    # 开始循环翻页
    while current_page <= total_pages:
        print(f"  -> 正在获取第 {current_page} 页 (共 {total_pages} 页)...")

        # 查询参数：加入了之前缺失的必填参数，并且把 page 设为动态变量
        querystring = {
            "location": city_name,
            "listingStatus": "For_Sale",  # 必填参数：在售房源
            "sortOrder": "Homes_for_you",  # 保持排序一致
            "page": str(current_page)  # 动态页码
        }
        try:
            # 发送请求
            response = requests.get(url, headers=headers, params=querystring)

            # 检查 HTTP 状态码
            if response.status_code != 200:
                print(f"请求失败！状态码: {response.status_code}")
                break  # 如果某页请求失败，跳出当前城市的翻页循环

            # 将返回的数据转化为字典格式
            data = response.json()
            # ---------------------------------------------------------
            # 核心更新 1：动态更新总页数 (只在获取第一页时更新一次即可)
            # 根据你之前的截图，API 返回了 pagesInfo -> totalPages
            # ---------------------------------------------------------
            if current_page == 1:
                pages_info = data.get('pagesInfo', {})
                if pages_info and 'totalPages' in pages_info:
                    total_pages = pages_info.get('totalPages')
                else:
                    print(f"  ⚠️ 未能从 API 获取到总页数，将只抓取第一页。")

            # 提取房源列表
            search_results = data.get('searchResults', [])

            if not search_results:
                print(f"  ⚠️ 第 {current_page} 页没有返回任何数据，停止翻页。")
                break

            # ---------------------------------------------------------
            # 核心更新 2：解析当页数据并按照所需字段追加到总列表
            # ---------------------------------------------------------
            for item in search_results:
                prop = item.get('property', {})

                # 提取嵌套的字典，使用 {} 作为默认值，防止因为某个房源缺少该分类而导致程序报错
                location_info = prop.get('location', {})
                address_info = prop.get('address', {})
                price_info = prop.get('price', {})
                estimates_info = prop.get('estimates', {})
                listing_info = prop.get('listing', {})
                lotsize_info = prop.get('lotSizeWithUnit', {})

                # 按照你要求的字段列表提取数据
                house_info = {
                    'latitude': location_info.get('latitude'),
                    'longitude': location_info.get('longitude'),
                    'zpid': prop.get('zpid'),  # 强烈建议保留：用于后续数据去重
                    'City': address_info.get('city'),
                    'streetaddress': address_info.get('streetAddress'),
                    'zipcode': address_info.get('zipcode'),
                    'hometype': prop.get('propertyType'),
                    'bathrooms': prop.get('bathrooms'),
                    'bedrooms': prop.get('bedrooms'),
                    'livingarea': prop.get('livingArea'),
                    'yearbuilt': prop.get('yearBuilt'),
                    'lotsize': lotsize_info.get('lotSize'),
                    'listingstatus': listing_info.get('listingStatus'),
                    'pricevalue': price_info.get('value'),
                    'pricepersquirefoot': price_info.get('pricePerSquareFoot'),
                    'zestimate': estimates_info.get('zestimate'),
                    'rentzestimate': estimates_info.get('rentZestimate')
                }

                all_houses_data.append(house_info)
            # 准备抓取下一页
            current_page += 1

            # ⚠️ 极度重要：每次翻页都必须停顿！否则很容易触发 API 限流 (Rate Limit)
            time.sleep(5)
        except Exception as e:
            print(f"  ❌ 获取 {city_name} 第 {current_page} 页时出错: {e}")
            break  # 发生异常时停止当前城市的翻页


# 2. 遍历我们的城市列表，逐个获取数据
for city in cities:
    fetch_city_data(city)
    # 加上两秒的停顿，防止请求过快被 API 平台限制
    time.sleep(2)

# 3. 将收集到的数据转化为 DataFrame，并保存为 CSV
if all_houses_data:
    df = pd.DataFrame(all_houses_data)

    # 简单去重一下（有时候 API 翻页时相邻页可能会有极少数重复的房源）
    df = df.drop_duplicates(subset=['zpid'])

    df.to_csv("sv_housing_raw_data.csv", index=False, encoding='utf-8')
    print(f"🎉 大功告成！四大城市全部抓取完毕！")
    print(f"📊 经过去重后，共抓取到 {len(df)} 套有效房源数据。")
    print(f"💾 已保存为 sv_housing_raw.csv")
else:
    print("未能获取到任何数据，请检查。")