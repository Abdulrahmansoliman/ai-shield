## Splitting Strategy

1. **Training/Validation/Test (80/10/10)**  
   - Ensure no near-duplicates appear across splits by hashing filenames/content.
   - Reserve entire generator families for the unseen-generator test set.

2. **Unseen Generator Set**  
   - Select at least one generator family that never appears in training.
   - Evaluate generalization on this unseen set.

3. **Stress-Test Suites**  
   - For each split, derive versions of samples with different JPEG qualities (100 -> 50 -> 10), different crops, blurs, and color adjustments.
   - Report performance across these transformations rather than a single accuracy number.
