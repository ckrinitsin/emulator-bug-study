## 007

```python
multi_label = True
model = "facebook/bart-large-mnli"
number_bugs = 89
```

Adds the categories *permissions*, *files*, *PID*, *performance* and *debug*. It also applies the category *other* if *semantic* has a score < 0.91 (This was an error, fixed in 009).
