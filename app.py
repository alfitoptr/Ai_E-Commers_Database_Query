import os
import re

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from psycopg2 import pool  # noqa: F401

from prompts import get_sql_prompt

API_KEY = st.secrets["api_key"]
DB_URL = st.secrets["DB_URL"]

# AI Model
sql_generator = GoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=API_KEY)
insight_generator = GoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=API_KEY)

# Database Connection Pool
connection_pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=10, dsn=DB_URL)


def clean_sql_query(sql_query):
    cleaned_query = sql_query.replace("\\n", " ").replace("\\", "")
    cleaned_query = re.sub(r"```sql|```", "", cleaned_query).strip()
    cleaned_query = re.sub(r"\s+", " ", cleaned_query).strip()
    return cleaned_query


def execute_query(sql_query):
    conn = None
    cursor = None
    try:
        conn = connection_pool.getconn()
        if conn is None:
            return None, "Failed to get a database connection"

        cursor = conn.cursor()
        cursor.execute(sql_query)
        query_result = cursor.fetchall()

        col_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(query_result, columns=col_names)

        return df, None
    except Exception as e:
        return None, f"Database error: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)


def generate_insight(user_query, df):
    if df.empty:
        return "No data was returned from the query. This could be due to missing records, restrictive filters, or an issue with the query logic."

    table_output = df.to_string(index=False)

    insight_prompt = f"""
    You are an expert data analyst. Your task is to analyze the SQL result and generate meaningful insights.

    Instructions:
    - Interpret the SQL result **ONLY** based on the user query.
    - **DO NOT** make up data that is not present in the SQL result.
    - Provide concise yet informative insights in a well-structured paragraph.

    User Question:
    {user_query}

    SQL Result (Table Format):
    ```
    {table_output}
    ```

    Insight:
    """

    final_response = insight_generator.invoke(insight_prompt)
    return final_response


st.title("E-Commerce AI Query Assistant")

tab1, tab2 = st.tabs(["📖 Dataset Overview", "🤖 AI Assistant"])

# TAB 1: Dataset Overview
with tab1:
    st.header("Olist E-Commerce Dataset")
    st.write("""
    **Olist Dataset** is a collection of data from a Brazilian e-commerce marketplace.  
    This dataset includes transactions, customers, products, reviews, and product categories.  

    Below are some of the main tables in the dataset:
    - **`orders`**: Order details (purchase time, delivery, order status).
    - **`customers`**: Customer data (customer ID, location).
    - **`order_items`**: Details of items in an order (product ID, price, quantity).
    - **`products`**: Product information (name, category, weight, dimensions).
    - **`sellers`**: Seller details (ID, location, number of products sold).
    - **`reviews`**: Customer reviews (rating, comments).
    - **`geolocation`**: Location data (latitude, longitude based on postal code).

    **Note:**  
    - The dataset contains records from **2017 to 2018**.  
    - **Please provide a question, not just a command, and be as specific as possible.**  

    **Use the AI Assistant tab to generate SQL queries automatically!**
    """)

# TAB 2: AI Assistant
with tab2:
    st.header("AI Database Query Assistant")
    st.write("💡 **Examples of questions you can ask:**")
    st.markdown("""
    - What was the total sales in 2018?
    - Which 5 product categories generate the highest revenue?
    - What is the distribution of product ratings from customers?
    - Which cities have the highest number of orders?
    """)

    user_query = st.text_area(
        "Enter your database-related question:",
        placeholder="Example: What was the total sales in 2018?",
    )

    if st.button("Generate"):
        if user_query:
            # AI Generate SQL Query
            sql_prompt = get_sql_prompt(user_query)
            sql_query = sql_generator.invoke(sql_prompt)
            sql_query = clean_sql_query(sql_query)

            # Execute SQL Query
            df, error = execute_query(sql_query)
            if error:
                st.error(
                    "I don't know. Please provide a question, not just a command, and be as specific as possible"
                )
            else:
                st.subheader("Query Result")
                st.dataframe(df)

                st.subheader("AI Insights")
                insight = generate_insight(user_query, df)
                st.text_area("AI Insights", insight, height=250)
        else:
            st.warning("Please enter a question first.")
