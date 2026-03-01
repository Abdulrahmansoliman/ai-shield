## Data Bootstrap

Use this for a fast local sanity dataset so the pipeline can run end-to-end.

### 1) Download a small starter set

```bash
python scripts/download_sanity_data.py --real-count 30 --generated-count 30
```

If SSL certificates fail in your environment, retry with:

```bash
python scripts/download_sanity_data.py --real-count 30 --generated-count 30 --insecure
```

This writes files to:
- `data/raw/real/picsum/...`
- `data/raw/generated/tpdne/...`

These are placeholder sources for pipeline smoke tests. They are not your final benchmark sources.

### 2) Prepare metadata and splits

```bash
python scripts/prepare_dataset.py --base-dir data
```

Output files:
- `data/processed/metadata.csv`
- `data/processed/metadata.jsonl`
- `data/processed/splits/train.csv`
- `data/processed/splits/val.csv`
- `data/processed/splits/test.csv`
- `data/processed/splits/unseen_generator.csv`

Use `--unseen-generators "<name>"` only when you have multiple generator families and want to hold one out.

### 3) (Optional) Download from your own URL manifest

Create a CSV like:

```csv
url,label,source,generator,prompt
https://example.com/real_1.jpg,real,coco,,
https://example.com/gen_1.png,generated,diffusiondb,stable-diffusion-v1-5,a sunset city
```

Then run:

```bash
python scripts/download_sanity_data.py --manifest-csv docs/example_manifest.csv --real-count 0 --generated-count 0
```
