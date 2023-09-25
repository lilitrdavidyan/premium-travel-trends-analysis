import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_numerical_distributions(df, num_cols = 3):
    """
    This function receives a DataFrame and plots the distributions
    of all numerical columns in the DataFrame.
    """
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    num_plots = len(numerical_columns)
    num_rows = -(-num_plots // num_cols)  # Calculate the number of rows required with ceiling division
    
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
    
    if num_rows == 1:
        axs = [axs]
    
    for i, col in enumerate(numerical_columns):
        row = i // num_cols
        col_idx = i % num_cols
        sns.histplot(df[col], kde=False, ax=axs[row][col_idx])
        axs[row][col_idx].set_title(f'Distribution of {col}')
    
    plt.tight_layout()
    plt.show()


def plot_categorical_distributions(df, num_cols = 3):
    # Filter the dataframe to include only object (string) type columns, which are typically categorical
    categorical_columns = df.select_dtypes(include=['object']).columns
    
    num_plots = len(categorical_columns)
    num_cols = min(num_cols, num_plots)  # We will plot up to three columns in one row
    num_rows = (num_plots // num_cols) + (1 if num_plots % num_cols > 0 else 0)
    
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
    
    # If there is only one plot, axs is not an array, so we convert it to a numpy array for consistency in indexing
    if num_plots == 1:
        axs = np.array([axs])
    
    for i, col in enumerate(categorical_columns):
        row_idx = i // num_cols
        col_idx = i % num_cols
        ax = axs[row_idx, col_idx] if num_rows > 1 else axs[col_idx]
        
        # Plotting the bar plot for a categorical column
        sns.countplot(y=df[col], ax=ax)
        ax.set_title(f'Distribution of {col}')
        ax.set_xlabel('Count')
    
    plt.tight_layout()
    plt.show()