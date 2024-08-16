import streamlit as st
import requests
import pandas as pd
from io import BytesIO
import os
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

def fetch_ifsc_details(ifsc_code):
    url = f"https://ifsc.razorpay.com/{ifsc_code.strip()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extract all possible fields from the API response
        if 'IFSC' in data:
            details = {
                'Bank Name': data.get('BANK', 'N/A'),
                'Branch': data.get('BRANCH', 'N/A'),
                'Address': data.get('ADDRESS', 'N/A'),
                'City': data.get('CITY', 'N/A'),
                'State': data.get('STATE', 'N/A'),
                'District': data.get('DISTRICT', 'N/A'),
                'Centre': data.get('CENTRE', 'N/A'),
                'Contact': data.get('CONTACT', 'N/A'),
                'IFSC Code': data.get('IFSC', 'N/A'),
                'MICR Code': data.get('MICR', 'N/A'),
                'SWIFT Code': data.get('SWIFT', 'N/A'),
                'RTGS': 'Yes' if data.get('RTGS', False) else 'No',
                'NEFT': 'Yes' if data.get('NEFT', False) else 'No',
                'IMPS': 'Yes' if data.get('IMPS', False) else 'No',
                'UPI': 'Yes' if data.get('UPI', False) else 'No',
                'ISO3166': data.get('ISO3166', 'N/A')
            }
            return details
        else:
            return {'Error': 'Invalid IFSC code or details not found'}
    except requests.RequestException as e:
        return {'Error': f'An error occurred: {e}'}

def main():
    st.title("IFSC Code Lookup")

    # Option to search for a single IFSC code
    st.header("Search Single IFSC Code")
    ifsc_code_single = st.text_input("Enter IFSC Code:")
    if st.button("Fetch Single IFSC Details"):
        if not ifsc_code_single:
            st.warning("Please enter an IFSC code")
        else:
            details = fetch_ifsc_details(ifsc_code_single)
            if 'Error' in details:
                st.error(details['Error'])
            else:
                st.write("### Bank Details:")
                for key, value in details.items():
                    st.write(f"**{key}:** {value}")

    # Option to upload an Excel file with multiple IFSC codes
    st.header("Upload Excel File with IFSC Codes")
    uploaded_file = st.file_uploader("Upload an Excel file with IFSC codes", type=["xlsx"])

    if uploaded_file:
        if st.button("Process IFSC Codes"):
            try:
                # Read the uploaded Excel file
                df = pd.read_excel(uploaded_file)

                # Check if the required column 'IFSC Code' exists
                if 'IFSC Code' not in df.columns:
                    st.error("The Excel file must contain a column named 'IFSC Code'")
                else:
                    details_list = []
                    # Iterate over each IFSC code and fetch details
                    for ifsc_code in df['IFSC Code'].dropna():
                        if isinstance(ifsc_code, str):  # Ensure IFSC code is a string
                            details = fetch_ifsc_details(ifsc_code)
                            if 'Error' not in details:
                                details_list.append(details)
                            else:
                                details_list.append({
                                    'Bank Name': 'N/A',
                                    'Branch': 'N/A',
                                    'Address': 'N/A',
                                    'City': 'N/A',
                                    'State': 'N/A',
                                    'District': 'N/A',
                                    'Centre': 'N/A',
                                    'Contact': 'N/A',
                                    'IFSC Code': ifsc_code,
                                    'MICR Code': 'N/A',
                                    'SWIFT Code': 'N/A',
                                    'RTGS': 'N/A',
                                    'NEFT': 'N/A',
                                    'IMPS': 'N/A',
                                    'UPI': 'N/A',
                                    'ISO3166': 'N/A'
                                })
                    
                    # Add the details to the original DataFrame
                    details_df = pd.DataFrame(details_list)
                    combined_df = pd.concat([df.reset_index(drop=True), details_df.reset_index(drop=True)], axis=1)
                    
                    # Save the output file to the same directory
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        combined_df.to_excel(writer, index=False, sheet_name='IFSC Details')
                    
                    output_path = os.path.join(os.getcwd(), "ifsc_details_combined.xlsx")
                    with open(output_path, 'wb') as f:
                        f.write(output.getvalue())
                    
                    st.success(f"File saved as {output_path}")
                    st.download_button(
                        label="Download IFSC Details",
                        data=output.getvalue(),
                        file_name="ifsc_details_combined.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
