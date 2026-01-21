# Metrics Comparison

| Metric | Before (5-class, original) | After (3-class + balancing + hard rules) |
|---|---:|---:|
| Accuracy | 0.7760 | 0.8760 |
| Weighted F1 | 0.7445 | 0.8563 |
| Weighted Precision | 0.7361 | 0.8428 |
| Weighted Recall | 0.7760 | 0.8760 |

Notes:
- `Before` numbers are from the earlier evaluation on the original dataset (5-class labels).
- `After` numbers are from the retrained model on the balanced 3-class dataset.
- Class 0 (Unsuitable) still has low absolute support; consider increasing `poor` sampling if you want better per-class metrics.
