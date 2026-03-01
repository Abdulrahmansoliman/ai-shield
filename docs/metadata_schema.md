## Metadata Schema

A JSON-like schema for each media sample:

```json
{
  "id": "<unique id>",
  "type": "image",
  "source": "coco",            // e.g. coco, open_images, genimage, diffusiondb, synthbuster
  "generator": "StableDiffusion-v1.5", // if generated; null for real
  "prompt": "<text prompt>",            // if available
  "compression": 90,                    // JPEG quality level
  "transforms": ["crop", "blur"],       // list of post-processing steps
  "split": "train"                      // train, val, test, or unseen_generator
}
```

This metadata allows robust filtering and helps prevent data leakage across splits.
