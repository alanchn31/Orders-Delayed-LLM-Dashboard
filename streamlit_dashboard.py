import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="Nature's Basket Mart Supplier Orders Monitoring Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded")

# assume we have same number of orders as number of products
all_products = pd.read_csv("data/products_data.csv")
delays_data = pd.read_csv("data/product_delays_detailed.csv")

# Calculate Disruptions
disruptions_count = len(delays_data)
total_orders = len(all_products)
disruption_rate = (disruptions_count / total_orders) * 100
disruption_value = delays_data['value_of_items_delayed'].sum()

# Streamlit UI
st.title("📦 Supplier Order Disruptions Dashboard")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", total_orders)
col2.metric("Delayed Orders", disruptions_count)
col3.metric("Disruption Rate", f"{disruption_rate:.2f}%")
col4.metric("Total value of disrupted items", f"${disruption_value:,.2f}")

st.subheader("📉 Disruption by Supplier")
data_container = st.container()
with data_container:
    plot1, plot2 = st.columns(2)
    with plot1:
        disruption_counts = delays_data.groupby('supplier')['product_name'].count().reset_index()
        disruption_counts.rename(columns={'product_name': 'count_of_orders_disrupted'}, inplace=True)
        disruption_counts = disruption_counts.sort_values(by='count_of_orders_disrupted', ascending=False)
        fig1 = px.bar(disruption_counts, x='supplier', y='count_of_orders_disrupted', title="Number of orders disrupted by supplier", color='supplier')
        fig1.update_layout(showlegend=False, width=500)
        st.plotly_chart(fig1)
    with plot2:
        disruption_value = delays_data.groupby('supplier')['value_of_items_delayed'].sum().reset_index()
        disruption_value.rename(columns={'value_of_items_delayed': 'value_of_orders_delayed'}, inplace=True)
        disruption_value = disruption_value.sort_values(by='value_of_orders_delayed', ascending=False)
        fig2 = px.bar(disruption_value, x='supplier', y='value_of_orders_delayed', title="Value of orders delayed by supplier", color='supplier')
        fig2.update_layout(yaxis_tickformat="$,.2f", width=700)
        st.plotly_chart(fig2)
    # Ensure both figures share the same legend
    def sync_legends(fig, group, show_legend):
        fig.for_each_trace(lambda trace: trace.update(legendgroup=group, showlegend=show_legend))
    sync_legends(fig1, "suppliers", True)
    sync_legends(fig2, "suppliers", False)

# Data Table
st.subheader("📊 Order Details")
st.dataframe(delays_data
             .sort_values(by='value_of_items_delayed', ascending=False)
             .head(5)[['supplier', 'product_name', 'num_days_delay', 'lead_time', 
                       'days_of_inventory', 'additional_order_days', 'value_of_items_delayed']])

# Download more details about orders disruption
csv = delays_data.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Download Data as CSV", data=csv, file_name="supplier_disruptions.csv", mime="text/csv")
