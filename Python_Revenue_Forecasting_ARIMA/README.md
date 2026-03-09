# Revenue Forecast Using ARIMA (Time Series Analysis)

## Project Overview

This project focuses on forecasting monthly revenue using time series modeling.  
The objective is to analyze historical revenue dynamics and build a statistical model capable of predicting short-term financial performance.

The analysis is based on historical e-commerce revenue data aggregated at the monthly level.

---

## Business Context

Revenue forecasting plays a critical role in financial planning and operational decision-making.

By analyzing historical revenue patterns, businesses can estimate future sales performance, plan budgets, and optimize resource allocation.

The goal of this project is to develop a time series forecasting model that captures revenue trends and generates short-term forecasts.

---

## Dataset

The dataset contains:

- **24 months of historical revenue**
- **monthly aggregated sales data**
- source: e-commerce transaction data

The dataset represents the revenue dynamics of an e-commerce platform over time.

Due to data privacy restrictions, the original dataset is not included in this repository.

---

## Tools and Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Statsmodels
- Jupyter Notebook

---

## Methodology

### 1. Time Series Exploration

- visualization of historical revenue trends
- identification of growth patterns
- volatility analysis

The revenue series shows a clear upward trend, typical for a scaling e-commerce business.

---

### 2. Stationarity Testing

To build a reliable ARIMA model, the time series must be stationary.

The **Augmented Dickey-Fuller (ADF) test** was used to evaluate stationarity.

Results:

- original series → **non-stationary**
- after **first differencing** → **stationary**

---

### 3. Model Identification

Autocorrelation (ACF) and partial autocorrelation (PACF) plots were used to identify suitable ARIMA parameters.

Candidate models were evaluated using metrics such as:

- AIC
- MAE
- RMSE

---

### 4. Model Selection

The selected model:

**ARIMA(1,1,0)**

This model provided the best balance between model complexity and predictive performance.

---

### 5. Revenue Forecast

The model generates a **6-month revenue forecast**.

The forecast suggests that:

- revenue stabilizes around **~1.0–1.1M**
- forecast uncertainty increases over time
- short-term forecasts are more reliable than long-term projections

---

## Key Insights

- Revenue demonstrates a clear upward growth trajectory.
- Volatility increases as the business scales.
- The ARIMA model captures short-term revenue momentum.
- Forecast uncertainty increases due to the limited historical dataset.

The forecast is therefore most useful for **short-term operational planning and budgeting**.

---

📊 ** Presentation **

A detailed explanation of the analysis and modeling process is available in the presentation:

🔗 [View Project Presentation](https://drive.google.com/file/d/1tvWO63pTwZA4am3YInCIgPBGjzXeQPvS/view?usp=sharing)
