import pandas as pd

def preprocess_flipkart_data(input_file, output_file):
    # Load the CSV
    
    df = pd.read_csv(input_file)

    # Fill missing values with defaults
    df['Brand'] = df['Brand'].fillna("Unknown")
    df['Product Link'] = df['Product Link'].fillna("N/A")
    df['Price'] = df['Price'].fillna("0")
    df['Original Price'] = df['Original Price'].fillna("0")
    df['Discount'] = df['Discount'].fillna("0")

    # Remove duplicates
    df.drop_duplicates(subset=["Product Link"], inplace=True)

    # Remove currency symbols and convert to float
    df['Price'] = df['Price'].str.replace(r'[₹,]', '', regex=True).astype(float)
    df['Original Price'] = df['Original Price'].str.replace(r'[₹,]', '', regex=True)
    df['Original Price'] = pd.to_numeric(df['Original Price'], errors='coerce').fillna(0)

    # Extract numeric discount percentage
    df['Discount'] = df['Discount'].str.replace('% off', '', regex=False).str.strip()
    df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce').fillna(0)

    # Add column for computed discount % if missing
    df['Computed Discount %'] = round(((df['Original Price'] - df['Price']) / df['Original Price']) * 100, 2)
    df['Computed Discount %'] = df['Computed Discount %'].fillna(0).replace([float('inf'), -float('inf')], 0)

    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"✅ Cleaned data saved to: {output_file}")

# Run preprocessing
preprocess_flipkart_data('shoes.csv', 'cleaned_output.csv')
