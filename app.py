import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Samsung Global Analysis", layout="wide")

# 2. Carregar Dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("samsung_global_sales_dataset.csv")
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    return df

df = carregar_dados()

# 3. Barra Lateral (Filtros)
st.sidebar.title("Filtros Globais")
regiao = st.sidebar.multiselect("Região", options=df["region"].unique(), default=df["region"].unique())
categoria = st.sidebar.multiselect("Categoria", options=df["category"].unique(), default=df["category"].unique())

# Aplicando Filtros
df_filtrado = df[df["region"].isin(regiao) & df["category"].isin(categoria)]

# 4. Título e Métricas Principais
st.title("📊 Dashboard Executivo Samsung")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Receita Total", f"$ {df_filtrado['revenue_usd'].sum():,.2f}")
m2.metric("Unidades Vendidas", f"{df_filtrado['units_sold'].sum():,}")
m3.metric("Ticket Médio", f"$ {df_filtrado['unit_price_usd'].mean():,.2f}")
m4.metric("Satisfação Média", f"⭐ {df_filtrado['customer_rating'].mean():.1f}")

st.markdown("---")

# 5. LINHA 1: Mapa e Top Países
st.subheader("🌎 Visão Geográfica")
col_mapa, col_paises = st.columns([2, 1])

with col_mapa:
    df_mapa = df_filtrado.groupby("country")["revenue_usd"].sum().reset_index()
    fig_mapa = px.choropleth(df_mapa, locations="country", locationmode="country names",
                             color="revenue_usd", color_continuous_scale="Blues")
    st.plotly_chart(fig_mapa, use_container_width=True)

with col_paises:
    top_paises = df_filtrado.groupby("country")["revenue_usd"].sum().nlargest(10).reset_index()
    fig_paises = px.bar(top_paises, x="revenue_usd", y="country", orientation='h', 
                        title="Top 10 Países", color_discrete_sequence=["#003399"])
    fig_paises.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_paises, use_container_width=True)

st.markdown("---")

# 6. LINHA 2: Tendência Temporal e Categorias
st.subheader("📈 Tendências e Produtos")
col_tempo, col_pizza = st.columns(2)

with col_tempo:
    vendas_tempo = df_filtrado.groupby("sale_date")["revenue_usd"].sum().reset_index()
    fig_linha = px.line(vendas_tempo, x="sale_date", y="revenue_usd", title="Evolução de Vendas")
    st.plotly_chart(fig_linha, use_container_width=True)

with col_pizza:
    fig_pizza = px.pie(df_filtrado, values="revenue_usd", names="category", title="Mix de Produtos")
    st.plotly_chart(fig_pizza, use_container_width=True)