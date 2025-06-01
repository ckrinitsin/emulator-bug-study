from os import path, makedirs

def output(text : str, category : str, labels : list, scores : list, identifier : str):
    file_path = f"output/{category}/{identifier}"
    makedirs(path.dirname(file_path), exist_ok = True)

    with open(file_path, "w") as file:
        for label, score in zip(labels, scores):
            file.write(f"{label}: {score:.3f}\n")

        file.write("\n")
        file.write(text)
