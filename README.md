# orders_disruption_llm_dashboard

1. gen_synthetic_product_data generates 100 records of synthetic product data using a LLM
2. gen_synthetic_emails generates 20 emails of items shipments being delayed
3. reorder_calculations calculates the amount of items to reorder and reorder date, assuming the inventory policy is continous

streamlit_dashboard.py generates a dashboard showing a summary of products with orders disrupted, and their value by supplier.

![alt text](pics/supplier_orders_disruption_dash1.png)
![alt text](pics/supplier_orders_disruption_dash2.png)