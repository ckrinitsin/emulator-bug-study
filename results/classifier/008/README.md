## 008

```python
multi_label = True
model = "facebook/bart-large-mnli"
number_bugs = 89
```

Adds the categories *all* and *none*. A bug is *all*, if all categories have a score > 0.9 and *none* if all categories have a score < 0.6.
