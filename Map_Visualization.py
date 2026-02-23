import pandas as pd
import plotly.express as px

# 1. 读取清洗好的数据
print("正在读取数据...")
df = pd.read_csv("sv_housing_clean_data.csv")

# 2. 清理掉没有坐标的异常数据 (以防万一有的房源没抓到经纬度)
df = df.dropna(subset=['latitude', 'longitude'])

# 3. 🚀 核心代码：绘制交互式地图散点
print("正在生成地图，请稍候（将在浏览器中自动打开）...")
fig = px.scatter_mapbox(
    df,
    lat="latitude",  # 纬度列
    lon="longitude",  # 经度列
    color="pricevalue", color_continuous_scale=px.colors.sequential.Plasma,  # 按照【城市】用不同颜色区分
    # 如果你想看哪里最贵，可以把上一行改成 color="pricevalue", 它会变成价格热力图！

    size="livingarea",  # 点的大小由【室内面积】决定 (房子越大，圆圈越大)
    size_max=15,  # 限制最大圆圈的尺寸，防止地图太拥挤

    # 当你的鼠标悬停在点上时，弹出的信息框里展示什么内容：
    hover_name="streetaddress",
    hover_data={
        "City": True,
        "pricevalue": ":$,.0f",  # 格式化为带逗号的美元符号 (如 $1,500,000)
        "livingarea": True,
        "price_to_rent_ratio": True,
        "latitude": False,  # 隐藏多余的经纬度显示
        "longitude": False
    },

    zoom=10.7,  # 初始的地图缩放级别
    mapbox_style="carto-positron",  # 免费且美观的底层地图样式 (不需要API Key)
    title="Silicon Valley Real Estate Spatial Distribution (San Jose, Santa Clara, Sunnyvale, Cupertino)"
)

# 4. 调整一下图表的边距和标题居中
fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    title_x=0.5
)

# 5. 在浏览器中弹出可交互的地图！
fig.show()

# 如果你想把这个可交互地图保存发给别人看，可以存为网页格式：
# fig.write_html("Silicon_Valley_Real_Estate_Map.html")
# print("可交互地图已保存为 Silicon_Valley_Real_Estate_Map.html，双击即可在浏览器打开！")