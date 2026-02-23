import pandas as pd

# 1. 加载原始数据
print("正在读取原始数据...")
df = pd.read_csv("sv_housing_raw_data.csv")

print(f"清洗前，共有 {len(df)} 套房源数据。")

# 2. 基础去重
# 以防万一 API 翻页时有重复抓取的房源，以 zpid 为唯一标准进行去重
df = df.drop_duplicates(subset=['zpid'])

# 3. 处理核心缺失值
# 对于接下来的市场研究来说，如果没有【售价】或【租金估价】，这条数据就失去了测算回报率的价值
# 所以我们选择直接剔除这些核心字段为空的行
df = df.dropna(subset=['pricevalue', 'rentzestimate', 'zestimate'])

# 对于次要字段，比如占地面积(lotsize)，如果是公寓(condo)可能没有占地面积
# 我们可以将其缺失值填充为 0，而不是直接删掉整条数据
df['lotsize'] = df['lotsize'].fillna(0)

# 4. 异常值过滤
# 剔除明显不符合逻辑的脏数据：例如建筑面积 <= 0，或者总价低于 10 万美元（硅谷基本没有这种正常房源）
df = df[(df['livingarea'] > 0) & (df['livingarea'] < 8000) & (df['pricevalue'] > 100000) & (df['pricevalue'] < 5000000)]

# 5. 数据格式标准化
# 确保所有用于计算的列都是数值型 (Numeric)，防止它们变成文本格式影响后续计算
numeric_cols = ['pricevalue', 'pricepersquirefoot', 'zestimate', 'rentzestimate', 'livingarea']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 6. 特征工程 (Feature Engineering) - 增加投资测算维度
# 计算 Zillow 估价与实际标价的差额比例（正数说明标价高于估价，存在溢价）
df['premium_ratio'] = round((df['pricevalue'] - df['zestimate']) / df['zestimate'], 4)

# 计算毛租金回报率 (Gross Rental Yield) = (月租金估价 * 12) / 房屋售价
df['gross_rental_yield'] = round((df['rentzestimate'] * 12) / df['pricevalue'], 4)

# 计算房屋售租比 (Price-to-Rent Ratio)：
df['price_to_rent_ratio'] = round(df['pricevalue'] / (df['rentzestimate'] * 12), 2)

# ==========================================
# 额外清洗：规范化城市名称与剔除边缘城市
# ==========================================

# 1. 规范化命名：将拼写错误的 'Sanjose' 全部替换为标准的 'San Jose'
df['City'] = df['City'].replace({'Sanjose': 'San Jose'})

# 2. 剔除越界数据：只保留城市名不是 'Milpitas' 的行
df = df[df['City'] != 'Milpitas']

# 保存清洗后的完美数据集
output_filename = "sv_housing_clean_data.csv"
df.to_csv(output_filename, index=False, encoding='utf-8')

print(f"\n🎉 清洗完成！")
print(f"清洗后剩余有效房源：{len(df)} 套。")
print(f"已生成用于市场分析的全新维度：'premium_ratio' (溢价率) , 'gross_rental_yield' (毛租金回报率), 'price_to_rent_ratio' (售租比)。")
print(f"数据已保存至：{output_filename}")