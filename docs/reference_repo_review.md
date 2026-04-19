# Reference Repo Review

Reference repo inspected:
- Upstream: `https://github.com/desi48danko/deepfake-image-detector`
- Local clone: `c:\Users\20112\OneDrive\Desktop\cp191\external\deepfake-image-detector-reference`

One small repo-quality note:
- The inspected README still tells users to clone `cdenq/deepfake-image-detector`, so `desi48danko/deepfake-image-detector` appears to be a fork or copied version rather than a fully renamed standalone repo.
- Source: [README.md](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/README.md:102)

## What it is

This repo is a TensorFlow + Streamlit deepfake image detector focused on manipulated human images. The README says it trained 11 CNN models on OpenForensics, compared sequential CNNs and EfficientNet variants, and selected `EfficientNet_v2B0` as the best model.

Key evidence:
- README summary: [README.md](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/README.md:78)
- Dataset and model claim: [README.md](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/README.md:80)
- Usage scope note: [README.md](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/README.md:125)

## Repo structure

Main pieces:
- Helper utilities for metrics, plotting, save/load, and dataset helpers: [config.py](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/helper/config.py:64)
- Training notebook: [Full_Training.ipynb](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/main/Training/Full_Training.ipynb)
- Testing / model comparison notebook: [Best_Models_NN.ipynb](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/main/Testing/Best_Models_NN.ipynb)
- Pretrained model zip and Streamlit app: `code/PretrainedModel/`
- Stored model comparison table: [model_eval.csv](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/results/model_eval.csv:1)

## How it works

### Training pipeline

The training notebook uses Keras directory-based datasets and a standard image classification flow:
- Directory loader: [Full_Training.ipynb](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/main/Training/Full_Training.ipynb:144)
- Input rescaling: [Full_Training.ipynb](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/main/Training/Full_Training.ipynb:200)
- EfficientNetV2B0 model section: [Full_Training.ipynb](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/main/Training/Full_Training.ipynb:1561)
- Adam learning rate `1e-5`: [Full_Training.ipynb](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/main/Training/Full_Training.ipynb:1614)
- Training call: [Full_Training.ipynb](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/main/Training/Full_Training.ipynb:1688)

The helper config tracks:
- `BinaryAccuracy`, `AUC`, `Precision`, `Recall`, `TrueNegatives`, `TruePositives`, `FalsePositives`, `FalseNegatives`: [config.py](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/helper/config.py:65)
- JSON + H5 save/load utilities: [config.py](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/helper/config.py:82) and [config.py](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/helper/config.py:135)

### App layer

The Streamlit app is simple and direct:
- Loads a model from JSON + H5: [multipage_app.py](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/PretrainedModel/streamlit_deepfake_detector/multipage_app.py:16)
- Resizes input to `256x256`: [multipage_app.py](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/PretrainedModel/streamlit_deepfake_detector/multipage_app.py:28)
- Uses a fixed `0.5` decision threshold and returns a text confidence string: [multipage_app.py](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/PretrainedModel/streamlit_deepfake_detector/multipage_app.py:36)
- Has two UI modes: upload detector and image guessing game: [multipage_app.py](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/PretrainedModel/streamlit_deepfake_detector/multipage_app.py:58) and [multipage_app.py](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/PretrainedModel/streamlit_deepfake_detector/multipage_app.py:96)

## Reported results

The repo’s evaluation CSV shows four compared entries, with `effnetv2b0` as the strongest validation performer:
- `val_acc = 0.9651`
- `val_precision = 0.9919`
- `val_recall = 0.9498`
- `val_auc = 0.9824`

Source:
- [model_eval.csv](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/results/model_eval.csv:4)

The testing notebook explicitly says the best model is `efficientnetv2-b0_retrain`:
- [Best_Models_NN.ipynb](c:/Users/20112/OneDrive/Desktop/cp191/external/deepfake-image-detector-reference/code/main/Testing/Best_Models_NN.ipynb:258)

## What is useful for AI Shield

Use these ideas:
- Simple baseline framing: one dataset, several CNN baselines, compare metrics, choose a winner.
- Fast deployment path: notebook training -> serialized model -> lightweight Streamlit demo.
- Metrics discipline: track precision, recall, AUC, and confusion counts instead of accuracy alone.
- Demo design: user upload flow plus example-image mode is a good presentation pattern.

## Gaps relative to AI Shield

This is the important part for your presentation. The reference repo is similar, but your project is stronger because it is designed around robustness and generalization, not only clean-set classification.

Main gaps:
- Single core dataset: it relies on OpenForensics rather than a broader real-vs-generated benchmark mix.
- Narrow domain: the README says it works best on photorealistic human imagery and struggles on cartoons or drawings.
- Limited split rigor: the README says not much cleaning was needed besides `train_test_split`, which is weaker than your dedupe + leakage prevention + unseen-generator design.
- No explicit robustness suite: no JPEG, resize, crop, blur, or mild-edit stress testing is described as a formal benchmark.
- No unseen-generator evaluation: that is central to your proposal and not a visible first-class part of this repo.
- No calibrated uncertainty: the app gives `Real` or `Fake` with a fixed threshold and no `uncertain` output.
- No honest failure policy: the output is binary rather than risk-aware.
- No video path: your proposal has video as a reach goal.

## Recommended positioning

For tomorrow, present this repo as:
- A strong proof that the basic problem is implementable.
- A good reference for baseline model selection and demo packaging.
- Not the same as AI Shield, because AI Shield adds dataset rigor, stress testing, unseen-generator evaluation, and uncertainty-aware output.

## What we should reuse

Short term:
- Baseline model family idea: start with EfficientNet or another strong pretrained backbone.
- Deployment pattern: CLI first, then a lightweight app.
- Metric tracking table and evaluation summaries.

Do not copy directly:
- The fixed `0.5` threshold.
- Single-dataset framing.
- Binary output without uncertainty handling.
- Weak data split assumptions.
