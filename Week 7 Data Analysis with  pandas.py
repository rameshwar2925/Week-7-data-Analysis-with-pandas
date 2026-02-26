# main.py - Complete Sales Data Analysis Dashboard

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

class SalesAnalyzer:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.load_data()

    # ----------------------------
    # Step 1: Load Data
    # ----------------------------
    def load_data(self):
        try:
            if self.file_path.endswith('.csv'):
                self.df = pd.read_csv(self.file_path)
            elif self.file_path.endswith('.xlsx'):
                self.df = pd.read_excel(self.file_path)
            else:
                raise ValueError("Unsupported file format")

            print("✅ Data Loaded Successfully!")
            print("Shape:", self.df.shape)

            if 'order_date' in self.df.columns:
                self.df['order_date'] = pd.to_datetime(self.df['order_date'])

        except Exception as e:
            print("❌ Error loading file:", e)

    # ----------------------------
    # Step 2: Data Cleaning
    # ----------------------------
    def clean_data(self):
        print("\n🧹 Cleaning Data...")

        # Remove duplicates
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        after = len(self.df)
        print(f"Removed {before - after} duplicate rows")

        # Handle missing values
        numeric_cols = self.df.select_dtypes(include=np.number).columns
        categorical_cols = self.df.select_dtypes(include='object').columns

        for col in numeric_cols:
            self.df[col].fillna(self.df[col].median(), inplace=True)

        for col in categorical_cols:
            self.df[col].fillna(self.df[col].mode()[0], inplace=True)

        print("Missing values handled.")

    # ----------------------------
    # Step 3: Basic Statistics
    # ----------------------------
    def basic_stats(self):
        print("\n📊 BASIC STATISTICS")
        print("="*40)

        total_sales = self.df['total_amount'].sum()
        avg_sale = self.df['total_amount'].mean()
        total_orders = len(self.df)
        unique_customers = self.df['customer_id'].nunique()

        print(f"Total Sales: ₹{total_sales:,.2f}")
        print(f"Average Order Value: ₹{avg_sale:,.2f}")
        print(f"Total Orders: {total_orders}")
        print(f"Unique Customers: {unique_customers}")

    # ----------------------------
    # Step 4: Sales by Category
    # ----------------------------
    def sales_by_category(self):
        print("\n🏆 Sales by Category")
        category = self.df.groupby('category')['total_amount'].sum().sort_values(ascending=False)
        print(category)
        return category

    # ----------------------------
    # Step 5: Monthly Trends
    # ----------------------------
    def monthly_trends(self):
        print("\n📅 Monthly Sales Trends")

        self.df['month'] = self.df['order_date'].dt.to_period('M')
        monthly = self.df.groupby('month')['total_amount'].sum()

        growth = monthly.pct_change() * 100
        result = pd.DataFrame({
            'Total Sales': monthly,
            'Growth %': growth
        })

        print(result)
        return result

    # ----------------------------
    # Step 6: Visualization
    # ----------------------------
    def visualize(self):
        os.makedirs("reports", exist_ok=True)

        # Monthly Trend Line Chart
        monthly = self.monthly_trends()

        plt.figure(figsize=(10,5))
        monthly['Total Sales'].plot(kind='line', marker='o')
        plt.title("Monthly Sales Trend")
        plt.xlabel("Month")
        plt.ylabel("Sales")
        plt.grid()
        plt.tight_layout()
        plt.savefig("reports/monthly_sales.png")
        plt.close()

        # Category Bar Chart
        category = self.sales_by_category()
        plt.figure(figsize=(8,5))
        category.plot(kind='bar')
        plt.title("Sales by Category")
        plt.xlabel("Category")
        plt.ylabel("Sales")
        plt.tight_layout()
        plt.savefig("reports/category_sales.png")
        plt.close()

        # Pie Chart
        plt.figure(figsize=(6,6))
        category.head(5).plot(kind='pie', autopct='%1.1f%%')
        plt.title("Top 5 Categories Share")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig("reports/category_pie.png")
        plt.close()

        print("📈 Visualizations saved in 'reports/' folder.")

    # ----------------------------
    # Step 7: Export Report
    # ----------------------------
    def export_report(self):
        os.makedirs("reports", exist_ok=True)

        with pd.ExcelWriter("reports/sales_report.xlsx", engine='openpyxl') as writer:
            self.df.to_excel(writer, sheet_name="Cleaned Data", index=False)
            self.monthly_trends().to_excel(writer, sheet_name="Monthly Trends")
            self.sales_by_category().to_excel(writer, sheet_name="Category Analysis")

        print("📁 Excel Report Generated Successfully!")

    # ----------------------------
    # CLI Menu
    # ----------------------------
    def run_dashboard(self):
        while True:
            print("\n📊 SALES DASHBOARD MENU")
            print("1. View Basic Statistics")
            print("2. View Sales by Category")
            print("3. View Monthly Trends")
            print("4. Generate Visualizations")
            print("5. Export Excel Report")
            print("6. Exit")

            choice = input("Enter choice: ")

            if choice == '1':
                self.basic_stats()
            elif choice == '2':
                self.sales_by_category()
            elif choice == '3':
                self.monthly_trends()
            elif choice == '4':
                self.visualize()
            elif choice == '5':
                self.export_report()
            elif choice == '6':
                print("Exiting Dashboard.")
                break
            else:
                print("Invalid choice!")

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    file_path = input("Enter path to sales data (CSV/Excel): ")
    analyzer = SalesAnalyzer(file_path)
    analyzer.clean_data()
    analyzer.run_dashboard()