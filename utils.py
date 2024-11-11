import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

# Get list of days of the week
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def generate_energy_summary(data, datetime_column='datetime', kwh_column='kwh', kw_column='kw'):
    # Determine the frequency based on the time intervals in the datetime column
    interval_seconds = data[datetime_column].diff().dt.total_seconds().median()
    frequency = 12 if interval_seconds == 300 else 1  # 12 for 5 minutes, 1 for 1 hour

    # Group by supply period and aggregate the necessary columns
    energy_summary = data.groupby("supply period", sort=False).agg({
        "supply period": "count",
        kwh_column: "sum",
        kw_column: "max"
    })

    # Rename columns for readability
    energy_summary.columns = ["number of intervals", "kwh", "kw"]

    # Calculate 'number of hours' based on frequency and drop 'number of intervals'
    energy_summary["number of hours"] = energy_summary["number of intervals"] / frequency
    energy_summary.drop(columns=["number of intervals"], inplace=True)

    # Add a total row with the sum of kWh and the max of kW
    energy_summary.loc["Total"] = energy_summary.sum()
    energy_summary.loc["Total", "kw"] = energy_summary.iloc[:-1]["kw"].max()

    # Calculate the load factor
    energy_summary["load factor"] = (energy_summary["kwh"] / (energy_summary['kw'] * energy_summary["number of hours"])) * 100

    # Create a copy of the summary data without the Total row for statistics
    original_energy_summary = energy_summary.iloc[:-1].copy()

    # Add Average, Max, Min rows based on the original data (excluding 'Total')
    energy_summary.loc["Average"] = original_energy_summary.mean()
    energy_summary.loc["Max"] = original_energy_summary.max()
    energy_summary.loc["Min"] = original_energy_summary.min()

    # Reset index to remove 'supply period' from being the index
    energy_summary = energy_summary.reset_index()

    # Reorder columns as specified
    energy_summary = energy_summary[["supply period", "number of hours", "kwh", "kw", "load factor"]]

    # Format columns to display numbers with 2 decimal places and comma separators
    energy_summary["number of hours"] = energy_summary["number of hours"].apply(lambda x: "{:,.2f}".format(x))
    energy_summary["kwh"] = energy_summary["kwh"].apply(lambda x: "{:,.2f}".format(x))
    energy_summary["kw"] = energy_summary["kw"].apply(lambda x: "{:,.2f}".format(x))
    energy_summary["load factor"] = energy_summary["load factor"].apply(lambda x: "{:,.2f}".format(x))

    return energy_summary

def plot_hourly_load_curve(hourly_summary, column_name='max', unit='MW', ylabel='Peak Demand', ylim: list = None):
  if ylim is not None:
    assert ylim[0] < ylim[1], "ylim should be a list with 2 elements, where the first element is less than the second."

  # Create figure and axis
  fig, ax = plt.subplots(figsize=(15, 5))

  # Plot
  hourly_summary[column_name].plot(
    ax=ax, kind='area',
    legend=True, color='#ff7f0e',
    label=f'{ylabel} ({unit})'
  )

  # Set x- and y-axis labels
  ax.set_xlabel("Hour")
  plt.ylabel(f'{ylabel} ({unit})')

  # Set y-axis minimum to 0
  if ylim is not None:
    ax.set_ylim(bottom=ylim[0], top=ylim[1])

  # Show y-axis ticks 0,000.00
  ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,.2f}".format(x)))

  # Show all x-ticks
  ax.set_xticks(hourly_summary.index)

  # Get list of existing legend
  legend = [l.get_text() for l in ax.get_legend().get_texts()]
  # Place legend at the bottom of the plot
  ax.legend(
    legend,
    loc='upper center',
    bbox_to_anchor=(0.5, 0.99),
    bbox_transform=fig.transFigure,
    ncol=len(legend),
  )

  # Set x-ticks to be horizontal
  plt.xticks(rotation=0)

  # Set font to Poppins
  # Load Poppins font
  plt.rcParams['font.family'] = 'Poppins'

  # Remove border box
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_visible(False)
  ax.spines['bottom'].set_visible(False)

  # Add gray horizontal gridlines
  ax.yaxis.grid(color='gray', linestyle='-', linewidth=0.25)

  # Remove y-axis ticks only (keep labels)
  ax.tick_params(axis='y', which='both', left=False)

  # Remove x-axis ticks only (keep labels)
  ax.tick_params(axis='x', which='both', bottom=False)

  plt.show()


def plot_hourly_by_day_load_curve(hourly_by_day_summary, column_name='max', unit='MW', ylabel='Peak Demand', ylim: list = None):
  if ylim is not None:
    assert ylim[0] < ylim[1], "ylim should be a list with 2 elements, where the first element is less than the second."

  # Create figure and axis
  fig, ax = plt.subplots(figsize=(15, 5))

  # Plot
  hourly_by_day_summary.plot(
    ax=ax, kind='line',
    legend=True, colormap='tab10',
    label=f'{ylabel} ({unit})'
  )

  # Set x- and y-axis labels
  ax.set_xlabel("Hour")
  ax.set_ylabel(f'{ylabel} ({unit})')

  # Set y-axis minimum to 0
  if ylim is not None:
    ax.set_ylim(bottom=ylim[0], top=ylim[1])

  # Show y-axis ticks 0,000.00
  ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,.2f}".format(x)))

  # Show all x-ticks
  ax.set_xticks(hourly_by_day_summary.index)

  # Get list of existing legend
  legend = days_of_week
  # Place legend at the bottom of the plot
  ax.legend(
    legend,
    loc='upper center',
    bbox_to_anchor=(0.5, 0.99),
    bbox_transform=fig.transFigure,
    ncol=len(legend),
  )

  # Set x-ticks to be horizontal
  plt.xticks(rotation=0)

  # Set font to Poppins
  # Load Poppins font
  plt.rcParams['font.family'] = 'Poppins'

  # Remove border box
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_visible(True)
  ax.spines['bottom'].set_visible(True)

  # Add gray horizontal gridlines
  ax.yaxis.grid(color='gray', linestyle='-', linewidth=0.25)

  # Remove y-axis ticks only (keep labels)
  ax.tick_params(axis='y', which='both', left=False)

  # Remove x-axis ticks only (keep labels)
  ax.tick_params(axis='x', which='both', bottom=False)

  plt.show()

def save_energy_consumption_plot(energy_summary):
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    # Filter out rows labeled 'Total', 'Average', 'Max', or 'Min'
    monthly_data = energy_summary[~energy_summary['supply period'].isin(['Total', 'Average', 'Max', 'Min'])]

    # Convert 'kwh' and 'kw' columns back to numeric since they're currently formatted as strings with commas
    monthly_data['kwh'] = monthly_data['kwh'].str.replace(',', '').astype(float)
    monthly_data['kw'] = monthly_data['kw'].str.replace(',', '').astype(float)

    # Find the highest values for setting axis limits
    max_kwh = monthly_data['kwh'].max()
    max_kw = monthly_data['kw'].max()
    
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Bar plot for 'kwh' with thinner bars
    bar_width = 0.4
    bars = ax1.bar(monthly_data['supply period'], monthly_data['kwh'], color='orange', label='kWh', width=bar_width)
    ax1.set_xlabel('Supply Period (Month)')
    ax1.set_ylabel('kWh', color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    # Set kWh axis limits and ticks
    ax1.set_ylim(0, max_kwh + 10000)
    ax1.set_yticks(np.arange(0, max_kwh + 10000, 10000))

    # Add labels at the center of each bar's height for kWh values
    for bar in bars:
        # Position the label at half the height of each bar
        label_y_position = bar.get_height() / 2
        ax1.text(
        bar.get_x() + bar.get_width() / 2, label_y_position,
        f'{bar.get_height():,.2f}', ha='center', va='center', color='black', fontsize=10
        )

    # Secondary y-axis for 'kw' with line plot and markers
    ax2 = ax1.twinx()
    line, = ax2.plot(monthly_data['supply period'], monthly_data['kw'], color='green', marker='o', label='kW')
    ax2.set_ylabel('kW', color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    # Set kW axis limits and ticks
    ax2.set_ylim(100, max_kw + 100)
    ax2.set_yticks(np.arange(100, max_kw + 100, 100))

    # Add labels to each point for kW values with one decimal place
    for x, y in zip(monthly_data['supply period'], monthly_data['kw']):
        ax2.text(x, y + 10, f'{y:,.2f}', ha='center', va='bottom', color='black', fontsize=10)

    # Configure grid: only horizontal lines, no vertical ones
    plt.grid(axis='y', linestyle='-', linewidth=0.5)  # Retain only horizontal grid lines

    # Remove all the boarders
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(True)
    ax1.spines['bottom'].set_visible(True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(True)
    ax2.spines['bottom'].set_visible(True)

    # Title and layout adjustments
    plt.title('Monthly Energy Consumption (kWh) and Peak Demand (kW)')
    fig.tight_layout()
    plt.show()

    # Save the plot as an image
    #plt.savefig('energy_consumption_plot.png', bbox_inches='tight')
    #plt.close(fig)  # Close the plot to free up memory
    #print(f"Energy consumption plot saved as {output_path}")

def energy_behavior_plot(data):
    """
    Plots the energy behavior (Demand in kW) over the supply period.
    
    Parameters:
        data (pd.DataFrame): DataFrame containing at least 'datetime' and 'kw' columns.
    """
    plt.figure(figsize=(14, 7))
    plt.plot(data['datetime'], data['kw'], linestyle='-', color='orange', label='Demand (kW)')
    
    # Set title based on the actual date range in 'datetime', with start date shifted by one month
    start_date = (data['datetime'].min() + pd.DateOffset(months=1)).strftime('%b-%y')
    end_date = data['datetime'].max().strftime('%b-%y')
    plt.title(f'Energy Behavior Over Supply Period: {start_date} to {end_date}')
    
    plt.xlabel('Date & Time')
    plt.ylabel('Demand (kW)')
    
    # Adjust the x-axis to show Month-Year format (e.g., May-24, Jun-24)
    plt.xticks(
        pd.date_range(start=data['datetime'].min(), end=data['datetime'].max(), freq='MS'),
        labels=pd.date_range(start=data['datetime'].min(), end=data['datetime'].max(), freq='MS').strftime('%b-%y')
    )

    # Configure grid: only horizontal lines, no vertical ones
    plt.grid(axis='y', linestyle='-', linewidth=0.5)  # Retain only horizontal grid lines
    
    # Remove all borders
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(True)
    plt.gca().spines['bottom'].set_visible(True)
    
    # Add legend
    plt.legend()
    
    # Display the plot
    plt.tight_layout()
    plt.show()
