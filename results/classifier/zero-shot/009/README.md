## 009

```python
multi_label = True
model = "facebook/bart-large-mnli"
number_bugs = 89
```

Fixes 007: If *semantic* has a score < 0.91 **and** is the highest category, it is categorized as *other*.
