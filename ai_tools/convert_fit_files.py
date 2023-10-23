#%%
import fitparse
import csv
import os

def convert_fit_to_csv(fit_filepath, csv_filepath):
    # Create a FIT File object
    fitfile = fitparse.FitFile(fit_filepath)

    # Open the CSV file for writing
    with open(csv_filepath, mode='w', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Initialize a flag to indicate whether headers have been written
        headers_written = False

        # Loop through all the messages in the FIT file
        for record in fitfile.get_messages('record'):
            # If headers haven't been written, write them
            if not headers_written:
                field_names = [field.name for field in record]
                csv_writer.writerow(field_names)
                headers_written = True

            # Get the values of all the fields in the record
            field_values = [field.value for field in record]

            # Write the values to the CSV file
            csv_writer.writerow(field_values)

    print(f"FIT file '{fit_filepath}' successfully converted to CSV file '{csv_filepath}'")

def convert_all_fit_files_in_directory(directory_path, output_directory):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file is a FIT file
        if filename.endswith('.fit'):
            # Construct the full file path
            fit_filepath = os.path.join(directory_path, filename)
            # Construct the output CSV file path
            csv_filename = os.path.splitext(filename)[0] + '.csv'
            csv_filepath = os.path.join(output_directory, csv_filename)
            # Convert the FIT file to CSV
            convert_fit_to_csv(fit_filepath, csv_filepath)

#%%
convert_all_fit_files_in_directory('/Users/pinheirochagas/Downloads/strava_export/activities', '/Users/pinheirochagas/Downloads/strava_export/activities_csv')


# %%
import csv
import os
import numpy as np

# Constants
ROLLING_AVERAGE_SECONDS_DEFAULT = 30
FTP = 250  # Functional Threshold Power of the athlete (in Watts)
POWER_COLUMN_INDEX = 0  # Column index of power data in the CSV file

def calculate_training_peaks_metrics(power_data):
    if not power_data:
        return None, None, None

    # Convert power data to a NumPy array
    power_data = np.array(power_data)

    # Determine the rolling average interval (in seconds)
    rolling_avg_seconds = min(ROLLING_AVERAGE_SECONDS_DEFAULT, len(power_data))

    # Calculate rolling average power (4th power) over the specified interval
    rolling_avg_power_4th = np.convolve(power_data**4, np.ones(rolling_avg_seconds)/rolling_avg_seconds, mode='valid')

    # Calculate Normalized Power (NP)
    np_power = np.cbrt(np.mean(rolling_avg_power_4th))

    # Calculate Intensity Factor (IF)
    intensity_factor = np_power / FTP

    # Calculate Training Stress Score (TSS)
    duration_hours = len(power_data) / 3600
    tss = (duration_hours * np_power * intensity_factor) / (FTP * 0.5) * 100

    return np_power, intensity_factor, tss

def calculate_metrics_for_all_activities(input_directory, output_csv_filepath):
    with open(output_csv_filepath, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Activity', 'Normalized Power (NP)', 'Intensity Factor (IF)', 'Training Stress Score (TSS)'])

        for filename in os.listdir(input_directory):
            if filename.endswith('.csv'):
                csv_filepath = os.path.join(input_directory, filename)

                # Extract power data from the CSV file
                power_data = []
                with open(csv_filepath, 'r') as activity_csv:
                    csv_reader = csv.reader(activity_csv)
                    for row in csv_reader:
                        try:
                            power = float(row[POWER_COLUMN_INDEX])
                            power_data.append(power)
                        except (ValueError, IndexError):
                            continue

                # Calculate TrainingPeaks metrics
                np_power, intensity_factor, tss = calculate_training_peaks_metrics(power_data)

                # Skip writing to CSV if metrics are not calculated
                if np_power is None:
                    continue

                # Write metrics to CSV
                csv_writer.writerow([filename, np_power, intensity_factor, tss])

    print(f"TrainingPeaks metrics have been calculated and saved to '{output_csv_filepath}'")

#%%
# Example usage: Calculate metrics for all activities in 'input_directory' and save to 'metrics.csv'
calculate_metrics_for_all_activities('/Users/pinheirochagas/Downloads/strava_export/activities_csv', '/Users/pinheirochagas/Downloads/strava_export/activities_csv/metrics.csv')

# %%
