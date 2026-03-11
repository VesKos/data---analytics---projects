# 📊 Customer Retention & Cohort Revenue Analysis

## Project Overview
This project analyzes customer behavior in an e-commerce dataset using cohort analysis.  
The goal is to understand how customers behave after their first purchase and how different cohorts contribute to revenue over time.

The dataset was cleaned and prepared in **Python**, and the results were visualized in **Tableau**.

---

## 🛠 Tools Used

- Python (pandas, numpy)
- Tableau

---

## 📦 Dataset

Online Retail dataset containing transactional data from an e-commerce business.

Main fields include:
- Invoice
- Quantity
- Price
- InvoiceDate
- Customer ID
- Country

---

## 🧹 Data Preparation (Python)

The dataset was cleaned and transformed using Python before being used in the visualization.

Main steps:

- removing cancelled orders
- filtering invalid quantities and prices
- handling missing customer IDs
- creating a revenue column
- generating cohort features

Key cohort fields created:

- `cohort_month`
- `order_month`
- `cohort_index`

---

## 📊 Dashboard Overview

The interactive Tableau dashboard includes:

### KPI Metrics
- Total Revenue
- Total Customers
- ARPU
- Repeat Purchase Rate
- Month-1 Retention

### Visualizations
- Cohort Revenue Chart
- Customer Retention Heatmap
- Cohort Size Analysis
- Geographic Revenue Map

The dashboard includes filters that allow the analysis to be explored by:

- Country
- Order Period
- Cohort Month

---

## 🔎 Key Insights

Some interesting patterns observed:

- Retention drops significantly after the first month.
- Revenue growth is largely driven by newly acquired customer cohorts.
- Customer behavior varies across different countries.

---

## 📈 Interactive Dashboard

Tableau Public dashboard:

👉 [[Tableau link](https://public.tableau.com/app/profile/vesna.kostrewa/viz/CustomerRetentionCohortRevenueAnalysis/Dashboard1)]

---

