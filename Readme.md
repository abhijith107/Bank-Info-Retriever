IFSC Code Lookup Tool
Overview
The IFSC Code Lookup Tool is a Python-based application designed to fetch detailed banking information using IFSC codes. It can process individual IFSC code inputs or bulk requests via an Excel file, making it a versatile tool for law enforcement agencies and financial analysts.

Features
Single IFSC Code Lookup: Enter an IFSC code to retrieve associated bank details, such as branch name, address, city, district, state, and bank name.
Bulk IFSC Code Lookup: Upload an Excel file containing multiple IFSC codes and receive a comprehensive report with details for each code.
Integration with Razorpay IFSC API: Fetch real-time information using the Razorpay IFSC API to ensure up-to-date and accurate data.

Installation
Clone the Repository:  git clone https://github.com/yourusername/ifsc-code-lookup-tool.git
                       cd ifsc-code-lookup-tool

Set Up API Keys:

Obtain an API key from Razorpay for the IFSC API.

Create a .env file in the root directory and add your API key: RAZORPAY_API_KEY=your_api_key_here

Run application - streamlit run ifscsearch.py
