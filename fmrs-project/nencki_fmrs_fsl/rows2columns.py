import pandas as pd

# Load the data
df = pd.read_csv('final_mean_passed.csv') 
met = 'Glu'

# Extract subject codes and regions
df['subj'] = df['code'].str.extract(r'(\d+)_')
df['code'] = df['code'].str.extract(r'\d+_(\w+)')

# Pivot the table to create separate columns for each region

col_names = [f'conc_{met}_{value}' for value in ['w500', 'w1000', 'w3000', 'w4500', 'b500', 'b1000', 'b3000', 'b4500']]

pivot_df = df.pivot(index='subj', columns='code', values=col_names)

# Reset index to make 'Subject' a regular column
pivot_df.reset_index(inplace=True)

# If you want to fill NaN values with empty cells
pivot_df = pivot_df.fillna('')

# Print the resulting DataFrame
print(pivot_df)

#save to csv
pivot_df.to_csv(f'{met}.csv', index=False,header=list(pivot_df.columns))