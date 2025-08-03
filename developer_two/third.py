import pandas as pd

def explore_csv(file_path):
    # Load CSV file
    df = pd.read_csv(file_path)
    
    # Display basic info
    print("Shape:", df.shape)
    print("\nColumns:", df.columns.tolist())
    print("\nData Types:\n", df.dtypes)
    print("\nMissing Values:\n", df.isnull().sum())
    print("\nSummary Statistics:\n", df.describe(include='all'))
    print("\nFirst 5 Rows:\n", df.head())

if __name__ == "__main__":
    csv_path = input("Enter path to CSV file: ")
    explore_csv(csv_path)