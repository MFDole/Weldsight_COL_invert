import os

# Specify the input file path
input_file = r'C:\Access_Folder\RainBow.COL'

try:
    # Read the .col file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Extract the color values from each line
    colors = []
    for line in lines:
        # Skip empty lines, lines starting with '#', or lines containing metadata
        if line.strip() == '' or line.startswith('#') or line.startswith('INFO') or line.startswith('BaseColorsTableStored'):
            continue
        
        # Split the line by whitespace and extract the color values
        values = line.split()
        if len(values) == 3:
            r, g, b = map(int, values)
            colors.append((r, g, b))

    # Reverse the order of colors
    reversed_colors = colors[::-1]

    # Create the output folder if it doesn't exist
    output_folder = r'C:\Access_Folder\Output'
    os.makedirs(output_folder, exist_ok=True)

    # Create the output file path
    output_file = os.path.join(output_folder, 'RainBow Inverted.COL')

    # Write the reversed colors to the output file
    with open(output_file, 'w') as file:
        file.write(f"{len(reversed_colors)}\n\n")  # Write the number of colors

        for color in reversed_colors:
            r, g, b = color
            file.write(f"{r} {g} {b}\n")

    print(f"Color palette inverted successfully.")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

except FileNotFoundError:
    print(f"File not found: {input_file}")
    print("Please make sure the file exists in the specified location.")
    print("If the file is located elsewhere, update the 'input_file' variable with the correct path.")

except Exception as e:
    print(f"An error occurred: {str(e)}")