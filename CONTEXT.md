# These are the files and columns
Category,Files,Key Columns
Core Sales,"orders, order_items","order_id, product_id, customer_id"
Users,"customers, customer_feedback","customer_id, rating, sentiment"
Logistics,"delivery_performance, inventory","delivery_time, stock_received, distance_km"
Catalog/Ads,"products, marketing_performance","category, brand, clicks, revenue_generated"


Q-Comm Pulse: Interactive Visual Analytics Framework for Last-Mile Delivery Optimization and Inventory Health
1. Project Overview

Project Title:
Q-Comm Pulse: An Interactive Visual Analytics Framework for Last-Mile Delivery Optimization and Inventory Health

Objective

The goal of this project is to transform a fragmented 11-file Blinkit dataset into a professional Business Intelligence Command Center capable of solving real-world logistics and profitability challenges in quick-commerce operations.

The system integrates data engineering, visual analytics, and machine learning to analyze delivery performance, inventory health, marketing efficiency, and customer sentiment.

Target Impact

The project is designed to achieve a high evaluation score (50–75 marks) by demonstrating:

Advanced data visualization

Clean data architecture

Machine learning integration

Real business problem solving

Execution Model

Currently the system is being built by a Solo Lead Developer (you), with plans to expand into a 4-person team structure:

Role	Responsibility
Lead Developer	Architecture, ML model, data pipeline
Data Engineer	Data ingestion and preprocessing
Data Analyst	KPI design and insights
Visualization Specialist	Dashboard UX/UI
QA & Documentation	Testing and reporting
2. Core Mission

The project addresses the “Last-Mile Delivery Problem” in quick commerce.

The mission is to convert multiple raw datasets into a single “Golden Dataset” that powers a real-time operations intelligence system.

The platform helps businesses:

Predict delivery delays

Detect inventory wastage

Improve customer satisfaction

Evaluate marketing campaign efficiency

3. Technical Ecosystem
Hardware

Processor: Intel i5 (12th Gen)

RAM: 16 GB

GPU: NVIDIA RTX 3050 (6GB)

Development Environment

Conda Environment: mini_project

Python Version: Python 3.12

Key Libraries

pandas – data processing

openpyxl – Excel file handling

streamlit – interactive dashboard

Development Tools

VS Code

GitHub Copilot & Copilot Chat (AI pair programming)

Version Control

GitHub repository linked with local project directory:

C:\Users\WELCOME\Downloads\blinkit_dataset
4. Data Architecture

The project integrates 11 datasets representing different operational domains.

4.1 Sales & Product Data

blinkit_orders

blinkit_order_items

blinkit_products

These files contain order transactions, item details, and product metadata.

4.2 Logistics Data

blinkit_delivery_performance

Includes delivery timings and operational metrics used for delay prediction.

4.3 Inventory Management

blinkit_inventory

blinkit_inventoryNew

Tracks stock levels, damage rates, and shelf life.

4.4 Customer Data

blinkit_customers

blinkit_customer_feedback

Provides customer profiles and satisfaction ratings.

4.5 Marketing Data

blinkit_marketing_performance

Tracks advertising campaign performance.

4.6 Visual Branding Assets

Category_Icons.xlsx

Rating_Icon.xlsx

Used for UI aesthetics in the dashboard.

5. Key Business Problems Addressed
5.1 The “Late-to-Angry” Pipeline

This analysis links delivery delays to negative customer feedback.

Key variables analyzed:

promised_time

actual_time

delivery delay

The goal is to identify operational issues before they impact customer satisfaction.

5.2 Inventory Shrinkage Detection

The system identifies product categories with high wastage rates.

Key metrics:

damaged_stock

shelf_life_days

This helps warehouse managers reduce inventory losses.

5.3 Marketing Efficiency (ROAS)

The system calculates Return on Ad Spend (ROAS) to determine which campaigns attract high-value customers.

This enables more effective marketing budget allocation.

6. Data Engineering Pipeline

A robust data preprocessing pipeline was built to convert raw files into a unified analytical dataset.

Step 1 – Data Cleaning

Performed in a Jupyter Notebook.

Tasks include:

Standardizing column names

Converting time strings into datetime

Removing null values

Eliminating impossible outliers

Step 2 – Master Merge

All datasets are merged using shared identifiers:

order_id

customer_id

product_id

The output is a centralized “Golden Dataset” used by both the dashboard and machine learning model.

Step 3 – Feature Engineering

New analytical features were created:

Feature	Purpose
delay_minutes	Measures delivery delay
profit_margin	Business profitability metric
wastage_rate	Inventory damage ratio
time_slot	Peak delivery periods (Morning/Evening)

These features improve model performance and business insight generation.

7. Visualization System (Streamlit Dashboard)

A Streamlit-based web dashboard acts as the central interface.

Dashboard Features

Management KPIs

Total revenue

Total orders

Delay percentage

Operational Tabs

Tab	Function
Operations	Logistics performance analysis
Inventory	Inventory health and wastage tracking
Customer Retention	Sentiment and satisfaction insights
Executive Summary System

An automated Action Alert System highlights:

Worst performing delivery zones

High wastage product categories

Declining customer satisfaction

This allows managers to take immediate action.

8. Machine Learning Intelligence Layer

The project integrates a Random Forest Classifier to predict delivery delays.

The algorithm belongs to the field of Machine Learning.

8.1 Problem: Class Imbalance

Most deliveries are on-time, causing the model to bias toward predicting “on-time”.

This creates an imbalanced dataset problem.

8.2 Solutions Implemented
One-Hot Encoding

Categorical variables such as geographic zones were encoded for better model accuracy.

Threshold Adjustment

Instead of the default 0.5 threshold, the model uses 0.4–0.5 to prioritize catching late deliveries.

This increases Recall, ensuring more potential delays are detected.

8.3 Model Outcome

The trained model can identify approximately:

~51% of potential late deliveries

This acts as an early warning system for warehouse and logistics managers.

9. Professional Data Science Practices

Several professional workflows were implemented:

Data Denoising

Outliers and corrupt values were removed to prevent computational errors such as divide-by-zero.

Trade-Off Analysis

The project documents why False Negatives (missing late deliveries) are more harmful than False Positives (extra alerts).

Scalability

The system processes:

5000+ records

300+ encoded features

without performance issues.

10. Development Workflow with Copilot

GitHub Copilot is used as an AI pair programmer.

Prompting Protocol

Use conversational prompts

Provide context with #file

Documentation Command
/doc

Automatically generates documentation for team members.

11. Current Project Status

The core system is fully operational.

Completed components include:

Data cleaning pipeline

Golden dataset creation

Feature engineering

Streamlit dashboard structure

Random Forest delay prediction model

The project is now ready for team expansion and feature enhancement.

12. Next Development Phase

The immediate next task is integrating the Prediction Interface.

Predictor Tab (Planned)

The dashboard will allow users to:

Input order details

Run the trained model (.joblib)

Predict delivery risk in real time

This will transform the dashboard into a decision-support tool for logistics managers.

13. Project Value

This project demonstrates a complete end-to-end data science pipeline:

Data engineering

Business analytics

Machine learning

Interactive visualization

Operational decision support

The result is a Q-Commerce Operations Intelligence System capable of reducing delivery delays, minimizing inventory waste, and improving customer satisfaction.