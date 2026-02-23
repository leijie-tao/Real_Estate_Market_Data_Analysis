import pandas as pd
import json
import requests
import plotly.graph_objects as go

# ==========================================
# 1. 准备你的“好学校” Zipcode 数据
# ==========================================
# 🚨 请在这里填入你手里的前10名学校对应的 Zipcode 和你给它们打的分数(或排名)
# 注意：Zipcode 必须是字符串格式（带引号），不能是纯数字！
top_school_data = {
    'zipcode': ['95014', '95129', '95051', '94087', '94024','94085','94086','94087','95050',
                '95054','95126','95111','95148','95131','95125','95126','95128','95117','95133',
                '95124','95112','95118','95136','95110','95122','95116'], # 这里我先用几个硅谷著名好学区举例
    'school_score': [10, 10, 10, 10, 10, 10, 10, 10, 8, 8, 7, 5, 10, 2, 8, 7, 5, 3, 10, 7, 5, 9, 6, 5, 5, 5] # 10分代表最顶尖
}
df_schools = pd.DataFrame(top_school_data)

# ==========================================
# 2. 获取加州 Zipcode 的 GeoJSON 边界文件
# ==========================================
print("正在从开源数据库自动下载加州 Zipcode 地图边界数据 (可能需要几秒钟)...")
# 这是一个非常稳定且常用的全美开源 GeoJSON 仓库
url = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ca_california_zip_codes_geo.min.json"
response = requests.get(url)
ca_zip_geojson = response.json()

# ==========================================
# 3. 读取并处理你的房源清洗数据
# ==========================================
print("正在读取房源数据...")
df_houses = pd.read_csv("sv_housing_clean_data.csv")
df_houses = df_houses.dropna(subset=['latitude', 'longitude', 'zipcode'])

# 🚨 极度重要：确保房源表里的 zipcode 是纯文本字符串，否则地图无法匹配！
# 比如把 "95014.0" 或者数字 95014 强制变成文本 "95014"
df_houses['zipcode'] = df_houses['zipcode'].astype(str).str.split('.').str[0]

# ==========================================
# 4. 开始画图：双图层叠加
# ==========================================
print("正在生成交互式叠加地图...")
fig = go.Figure()

# --- 图层一：Zipcode 学区热力底图 (Choropleth) ---
fig.add_trace(go.Choroplethmapbox(
    geojson=ca_zip_geojson,
    locations=df_schools['zipcode'],
    # 在这个开源 GeoJSON 里，代表邮编的字段名叫 'ZCTA5CE10'
    featureidkey="properties.ZCTA5CE10",
    z=df_schools['school_score'],
    colorscale="Greens",        # 用绿色渐变：越绿代表学校越好
    marker_opacity=0.5,         # 半透明，为了能看清底下的街道名字
    marker_line_width=1.5,      # 邮编边界线粗细
    marker_line_color='white',
    name="School Score",
    colorbar_title="School<br>Score"
))

# --- 图层二：房源散点图 (Scatter) ---
fig.add_trace(go.Scattermapbox(
    lat=df_houses['latitude'],
    lon=df_houses['longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=8,
        color=df_houses['pricevalue'],  # 房子越贵，颜色越暖（红/黄）
        colorscale='Plasma',            # 散点用紫红黄渐变，和绿色的底图形成强烈视觉对比
        showscale=True,
        colorbar_title="Home Price",
        colorbar_x=1.1                  # 把房源的颜色条往右移一点，防止和学区颜色的条重叠
    ),
    # 鼠标悬停时显示具体信息
    text="Price: $" + df_houses['pricevalue'].astype(str) + "<br>Zip: " + df_houses['zipcode'],
    hoverinfo='text',
    name="Properties"
))

# ==========================================
# 5. 设置地图视角并展示
# ==========================================
fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        zoom=10.5,
        center={"lat": 37.35, "lon": -122.0} # 视角中心对准硅谷
    ),
    margin={"r":0,"t":50,"l":0,"b":0},
    title_text="School Distribution and Real Estate Spatial Distribution (San Jose, Santa Clara, Sunnyvale, Cupertino)",
    title_x=0.5
)

# 自动在浏览器中打开
fig.show()