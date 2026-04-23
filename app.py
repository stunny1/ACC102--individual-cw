import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# 设置页面标题
st.set_page_config(page_title="Foreign Investment Risk Analysis", layout="wide")

# 英文标题 + 居中
st.markdown(
    "<h1 style='text-align: center;'>Foreign Investment Judicial Risk Visualization Analysis</h1>",
    unsafe_allow_html=True
)

# 1. 加载数据
@st.cache_data
def load_data():
    df = pd.read_excel('data/raw/FDI.xlsx')
    return df

df = load_data()



#Step1 Data Cleaning
##1. 从文件夹中抓取数据
#（1）找到文件所在并确保能够打开
import pandas as pd

# 正确的相对路径：从 notebooks/ 文件夹回到项目根目录，再进 data/raw/
file_path = 'data/raw/FDI.xlsx'

# 加载数据
df = pd.read_excel(file_path)
# 查看数据的前几行，确保数据加载正常
print(df.head())

# 查看数据的基本信息，检查是否有缺失值
df.info()

#2. 分步清洗并导出所需数据
#所需数据#1.企业名称：用于统计涉及的企业数量。
         #2.案件名称：用于案件总数统计。
         #3.案件涉及地区（或原告地址）：用于统计案件涉及的省份/城市。
         #4.案件日期（以为案号年份准）：用于时间统计，提取年份。
#（1）企业名称：用于统计涉及的企业数量。
#     提取 `企业名称` 并去重
df_company = df[['企业名称']].dropna()  # 只保留 `企业名称` 列，去除空值
df_company = df_company.drop_duplicates()  # 去重

# 导出路径
df_company.to_csv('data/processed/company_data.csv', index=False)

#（2）案件名称：用于案件总数统计
df_case = df[['案件名称']].dropna()  # 只保留 `案件名称` 列，去除空值
df_case.to_csv('data/processed/case_data.csv', index=False)  # 保存

#（3）地区统计：各城市的案件数量（方便后续除直辖市外合并为各省份数量比较）
df_court = df[['法院']].dropna()  # 只保留 `法院` 列，去除空值
df_court_counts = df_court['法院'].value_counts().reset_index()  # 统计各地区法院数量
df_court_counts.columns = ['法院', '案件数量']  # 重命名列
df_court_counts.to_csv('data/processed/court_data.csv', index=False)  # 保存

#（4）案件日期（以为案号年份准）：用于时间统计，提取年份。
# 提取“相关案号”列
df_case_number = df[['相关案号']]
# 保存提取的相关案号数据到 processed 文件夹
output_file = 'data/processed/relevant_case_numbers.csv'
df_case_number.to_csv(output_file, index=False)

# 保存清洗后的数据
output_file = 'data/processed/cleaned_data.csv'
df.to_csv(output_file, index=False)

# 输出清洗后的数据基本信息
df.info()

#Step2 Analysis

#1.统计案件总数及企业数量
import pandas as pd
import streamlit as st

# 读取清洗后的数据（路径已改好）
df_cleaned = pd.read_csv('data/processed/cleaned_data.csv')

# 统计案件总数
total_cases = len(df_cleaned)

# 统计涉及的企业数量
unique_companies = df_cleaned['企业名称'].nunique()

# 创建 DataFrame 展示案件总数和企业数量
summary_data = {
    "Item": ["Total Cases", "Number of Unique Companies"],
    "Result": [total_cases, unique_companies]
}

# 转换为 DataFrame
summary_df = pd.DataFrame(summary_data)

# ======================
# 👇 网页显示（全英文）
# ======================
st.header("1. Data Summary")
st.dataframe(summary_df, use_container_width=True)
#2.基于法院信息统计不同地区的案件数量（倒序呈现）
import pandas as pd

# 读取清洗后的数据（路径已改好）
df_cleaned = pd.read_csv('data/processed/cleaned_data.csv')

# 城市映射字典
city_mapping = {
    '上海': '上海', '北京': '北京', '广州': '广州', '深圳': '深圳',
    '南京': '南京', '成都': '成都', "杭州": "杭州", "重庆": "重庆",
    "天津": "天津", "苏州": "苏州", "武汉": "武汉", "青岛": "青岛",
    "郑州": "郑州", "长沙": "长沙", "合肥": "合肥", "沈阳": "沈阳",
    "大连": "大连", "济南": "济南", "无锡": "无锡", "厦门": "厦门",
    "福州": "福州", "温州": "温州", "珠海": "珠海", "珠海市": "珠海",
    "昆明": "昆明", "南昌": "南昌", "兰州": "兰州", "贵阳": "贵阳",
    "长春": "长春", "哈尔滨": "哈尔滨", "乌鲁木齐": "乌鲁木齐",
    "海口": "海口", "呼和浩特": "呼和浩特", "西安": "西安", "桂林": "桂林",
    "石家庄": "石家庄", "太原": "太原", "邯郸": "邯郸", "南宁": "南宁",
    "常州": "常州", "洛阳": "洛阳", "金华": "金华", "泉州": "泉州",
    "唐山": "唐山", "中山": "中山", "茂名": "茂名", "台州": "台州",
    "赣州": "赣州", "汕头": "汕头", "扬州": "扬州", "马鞍山": "马鞍山",
    "鞍山": "鞍山", "漳州": "漳州", "蚌埠": "蚌埠", "内蒙古": "内蒙古",
    "吉林": "吉林", "西藏": "西藏", "宁波": "宁波", "威海": "威海",
    "绍兴": "绍兴", "宜昌": "宜昌", "柳州": "柳州", "阜阳": "阜阳",
    "聊城": "聊城", "镇江": "镇江", "烟台": "烟台", "遵义": "遵义",
    "大庆": "大庆", "宿迁": "宿迁", "黄冈": "黄冈", "淮安": "淮安",
    "湛江": "湛江", "西宁": "西宁", "怀化": "怀化", "吕梁": "吕梁",
    "云浮": "云浮", "包头": "包头", "临沂": "临沂", "昌吉": "昌吉",
    "许昌": "许昌", "焦作": "焦作", "咸阳": "咸阳", "中卫": "中卫",
    "拉萨": "拉萨", "商丘": "商丘",
}

# 定义城市匹配函数
def map_city(court_name):
    if pd.isna(court_name):
        return '未知'
    for city in city_mapping:
        if city in court_name:
            return city
    return '其他'

# 生成城市列
df_cleaned['城市'] = df_cleaned['法院'].apply(map_city)

# 统计各城市案件数量
city_case_counts = df_cleaned.groupby('城市')['案件名称'].nunique().reset_index()
city_case_counts.columns = ['城市', '案件数量']
city_case_counts_sorted = city_case_counts.sort_values(by='案件数量', ascending=False)

# 保存结果（给后面地图用）
output_file = 'data/processed/sorted_city_case_counts.csv'
city_case_counts_sorted.to_csv(output_file, index=False)

#3.单独留存案件数量按年份统计表格（方便可视化分析）
import pandas as pd

# 读取案件数据（路径已改好）
file_path = 'data/processed/relevant_case_numbers.csv'
df_case = pd.read_csv(file_path)

# 提取案号年份（假设年份在'相关案号'列中，且格式为“xxxx年”）
df_case['年份'] = df_case['相关案号'].str.extract(r'(\d{4})')

# 清理无效年份
df_case['年份'] = pd.to_numeric(df_case['年份'], errors='coerce')

# 过滤掉非有效年份（如：NaN）
df_case_cleaned = df_case.dropna(subset=['年份'])

# 只保留2010到2025的年份数据
df_case_recent = df_case_cleaned[df_case_cleaned['年份'].between(2010, 2025)]

# 统计不同年份的案件数量
cases_by_year = df_case_recent['年份'].value_counts().sort_index()

# 导出统计结果到processed文件夹
output_file = 'data/processed/cases_by_year_recent.csv'
cases_by_year.to_csv(output_file, index=True)

#Step3 Visualization
#1.除直辖市外的城市按照省份合并，方便后续可视化
import pandas as pd
import os

# --------------------------
#  先读取数据，创建 df_city_cases 变量
# --------------------------
file_path = 'data/processed/sorted_city_case_counts.csv'
df_city_cases = pd.read_csv(file_path)

# --------------------------
# 定义城市到省份的映射字典
# --------------------------
city_to_province = {
  '上海': '上海',
    '北京': '北京',
    '广州': '广东',
    '深圳': '广东',
    '杭州': '浙江',
    '南京': '江苏',
    '苏州': '江苏',
    '天津': '天津',
    '重庆': '重庆',
    '成都': '四川',
    '武汉': '湖北',
    '郑州': '河南',
    '长沙': '湖南',
    '沈阳': '辽宁',
    '青岛': '山东',
    '大连': '辽宁',
    '佛山': '广东',
    '珠海': '广东',
    '厦门': '福建',
    '宁波': '浙江',
    '合肥': '安徽',
    '济南': '山东',
    '福州': '福建',
    '南昌': '江西',
    '兰州': '甘肃',
    '昆明': '云南',
    '哈尔滨': '黑龙江',
    '长春': '吉林',
    '贵阳': '贵州',
    '乌鲁木齐': '新疆',
    '南宁': '广西',
    '呼和浩特': '内蒙古',
    '海口': '海南',
    '石家庄': '河北',
    '邯郸': '河北',
    '宝鸡': '陕西',
    '西安': '陕西',
    '温州': '浙江',
    '湛江': '广东',
    '茂名': '广东',
    '汕头': '广东',
    '芜湖': '安徽',
    '唐山': '河北',
    '洛阳': '河南',
    '淄博': '山东',
    '邢台': '河北',
    '鄂尔多斯': '内蒙古',
    '赣州': '江西',
    '上饶': '江西',
    '扬州': '江苏',
    '徐州': '江苏',
    '南通': '江苏',
    '湖州': '浙江',
    '常州': '江苏',
    '镇江': '江苏',
    '宜昌': '湖北',
    '十堰': '湖北',
    '荆州': '湖北',
    '襄阳': '湖北',
    '咸阳': '陕西',
    '安康': '陕西',
    '银川': '宁夏',
    '西宁': '青海',
    '昭通': '云南',
    '丽江': '云南',
    '大理': '云南',
    '西双版纳': '云南',
    '阿坝': '四川',
    '雅安': '四川',
    '绵阳': '四川',
    '乐山': '四川',
    '泸州': '四川',
    '广元': '四川',
    '达州': '四川',
    '内江': '四川',
    '资阳': '四川',
    '简阳': '四川',
    '攀枝花': '四川',
    '三亚': '海南',
    '东方': '海南',
    '文昌': '海南',
    '五指山': '海南',
    '儋州': '海南',
    '屯昌': '海南',
    '琼海': '海南',
    '万宁': '海南',
    '澄迈': '海南',
    '临高': '海南',
    '保亭': '海南',
    '陵水': '海南',
    '白沙': '海南',
    '昌江': '海南',
    '乐东': '海南',
    '西沙群岛': '海南',
    '中沙群岛': '海南',
    '南沙群岛': '海南',
    '临沧': '云南',
    '保山': '云南',
    '德宏': '云南',
    '文山': '云南',
    '红河': '云南',
    '楚雄': '云南',
    '曲靖': '云南',
    '普洱': '云南',
    '怒江': '云南',
    '迪庆': '云南',
}

# --------------------------
#  按省份归类、聚合数据
# --------------------------
df_city_cases['省份'] = df_city_cases['城市'].apply(lambda x: city_to_province.get(x, '其他'))
df_province_cases = df_city_cases.groupby('省份')['案件数量'].sum().reset_index()
df_province_cases = df_province_cases.sort_values(by='案件数量', ascending=False)

# --------------------------
# 保存数据
# --------------------------
output_dir = 'data/processed'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df_province_cases.to_csv(f'{output_dir}/province_case_counts.csv', index=False)

#2.绘图（以最直观的地图展示各省份近年案件数量）
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth, GeoJson
from folium.plugins import MousePosition
import branca.colormap as cm

# --------------------------
# 1. 数据读取与处理
# --------------------------
# 读取城市案件数据
df_city_cases = pd.read_csv('data/processed/sorted_city_case_counts.csv')

# 城市到省份映射
city_to_province = {
    '上海': '上海', '北京': '北京', '广州': '广东', '深圳': '广东', '杭州': '浙江',
    '南京': '江苏', '苏州': '江苏', '天津': '天津', '重庆': '重庆', '成都': '四川',
    '武汉': '湖北', '郑州': '河南', '长沙': '湖南', '沈阳': '辽宁', '青岛': '山东',
    '大连': '辽宁', '佛山': '广东', '珠海': '广东', '厦门': '福建', '宁波': '浙江',
    '合肥': '安徽', '济南': '山东', '福州': '福建', '南昌': '江西', '兰州': '甘肃',
    '昆明': '云南', '哈尔滨': '黑龙江', '长春': '吉林', '贵阳': '贵州', '乌鲁木齐': '新疆',
    '南宁': '广西', '呼和浩特': '内蒙古', '海口': '海南', '石家庄': '河北', '邯郸': '河北',
    '宝鸡': '陕西', '西安': '陕西', '温州': '浙江', '湛江': '广东', '茂名': '广东',
    '汕头': '广东', '芜湖': '安徽', '唐山': '河北', '洛阳': '河南', '淄博': '山东',
    '邢台': '河北', '鄂尔多斯': '内蒙古', '赣州': '江西', '上饶': '江西', '扬州': '江苏',
    '徐州': '江苏', '南通': '江苏', '湖州': '浙江', '常州': '江苏', '镇江': '江苏',
    '宜昌': '湖北', '十堰': '湖北', '荆州': '湖北', '襄阳': '湖北', '咸阳': '陕西',
    '安康': '陕西', '银川': '宁夏', '西宁': '青海', '昭通': '云南', '丽江': '云南',
    '大理': '云南', '西双版纳': '云南', '阿坝': '四川', '雅安': '四川', '绵阳': '四川',
    '乐山': '四川', '泸州': '四川', '广元': '四川', '达州': '四川', '内江': '四川',
    '资阳': '四川', '简阳': '四川', '攀枝花': '四川', '三亚': '海南', '东方': '海南',
    '文昌': '海南', '五指山': '海南', '儋州': '海南', '屯昌': '海南', '琼海': '海南',
    '万宁': '海南', '澄迈': '海南', '临高': '海南', '保亭': '海南', '陵水': '海南',
    '白沙': '海南', '昌江': '海南', '乐东': '海南',
    '临沧': '云南', '保山': '云南', '德宏': '云南', '文山': '云南', '红河': '云南',
    '楚雄': '云南', '曲靖': '云南', '普洱': '云南', '怒江': '云南', '迪庆': '云南',
}

# 映射城市到省份并聚合
df_city_cases['省份'] = df_city_cases['城市'].apply(lambda x: city_to_province.get(x, '其他'))
df_province_cases = df_city_cases.groupby('省份')['案件数量'].sum().reset_index()

# 标准化省份名称
def normalize_province(name):
    return str(name).replace('市', '').replace('省', '').replace('自治区', '').replace('特别行政区', '')

df_province_cases['省份_normalized'] = df_province_cases['省份'].apply(normalize_province)

# 读取地图文件
china = gpd.read_file('data/china_shapefile/province.shp')
china['pr_name_normalized'] = china['pr_name'].apply(normalize_province)

# 合并数据（案件数量，无数据省份为0）
china = china.merge(
    df_province_cases,
    left_on='pr_name_normalized',
    right_on='省份_normalized',
    how='left'
)
china['案件数量'] = china['案件数量'].fillna(0).astype(int)

# --------------------------
# 2. 创建交互式地图
# --------------------------
st.header("2.Distribution of Case Numbers Across Provinces of China")

# 创建地图
m = folium.Map(location=[35, 105], zoom_start=4, tiles="CartoDB Positron")

# 定义颜色映射（红色系渐变，全英文图例）
colormap = cm.LinearColormap(
    colors=['#fde0dc', '#f99fb7', '#f16873', '#e53b49', '#cb181d', '#99000d'],
    vmin=china['案件数量'].min(),
    vmax=china['案件数量'].max()
)
colormap.caption = "Number of Cases"  # 图例英文
colormap.add_to(m)

# 添加省份图层，实现悬停高亮 + 点击显示数据
def style_function(feature):
    count = feature['properties']['案件数量']
    return {
        'fillColor': colormap(count),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
    }

def highlight_function(feature):
    return {
        'weight': 3,
        'color': '#666',
        'fillOpacity': 0.9
    }

# 转换为 GeoJSON 格式
geojson_data = china.to_json()

GeoJson(
    geojson_data,
    style_function=style_function,
    highlight_function=highlight_function,
    tooltip=None,
    popup=folium.GeoJsonPopup(
        # 全英文显示
        fields=['pr_name', '案件数量'],
        aliases=['Province:', 'Case Count:'],
        localize=True
    ),
    name="Province Case Distribution"
).add_to(m)

# 添加鼠标位置显示
MousePosition().add_to(m)

# --------------------------
# 3. Streamlit 网页展示
# --------------------------
st.components.v1.html(m._repr_html_(), height=700)

# Step2 时间趋势折线图
#目的：展示近15年案件数量的变化趋势，观察案件数量是否出现明显上升、下降或波动。
#1.绘制折线统计图
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 页面设置
st.set_page_config(page_title="历年案件数量趋势", layout="wide")
st.header("3. Number of Cases Over the Past 15 Years")
# 读取数据
file_path = "data/processed/cases_by_year_recent.csv"
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# 排序确保年份顺序正确
df = df.sort_values('年份').reset_index(drop=True)

# ===================== 计算同比增长率 =====================
df['上一年数量'] = df['count'].shift(1)
df['增长率'] = ((df['count'] - df['上一年数量']) / df['上一年数量'] * 100).round(2)
df['增长率'] = df['增长率'].fillna(0)  # 第一年没有增长率

# ===================== 判断颜色：上升黑 / 下降红 =====================
def get_line_color(current, prev):
    if pd.isna(prev):
        return 'black'
    return 'black' if current >= prev else 'red'

colors = []
for i in range(len(df)):
    if i == 0:
        colors.append('black')
    else:
        colors.append(get_line_color(df['count'].iloc[i], df['count'].iloc[i-1]))

# ===================== 使用 Plotly 绘制动态图表 =====================
fig = go.Figure()

#  hover 显示内容（修改为英文）
hover_text = [
    f"Year: {year}<br>Cases: {cnt}<br>Growth Rate: {growth}%"
    for year, cnt, growth in zip(df['年份'], df['count'], df['增长率'])
]

# 画点（修改图例名称为英文）
fig.add_trace(go.Scatter(
    x=df['年份'],
    y=df['count'],
    mode='markers+text',
    text=df['count'],
    textposition='top center',
    textfont=dict(color='red', size=11),
    marker=dict(size=8, color='blue'),
    hovertext=hover_text,
    hoverinfo='text',
    name="Number of Cases" # 图例名称修改为英文
))

# 分段画线：上升黑色 / 下降红色
for i in range(1, len(df)):
    fig.add_trace(go.Scatter(
        x=[df['年份'].iloc[i-1], df['年份'].iloc[i]],
        y=[df['count'].iloc[i-1], df['count'].iloc[i]],
        mode='lines',
        line=dict(color=colors[i], width=3),
        hoverinfo='skip',
        showlegend=False
    ))

# ===================== 动态绘制动画（关键） =====================
frame_duration = 120  # 动画速度，越小越快
frames = []
for i in range(1, len(df)+1):
    frames.append(go.Frame(
        data=fig.data[:1] + fig.data[1:i],
        name=f"frame{i}"
    ))

fig.frames = frames

# 布局 + 动画开启
fig.update_layout(
    # 1. 修改标题为英文
    title="Number of Cases Over the Past 15 Years",
    title_x=0.5,  # 让标题居中 
    xaxis_title="Year",
    yaxis_title="Number of Cases",
    width=1100,
    height=600,
    hovermode="x unified",
    
    # 2. 强制显示每一年的年份
    xaxis=dict(
        tickmode='array',
        tickvals=df['年份'],
        ticktext=df['年份']
    ),

    # 自动播放动画
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        buttons=[dict(
            label="Play Animation",
            method="animate",
            args=[None, dict(
                frame=dict(duration=frame_duration, redraw=True),
                fromcurrent=True,
                transition=dict(duration=0)
            )]
        )]
    )]
)

# 显示图表
st.plotly_chart(fig, use_container_width=True)

#绘制逐年增长率折线图
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ===================== Page Settings =====================
st.set_page_config(page_title="Annual Case Numbers & Growth Rate", layout="wide")


# ===================== Read Data =====================
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "data" / "processed" / "cases_by_year_recent.csv"

df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# Ensure the data is sorted by year
df = df.sort_values('年份').reset_index(drop=True)

# ===================== Calculate Year-over-Year Growth Rate =====================
df['pct_change'] = df['count'].pct_change() * 100

# ===================== Generate Growth Rate Line Chart =====================
fig = go.Figure()

# Add a single trace for all markers (data points)
# This will handle the hover information
fig.add_trace(go.Scatter(
    x=df['年份'],
    y=df['pct_change'],
    mode='markers',
    marker=dict(size=8, color='blue'),
    showlegend=False,
    hovertemplate='Year: %{x}<br>Growth Rate: %{y:.2f}%<extra></extra>'
))

# Add a trace for each line segment to control color based on growth
for i in range(1, len(df)):
    x_vals = [df['年份'].iloc[i-1], df['年份'].iloc[i]]
    y_vals = [df['pct_change'].iloc[i-1], df['pct_change'].iloc[i]]
    
    # Determine the color based on the growth rate of the current point
    color = 'black' if df['pct_change'].iloc[i] >= 0 else 'red'
    
    # Add a line segment, but disable hover for these lines
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='lines',  # Only lines, no markers
        line=dict(color=color, width=3),
        showlegend=False,
        hoverinfo='skip'  # Skip hover for line segments
    ))

# Add a single trace for the legend entry
fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='lines',
    line=dict(color='black', width=3),
    name='Positive Growth'
))
fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='lines',
    line=dict(color='red', width=3),
    name='Negative Growth'
))

# Update layout for titles and labels
fig.update_layout(
    title="Yearly Growth Rate of Case Numbers",
    title_x=0.5,  # 居中 
    xaxis_title="Year",
    yaxis_title="Growth Rate (%)",
    hovermode='x unified',
    legend_title="Growth Type"
)

# Display the chart in the Streamlit app
st.plotly_chart(fig, use_container_width=True)

# Step3 Further analysis of the relationship between year and case count.

#Regression analysis is conducted to examine the linear relationship between the year and the number of cases.
#Hypothesis testing is performed to statistically validate this trend.
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from pathlib import Path

# ===================== Page Settings =====================
st.set_page_config(page_title="5.Case Count Trend Analysis", layout="wide")
st.header("4. Case Count Over Years with Linear Regression Trend Line")


# ===================== Read Data =====================
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "data" / "processed" / "cases_by_year_recent.csv"

df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# ===================== Data Preparation =====================
# Convert year to numeric type for regression
df['year_numeric'] = df['年份'].apply(lambda x: int(x))

# ===================== Linear Regression =====================
# Create and fit the regression model
model = LinearRegression()
model.fit(df[['year_numeric']], df['count'])

# Predict the trend
df['trend'] = model.predict(df[['year_numeric']])

# ===================== Generate Interactive Plot =====================
fig = go.Figure()

# Add trace for actual case count
fig.add_trace(go.Scatter(
    x=df['年份'],
    y=df['count'],
    mode='lines+markers',
    name='Actual Case Count',
    line=dict(color='blue', width=2),
    marker=dict(size=8),
    hovertemplate='Year: %{x}<br>Actual Cases: %{y}<extra></extra>'
))

# Add trace for regression trend line
fig.add_trace(go.Scatter(
    x=df['年份'],
    y=df['trend'],
    mode='lines',
    name='Trend Line',
    line=dict(color='red', width=3, dash='dash'),
    hovertemplate='Year: %{x}<br>Trend Value: %{y:.0f}<extra></extra>'
))

# Update layout for titles, labels, and hover mode
fig.update_layout(
    title="Case Count Over Years with Linear Regression Trend Line",
    title_x=0.5,  # 居中 
    xaxis_title="Year",
    yaxis_title="Number of Cases",
    hovermode='x unified',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )
)

# Display the chart in the Streamlit app
st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Regression Analysis", layout="wide")
st.header("5. Regression Analysis & Hypothesis Testing")

# ===================== 路径设置 =====================
BASE_DIR = Path(__file__).parent
file_path = BASE_DIR / "data" / "processed" / "cases_by_year_recent.csv"

# 读取数据
df = pd.read_csv(file_path)

# 清理数据
df.columns = df.columns.str.strip()
df['year_numeric'] = df['年份'].astype(int)

# ===================== 生成所有年份列表 =====================
all_years = sorted(df['year_numeric'].unique())

# ===================== 年份选择器 =====================
start_year, end_year = st.select_slider(
    'Select Year Range',
    options=all_years,
    value=(min(all_years), max(all_years))
)

# 按年份筛选数据
df_filtered = df[(df['year_numeric'] >= start_year) & (df['year_numeric'] <= end_year)]
st.write(f"**Analysis Period: {start_year} – {end_year} | Observations: {len(df_filtered)}**")

# ===================== 严谨回归分析（年份中心化，避免数值问题） =====================
# 年份中心化（关键！解决条件数过大问题）
df_filtered = df_filtered.copy()
df_filtered['year_centered'] = df_filtered['year_numeric'] - df_filtered['year_numeric'].mean()

X = sm.add_constant(df_filtered['year_centered'])
y = df_filtered['count']
model = sm.OLS(y, X)
results = model.fit()

# ===================== 显示回归结果 =====================
st.write("### Regression Analysis Results")
st.text(results.summary().as_text())  # 更清晰展示

# ====================== 绘制回归图 ======================
fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(df_filtered['year_numeric'], df_filtered['count'], color='#3399ff', label='Actual Cases')
ax.plot(df_filtered['year_numeric'], results.fittedvalues, color='red', linewidth=2, label='Trend Line')

ax.set_title('Case Count vs Year with Regression Trend', fontsize=14)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Number of Cases', fontsize=12)
ax.legend()
plt.tight_layout()
st.pyplot(fig)

# ===================== 假设检验（严谨学术版） =====================
st.write("### Hypothesis Testing")
st.write(f"**R-squared**: {results.rsquared:.4f}")

# 提取关键统计量
coef = results.params['year_centered']
p_val = results.pvalues['year_centered']
r2 = results.rsquared

st.write(f"**Coefficient (Year)**: {coef:.4f}")
st.write(f"**P-value (Year)**: {p_val:.4f}")

# ===================== 原假设与备择假设 =====================
st.write("#### Null Hypothesis & Alternative Hypothesis")
st.write("""
**Null Hypothesis (H₀):** There is no significant linear relationship between the year and the case counts. The slope of the regression line (coefficient of year) is equal to zero.
 
**Alternative Hypothesis (H₁):** There is a significant linear relationship between the year and the case counts. The slope of the regression line (coefficient of year) is not equal to zero.
""")

# ===================== 动态严谨结论（自动判断显著性！） =====================
st.markdown("---")
st.subheader("📊 Conclusion (Statistically Rigorous)")

if p_val < 0.05:
    significance = "**statistically significant**"
    trend_dir = "positive" if coef > 0 else "negative"
    sig_text = f"We **reject the null hypothesis** (p = {p_val:.4f} < 0.05)."
else:
    significance = "**not statistically significant**"
    trend_dir = "non-significant"
    sig_text = f"We **fail to reject the null hypothesis** (p = {p_val:.4f} ≥ 0.05)."

st.write(f"""
{sig_text}

The relationship between year and case counts is **{significance}**.
The coefficient is **{coef:.4f}**, indicating a **{trend_dir} trend**.

R-squared = **{r2:.4f}**, meaning **{r2*100:.1f}%** of the variance in case counts is explained by the time trend.

**Important Note**: This is a **statistical correlation**, not a causal relationship.
Time is a proxy for underlying social, policy, or economic factors—not a direct cause of case count changes.
""")