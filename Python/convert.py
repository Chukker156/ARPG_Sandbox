import argparse
import csv
import re

def convert_to_csv(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()[1:-1]  # Skip first and last lines

    data = []
    current_object = {}
    uid_counter = 1  # Unique identifier counter

    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespaces
        if line.startswith('*BEGIN_OBJECT'):
            if current_object:  # If there's existing data in current_object, append it to data
                current_object['UID'] = f'{uid_counter:04d}'  # Add unique identifier
                data.append(current_object)
                uid_counter += 1  # Increment unique identifier counter
            current_object = {}  # Reset current_object for the new block
        elif line.startswith('*END_OBJECT'):
            if current_object:  # Append the current_object to data if it's not empty
                current_object['UID'] = f'{uid_counter:04d}'  # Add unique identifier
                data.append(current_object)
                uid_counter += 1  # Increment unique identifier counter
                current_object = {}  # Reset current_object after appending
        else:
            parts = line.split()
            if len(parts) > 1:
                key, *values = parts
                if key == '*NAME':
                    current_object[key[1:]] = values[0].strip("['']")
                else:
                    current_object[key[1:]] = values

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['UID', 'NAME', 'POSITION1', 'POSITION2', 'POSITION3', 'ROTATION1', 'ROTATION2', 'ROTATION3', 'SCALE']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for obj in data:
            writer.writerow({
                'UID': obj.get('UID', ''),
                'NAME': obj.get('NAME', ''),
                'POSITION1': obj.get('POSITION', [''])[0],
                'POSITION2': obj.get('POSITION', [''])[1],
                'POSITION3': obj.get('POSITION', [''])[2],
                'ROTATION1': obj.get('ROTATION', [''])[0],
                'ROTATION2': obj.get('ROTATION', [''])[1],
                'ROTATION3': obj.get('ROTATION', [''])[2],
                'SCALE': obj.get('SCALE', [''])[0]
            })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert .tog file to .csv file')
    parser.add_argument('input_file', help='Input .tog file')
    parser.add_argument('output_file', help='Output .csv file')
    args = parser.parse_args()

    input_file = args.input_file + '.tog'
    output_file = args.output_file + '.csv'

    convert_to_csv(input_file, output_file)
