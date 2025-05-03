import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np

# 基本設定
st.set_page_config(page_title="汽車銷售儀表板", layout="wide")
st.markdown("""
- **設計: Aries Yeh V1.2**
""")

st.markdown(
    '<a href="https://autosales-lvhamomeiakzjtkdyzwze6.streamlit.app/" style="font-size:64px;">直接看線上分析報告-👉 👉 👉請點我👈 👈 👈</a>',
    unsafe_allow_html=True
)
st.markdown("""
    <style>
        .main {background-color: #f5f7fa;}
        h1, h2, h3, h4 {color: #003366;}
        .block-container {padding: 2rem 2rem;}
    </style>
""", unsafe_allow_html=True)

# 載入資料
@st.cache_data
def load_data():
    df = pd.read_csv('Auto Sales data.csv')
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], format='%d/%m/%Y')
    return df

df = load_data()

# 標題與說明
st.title('🚗 汽車銷售資料分析儀表板')
st.subheader('設計者：葉春華｜版本：V1.2')
st.markdown("""
這個互動式儀表板協助您洞察汽車銷售趨勢、產品表現、顧客行為、市場分布與行銷效果，作為商業決策的依據。
---
""")

# 1. 銷售趨勢分析
st.header('📈 1. 銷售趨勢分析')
df['Month'] = df['ORDERDATE'].dt.to_period('M')
sales_trend = df.groupby('Month')['SALES'].sum().reset_index()
sales_trend['Month'] = sales_trend['Month'].astype(str)
avg_sales = sales_trend['SALES'].mean()

fig1 = px.line(
    sales_trend,
    x='Month',
    y='SALES',
    title='月度銷售趨勢',
    markers=True,
    color_discrete_sequence=px.colors.sequential.Plasma
)
fig1.add_hline(
    y=avg_sales,
    line_dash="dash",
    line_color="orange",
    annotation_text="平均銷售額",
    annotation_position="top left"
)
fig1.update_layout(width=1000, height=500, paper_bgcolor='lightblue', plot_bgcolor='white')
st.plotly_chart(fig1, use_container_width=True)

# 2. 產品表現分析
st.header('📊 2. 產品表現分析')
product_sales = df.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
fig2 = px.bar(product_sales, x='PRODUCTLINE', y='SALES', title='產品線銷售表現', color='PRODUCTLINE', color_discrete_sequence=px.colors.sequential.Greens)
fig2.update_layout(width=1000, height=500)
st.plotly_chart(fig2, use_container_width=True)

# 3. 顧客行為分析
st.header('🔍 3. 顧客行為分析')
customer_behavior = df.groupby('CUSTOMERNAME').agg({'QUANTITYORDERED': 'sum', 'SALES': 'sum'}).reset_index()
fig3 = px.scatter(customer_behavior, x='QUANTITYORDERED', y='SALES', color='CUSTOMERNAME', title='顧客訂單量與銷售額關係', color_discrete_sequence=px.colors.sequential.Reds)
fig3.add_hline(y=customer_behavior['SALES'].mean(), line_dash='dash', line_color='black', annotation_text='平均銷售額')
fig3.add_vline(x=customer_behavior['QUANTITYORDERED'].mean(), line_dash='dash', line_color='black', annotation_text='平均訂單量')
trend = np.polyfit(customer_behavior['QUANTITYORDERED'], customer_behavior['SALES'], 1)
fig3.add_trace(go.Scatter(x=customer_behavior['QUANTITYORDERED'], y=np.poly1d(trend)(customer_behavior['QUANTITYORDERED']), mode='lines', name='趨勢線'))
st.plotly_chart(fig3, use_container_width=True)

# 4. 地理分布分析
st.header('🌍 4. 地理分布分析')
country_sales = df.groupby('COUNTRY')['SALES'].sum().reset_index()
fig4 = px.choropleth(country_sales, locations='COUNTRY', locationmode='country names', color='SALES', title='全球銷售分布', color_continuous_scale=px.colors.sequential.Purples)
fig4.update_layout(width=1000, height=500)
st.plotly_chart(fig4, use_container_width=True)

# 5. 價格策略分析
st.header('💰 5. 價格策略分析')
fig5 = px.box(df, x='DEALSIZE', y='PRICEEACH', title='交易規模與價格關係', color='DEALSIZE', color_discrete_sequence=px.colors.sequential.Oranges)
fig5.update_layout(width=1000, height=500)
st.plotly_chart(fig5, use_container_width=True)

# 6. 庫存管理分析
st.header('📦 6. 庫存管理分析')
product_quantity = df.groupby(['PRODUCTCODE', 'PRODUCTLINE'])['QUANTITYORDERED'].sum().reset_index()
fig6 = px.density_heatmap(product_quantity, x='PRODUCTCODE', y='PRODUCTLINE', z='QUANTITYORDERED', title='產品訂單量熱力圖', color_continuous_scale='YlOrRd')
fig6.update_layout(width=1000, height=500)
st.plotly_chart(fig6, use_container_width=True)

# 7. 市場競爭分析
st.header('📌 7. 市場競爭分析')
product_competition = df.groupby('PRODUCTLINE')['SALES'].mean().reset_index()
fig7 = go.Figure()
fig7.add_trace(go.Scatterpolar(r=product_competition['SALES'], theta=product_competition['PRODUCTLINE'], fill='toself', fillcolor='#00BFFF', opacity=0.6, line=dict(color='#00BFFF', width=2)))
fig7.update_layout(polar=dict(radialaxis=dict(visible=True, tickfont=dict(color='red')), angularaxis=dict(tickfont=dict(color='limegreen'))), title='產品線競爭力雷達圖', width=1000, height=500)
st.plotly_chart(fig7, use_container_width=True)

# 8. 營銷效果分析
st.header('📢 8. 營銷效果分析')
marketing_effect = df.groupby('DEALSIZE')['SALES'].sum().reset_index()
fig8 = px.bar(marketing_effect, x='DEALSIZE', y='SALES', title='營銷活動銷售效果', color='DEALSIZE', color_discrete_sequence=px.colors.sequential.Greens)
fig8.update_layout(width=1000, height=500)
st.plotly_chart(fig8, use_container_width=True)

# 9. 顧客反饋分析
st.header('❤️ 9. 顧客反饋分析')
feedback = df['STATUS'].value_counts().reset_index()
feedback.columns = ['STATUS', 'COUNT']
fig9 = px.pie(feedback, values='COUNT', names='STATUS', title='顧客滿意度分析', color_discrete_sequence=px.colors.sequential.Reds)
fig9.update_layout(width=1000, height=500)
st.plotly_chart(fig9, use_container_width=True)

# 10. 總結與建議
st.header('📌 10. 總結與建議')
st.markdown("""
- **銷售趨勢**：2019年銷售呈現上升，年底可加強促銷。
- **產品表現**：Classic Cars 表現佳，應提高行銷與庫存策略。
- **顧客行為**：識別高價值顧客，進行個性化行銷。
- **地理分布**：USA與France 為主市場，建議開拓日本市場。
- **價格策略**：高單價產品需求穩定，可嘗試微幅調價策略。
- **庫存管理**：熱銷產品需確保充足庫存，清理滯銷品項。
- **市場競爭**：Classic Cars 保持領先，應持續創新與推廣。
- **營銷效果**：Large 類型交易銷售高，可強化 B2B 行銷活動。
- **顧客反饋**：Disputed 與 Cancelled 雖少見，但物流仍有優化空間。
""")
