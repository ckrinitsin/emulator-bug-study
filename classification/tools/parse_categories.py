from os import listdir, path

root_directory = "../../results/classifier/"

def parse_iteration(directory):
    dictionary = {}

    for entry in listdir(directory):
        full_path = path.join(directory, entry)
        if path.isdir(full_path):
            dictionary[entry] = len([name for name in listdir(full_path)])

    return dictionary

def output_csv(dictionary, full_path):
    with open(path.join(full_path, 'categories.csv'), "w") as file:
        file.write("category, count\n")
        for key, value in dictionary.items():
            file.write(f"{key}, {value}\n")

def main():
    for entry in listdir(root_directory):
        full_path = path.join(root_directory, entry)
        if path.isdir(full_path):
            dictionary = parse_iteration(full_path)
            output_csv(dictionary, full_path)

if __name__ == "__main__":
    main()
