## create_csv.py

This script creates a csv for every iteration of the classifier (inside *results/classifier*). It represents the quantity of bugs in a category.

Execute:
```
python create_csv.py
```

## create_diff.py

This script creates a diff file, which represents the changes between to iterations.

Execute:
```
python create_diff.py <id_old> <id_new>
```
The *id* is a directory name in *results/classifier*.
