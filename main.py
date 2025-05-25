# main.py
import streamlit as st
from a import main as upi_main
from banks_kpi import main as analytics_main

# Configure page
st.set_page_config(page_title="Multi-Page App", page_icon="🚀", layout="wide")

# Create sidebar navigation
st.sidebar.title("📱 Navigation")
page = st.sidebar.selectbox(
    "Select a page:",
    ["🏠 Home", "📊 UPI Dashboard", "📈 Analytics"]
)

st.title("🏛️ UPI Transaction Data Analysis-Indian Banking Sector Performance")
# Show content based on selection
if page == "🏠 Home":
    st.markdown("""
### 🔍 Project Context

India has witnessed exponential growth in digital payments, particularly through the Unified Payments Interface (UPI). With over **10 billion UPI transactions per month**, there's a growing need to understand **how different banks perform** in this rapidly evolving ecosystem.

Our goal was to create a **data-driven performance analysis** of Indian banks in the UPI ecosystem by comparing transaction volume, success rates, and market share trends — using publicly available web data.

---

### 🎯 Why This Project?

- There is **no single API or open-source dataset** that aggregates this info comprehensively.
- Banks publish monthly or quarterly UPI data across different formats, mostly unstructured.

---

### ⚙️ Data Extraction Approach

To solve this challenge, we:

- Built a **custom web scraping pipeline** using `BeautifulSoup` and `Selenium`.
- Targeted official website of NPCI
- Cleaned and structured the data using `Pandas` and `NumPy`.

Example code snippet for scraping (simplified):

```python
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://examplebank.com/upi-transactions")

soup = BeautifulSoup(driver.page_source, 'html.parser')
data_table = soup.find("table", {"id": "upi-data"})
```

---
### 🧮SQL Integration 
I stored all the extracted data in a SQL database, which allowed me to:

Run comparative queries like bank-wise growth, failure rates, etc.

Create year-over-year analysis to track performance improvement.

---

### 🧠 Key Takeaways
Some banks consistently maintain high success rates, while others show volatility.

Private sector banks tend to lead in transaction volumes, but public sector banks are catching up.

### 🛠️ Tools & Technologies Used
Python – Data handling

BeautifulSoup, Selenium – Web scraping

SQL – Querying and storing structured data

NumPy, Pandas – Data cleaning & processing



""")


    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📊 **UPI Dashboard**\n\nView UPI transaction analytics and market insights")
    with col2:
        st.info("📈 **Analytics**\n\nExplore detailed data analysis and reports")

elif page == "📊 UPI Dashboard":
    upi_main()
    
elif page == "📈 Analytics":
    analytics_main()