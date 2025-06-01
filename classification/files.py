import os

def list_files_recursive(path='.'):
    result = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            result = result + list_files_recursive(full_path)
        else:
            result.append(full_path)
    return result

if __name__ == "__main__":
    directory_path = '../gitlab/issues_text'
    arr = list_files_recursive(directory_path)
    print(arr)
