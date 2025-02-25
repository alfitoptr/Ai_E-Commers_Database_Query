## AI-Powered E-Commerce Database Query Assistant

**Overview**
This project is an AI-powered database query assistant that helps users interact with a PostgreSQL database using natural language. The application is built with Streamlit, LangChain, and Google Gemini AI, enabling automatic SQL query generation and insightful data analysis.

The dataset used in this project is the Olist E-Commerce Dataset, which contains transactional data from a Brazilian e-commerce marketplace between 2017 and 2018.

**Project Structure**
```bash
│── app.py              # Main Streamlit application
│── prompts.py          # Prompt templates for AI-generated SQL queries
│── requirements.txt    # List of dependencies
│── README.md           # Project documentation
```

**Features**

✅ Natural Language Querying: Users can input database-related questions, and the AI will generate SQL queries automatically.

✅ SQL Query Execution: The generated SQL queries are executed on a PostgreSQL database.

✅ AI-Powered Insights: The AI provides meaningful insights based on query results.

✅ Dual-Tab Interface:
- Dataset Overview: Explanation of the Olist dataset.**
- AI Assistant: SQL generation and insights panel.

🛠 **Installation**
Clone the Repository
```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```
```
Install Dependencies
```bash
pip install -r requirements.txt
```

**Set Up Environment Variables**
Create a .env file in the project directory and add the following:
```bash
api_key=your_google_api_key
DB_URL=your_postgresql_connection_string
```

Running the Application
```bash
streamlit run app.py
```

**Dataset Overview**
The Olist E-Commerce Dataset consists of multiple tables, including:

- orders: Order details (purchase date, delivery, status).
- customers: Customer data (ID, location).
- order_items: Order item details (product ID, price, quantity).
- products: Product information (name, category, weight, dimensions).
- sellers: Seller details (ID, location, products sold).
- reviews: Customer reviews (ratings, comments).
- geolocation: Location data (latitude, longitude by postal code).


**Technologies Used**
- Python
- Streamlit
- PostgreSQL
- LangChain
- Google Gemini AI

**License**
This project is licensed under the MIT License.
