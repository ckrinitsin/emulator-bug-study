## 005

```python
multi_label = True
model = "facebook/bart-large-mnli"
number_bugs = 89
```

If a category, which suggests a bug we want to discard, has a score over *0.92*, it gets applied, even if it is not the highest score.
