# AI Shield Presentation

## Goal

This outline is built for a short capstone presentation. It uses the inspected reference repo as related work, but keeps the emphasis on why `AI Shield` is a stronger and more research-grounded project.

## Slide 1: Title

Title:
- `AI Shield: Robust Detection of AI-Generated Images Under Real-World Conditions`

Say:
- My capstone project is about detecting AI-generated images, and eventually short videos, in conditions closer to the real internet.
- The core problem is not just detecting clean generated images.
- The harder and more important problem is detecting them after compression, resizing, cropping, reposting, and mild edits.

## Slide 2: Why this matters

Title:
- `Why This Problem Matters`

Bullets:
- AI-generated media is getting harder to distinguish from real media.
- Misuse includes deception, misinformation, impersonation, and non-consensual content.
- Many detectors look good on benchmark datasets but degrade in real-world use.

Say:
- A detector that only works on ideal images is not enough.
- Real media moves through platforms and gets transformed.
- So robustness is part of the problem, not an optional extra.

## Slide 3: Related work / reference repo

Title:
- `Reference Implementation I Studied`

Bullets:
- GitHub repo: `desi48danko/deepfake-image-detector`
- Uses TensorFlow + Streamlit.
- Trains multiple CNNs on OpenForensics.
- Chooses EfficientNetV2B0 as the best model.
- Deploys a simple upload-based detector and a game mode.

Say:
- I cloned and inspected this repo because it is close to the kind of system I want to build.
- It proves the baseline idea is very feasible: dataset, trained model, and working app.
- It also shows exactly where my project needs to go further.

Evidence:
- Summary and model choice: [reference_repo_review.md](c:/Users/20112/OneDrive/Desktop/cp191/ai-shield/docs/reference_repo_review.md)

## Slide 4: What the reference repo does well

Title:
- `What It Does Well`

Bullets:
- Clear baseline detector pipeline.
- Multiple models compared rather than one arbitrary choice.
- Precision, recall, AUC, and confusion counts are tracked.
- A simple app makes the work demoable.

Say:
- This is useful because it gives me a realistic baseline.
- It also shows that a capstone can connect experiments to a usable interface.

## Slide 5: Limits of the reference repo

Title:
- `Why AI Shield Needs More`

Bullets:
- It is centered on a narrower dataset and domain.
- The README only describes light cleaning plus `train_test_split`.
- The deployed app uses a fixed threshold and always returns `Real` or `Fake`.
- It does not center unseen-generator testing or stress-test robustness.

Say:
- This is the key difference.
- My capstone is not just “build a detector.”
- It is “build and evaluate a detector honestly under realistic distribution shift.”

## Slide 6: My project design

Title:
- `AI Shield Design`

Bullets:
- Real image sources: MS COCO, Open Images.
- Generated image sources: GenImage, DiffusionDB, Synthbuster.
- Careful metadata, deduplication, and leakage-aware splits.
- Evaluation under JPEG compression, resizing, cropping, blur/noise, and mild edits.
- Unseen-generator evaluation.
- Final tool outputs score, confidence, and possibly `uncertain`.

Say:
- The proposal is image-first so the project stays feasible.
- Video is a reach goal after the image pipeline is solid.
- The tool should follow the evidence from the experiments, not hide the failures.

## Slide 7: What I have already built

Title:
- `Current Progress`

Bullets:
- Repo scaffolded for docs, scripts, and data.
- Dataset prep pipeline implemented.
- Starter downloader implemented for sanity testing.
- Metadata and split generation already working.
- Reference repo reviewed for baseline ideas.

Say:
- I already have the project skeleton in place.
- I also implemented a first-pass data bootstrap pipeline so I can move from proposal to experimentation quickly.

Code refs:
- [prepare_dataset.py](c:/Users/20112/OneDrive/Desktop/cp191/ai-shield/scripts/prepare_dataset.py)
- [download_sanity_data.py](c:/Users/20112/OneDrive/Desktop/cp191/ai-shield/scripts/download_sanity_data.py)
- [data_bootstrap.md](c:/Users/20112/OneDrive/Desktop/cp191/ai-shield/docs/data_bootstrap.md)

## Slide 8: Deliverables

Title:
- `Planned Deliverables`

Bullets:
- A curated and documented dataset pipeline.
- Baseline and improved detection models.
- Robustness curves, not just one accuracy number.
- Unseen-generator evaluation.
- A final `AI Shield` tool for image upload or batch scanning.

Say:
- The final deliverable is both research and tooling.
- The written report decides which model to trust, where it breaks, and when the system should say `uncertain`.

## Slide 9: Why this is a good capstone

Title:
- `Why This Is a Strong Capstone`

Bullets:
- Technically feasible with an image-first scope.
- Substantial engineering: data, training, evaluation, and tool deployment.
- Stronger than a basic classifier because it studies generalization and robustness.
- Socially relevant and timely.

Say:
- The value is not only that the model can classify images.
- The value is that the evaluation design is realistic enough to support a trustworthy tool.

## Slide 10: Immediate next steps

Title:
- `Next Steps After This Presentation`

Bullets:
- Pull actual benchmark datasets instead of placeholder sanity data.
- Build the first real baseline model.
- Lock the metadata schema and split rules.
- Add perturbation generators for JPEG, resize, crop, blur, and noise.

Say:
- After this presentation, the work becomes very concrete.
- The first milestone is a baseline model plus a reproducible evaluation harness.

## Short closing

Use this if they ask for a one-sentence summary:

`AI Shield is a deepfake detection capstone that focuses on the harder and more realistic question: can a detector still work after the image has been through the internet, and can it admit uncertainty when it should not guess?`

## Likely questions and short answers

### Why not just use an existing detector?

Because most existing demos optimize for clean classification, while my capstone is explicitly about robustness, generalization, and honest uncertainty.

### Why start with images and not video?

Because image-first is the right scope for compute, storage, and reproducibility. Video remains a reach goal once the image pipeline is solid.

### What makes this different from the reference repo?

The reference repo is a useful baseline. AI Shield extends the idea with multi-source datasets, leakage-aware splits, stress tests, unseen-generator evaluation, and uncertainty-aware outputs.

### What have you implemented already?

The repo, dataset bootstrap scripts, and split-generation pipeline are already in place. The next step is plugging in real benchmark datasets and training the first baseline.

## If you only have 3 minutes

Use Slides 1, 2, 3, 5, 6, and 10.
