## Dataset Plan

1. **Real Images**  
   - Sample from MS COCO and Open Images (real-world photos).
   - Deduplicate and document each sample with its source and any preprocessing.

2. **Generated Images**  
   - Use the **GenImage** dataset for a range of generator models.
   - Sample from **DiffusionDB** (Stable Diffusion) and **Synthbuster** (diffusion detection benchmark).
   - Record the generator model, prompt (if available), and any post-processing.

3. **Video (Reach Goal)**  
   - Consider frame sampling from DFDC, FaceForensics++, Celeb-DF, or DeeperForensics only if time allows.
   - Each video sample would be stored as a set of frames with metadata.

Create a small "sanity subset" (5k-10k samples) to iterate quickly before scaling up.
