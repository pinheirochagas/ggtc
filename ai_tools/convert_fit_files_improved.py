
import fitparse
import csv
import os

def convert_fit_to_csv(fit_files_directory, output_csv_directory):
    # Check if output directory exists, if not, create it
    if not os.path.exists(output_csv_directory):
        os.mkdir(output_csv_directory)

    for file in os.listdir(fit_files_directory):
        if file.endswith(".fit"):
            # Create a FitFile object
            fitfile = fitparse.FitFile(os.path.join(fit_files_directory, file))

            # Placeholder for activity type
            activity_type = None

            # Find the activity type from the session message
            for session in fitfile.get_messages('session'):
                activity_type = session.get_value('sport')
                break

            # Placeholder for field names (dynamically determined)
            field_names = set()

            # Add 'activity_type' to the field names
            field_names.add('activity_type')

            # Determine all field names from the records
            for record in fitfile.get_messages('record'):
                field_names.update(record.get_values().keys())

            # Convert field names to a list
            field_names = list(field_names)

            # Prepare CSV file for writing
            with open(os.path.join(output_csv_directory, file.replace(".fit", ".csv")), 'w', newline='') as csvfile:
                # Initialize CSV writer
                writer = csv.DictWriter(csvfile, fieldnames=field_names)

                # Write header to CSV file
                writer.writeheader()

                # Iterate through all records in FIT file
                for record in fitfile.get_messages('record'):
                    # Get all data of the record as a dictionary
                    record_data = record.get_values()

                    # Include activity type to the record data
                    record_data['activity_type'] = activity_type

                    # Write row to CSV file
                    writer.writerow(record_data)

            print(file + " has been converted to CSV.")

# Usage
fit_files_directory = 'path/to/fit/files'  # Update with the path to your FIT files directory
output_csv_directory = 'path/to/output/csv'  # Update with the path to your output CSV directory
convert_fit_to_csv(fit_files_directory, output_csv_directory)
