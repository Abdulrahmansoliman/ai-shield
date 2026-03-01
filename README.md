# AI Shield

This repository is the starting point for my CP192 capstone project. It contains:

- A draft plan for curating real and AI-generated image datasets.
- A draft metadata schema describing each sample (source, generator, compression, transformations).
- A draft strategy for splitting data into training, validation, test and unseen-generator sets.
- A skeleton for the data pipeline, model training, evaluation harness, and packaging a final detection tool (AI Shield).

The goal of this project is to build a robust detector for AI-generated media (images, and optionally video) that remains reliable under compression, resizing, cropping and minor edits, and can generalize to new generator models.

See the `docs` and `scripts` directories for more detail.
