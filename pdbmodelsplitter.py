import os
import sys

def extract_models_from_pdb(input_pdb, output_dir):
    """
    Extracts all MODEL sections from a PDB file and saves them to separate files without the MODEL line.

    :param input_pdb: Path to the input PDB file
    :param output_dir: Directory to save the extracted models
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print("Created Output Directory")

    input_file_base = os.path.splitext(os.path.basename(input_pdb))[0]

    with open(input_pdb, 'r') as pdb_file:
        current_model_lines = []
        model_number = None

        for line in pdb_file:

            if line.startswith('MODEL'):
                if current_model_lines and model_number is not None:

                    # Save the previous model
                    output_path = os.path.join(output_dir, f"{input_file_base}_{model_number}.pdb")

                    with open(output_path, 'w') as output_file:
                        output_file.writelines(current_model_lines)

                    current_model_lines = []
                model_number = line.split()[1]  # Extract model number

            elif line.startswith('ENDMDL'):
                if current_model_lines and model_number is not None:
                    # Save the current model
                    output_path = os.path.join(output_dir, f"{input_file_base}_{model_number}.pdb")

                    print("Save MODEL ", model_number)
                    with open(output_path, 'w') as output_file:
                        output_file.writelines(current_model_lines)

                    current_model_lines = []
                    model_number = None

            elif line.startswith('ATOM') or line.startswith('HETATM'):
                current_model_lines.append(line)

        # Handle the last model in case the file doesn't end with ENDMDL
        if current_model_lines and model_number is not None:
            output_path = os.path.join(output_dir, f"{input_file_base}_{model_number}.pdb")

            print("Save MODEL ", model_number)
            with open(output_path, 'w') as output_file:
                output_file.writelines(current_model_lines)

        print("Done")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_pdb_file> <output_directory>")
        sys.exit(1)

    input_pdb_file = sys.argv[1]
    output_directory = sys.argv[2]

    extract_models_from_pdb(input_pdb_file, output_directory)