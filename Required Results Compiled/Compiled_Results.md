# Project Phoenix — Compiled Required Results

Source repository: https://github.com/Meet2304/Project-Phoenix
Dataset: Sipakmed (5 classes) · Test set: 405 samples

This document fills the tables requested in *Required Results.docx* using the actual
values recovered from the repository (notebooks, evaluation reports and result CSVs).
Where a requested metric was never computed in the project, that is stated explicitly.

---

## Table 1 — Preprocessing metrics (per technique, per cell category)

Data source: `Image Preprocessing/Comparative Analysis Results/detailed_results.csv`
(per-image results, averaged here by technique × cell category).

**Important:** The project measured **PSNR, SSIM, Edge-Preservation Index (EPI) and
Contrast Enhancement**. **CNR (Contrast-to-Noise Ratio) was never computed** in the
pipeline, so that column cannot be filled from the repo. "Contrast Enhancement" is the
project's contrast metric and is included in its place. Also, the project has no
"Enhanced CLAHE" variant — the available techniques are NLM, PMD, CLAHE and the
combination NLM+CLAHE (`CLAHE_NLM`). Higher PSNR/SSIM = better fidelity/denoising;
higher EPI = better edge preservation; Contrast > 1 = contrast boosted.

| Technique | Cell Category | PSNR (dB) | SSIM | EPI | Contrast Enh. | Denoising | Contrast Enh.? | Edge Pres. |
|-----------|---------------|-----------|------|-----|---------------|-----------|----------------|------------|
| **NLM** | Dyskeratotic | 33.12 | 0.8649 | 0.3786 | 0.9702 | Yes | No | Good |
| NLM | Koilocytotic | 33.25 | 0.8781 | 0.5102 | 0.9636 | Yes | No | Good |
| NLM | Metaplastic | 31.75 | 0.8423 | 0.3937 | 0.9224 | Yes | No | Good |
| NLM | Parabasal | 33.68 | 0.8502 | 0.2229 | 0.9216 | Yes | No | Moderate |
| NLM | Superficial-Intermediate | 34.51 | 0.8813 | 0.3685 | 0.9394 | Yes | No | Good |
| **PMD** | Dyskeratotic | 31.17 | 0.8512 | 0.0795 | 0.9352 | Yes | No | Weak |
| PMD | Koilocytotic | 29.32 | 0.7798 | 0.0519 | 0.8988 | Yes | No | Weak |
| PMD | Metaplastic | 30.39 | 0.8236 | 0.0606 | 0.9027 | Yes | No | Weak |
| PMD | Parabasal | 34.34 | 0.8704 | 0.0274 | 0.9336 | Yes | No | Weak |
| PMD | Superficial-Intermediate | 32.38 | 0.8677 | 0.0644 | 0.9126 | Yes | No | Weak |
| **CLAHE** | Dyskeratotic | 20.55 | 0.8146 | 0.5616 | 1.4422 | No | Yes | Excellent |
| CLAHE | Koilocytotic | 22.77 | 0.8388 | 0.6544 | 1.4133 | No | Yes | Excellent |
| CLAHE | Metaplastic | 21.21 | 0.8037 | 0.5861 | 1.5561 | No | Yes | Excellent |
| CLAHE | Parabasal | 23.85 | 0.8038 | 0.3981 | 1.4544 | No | Yes | Good |
| CLAHE | Superficial-Intermediate | 22.77 | 0.8562 | 0.5608 | 1.5664 | No | Yes | Excellent |
| **NLM+CLAHE** | Dyskeratotic | 20.95 | 0.8603 | 0.6028 | 1.4048 | Yes | Yes | Excellent |
| NLM+CLAHE | Koilocytotic | 23.19 | 0.8757 | 0.6775 | 1.3772 | Yes | Yes | Excellent |
| NLM+CLAHE | Metaplastic | 21.81 | 0.8554 | 0.6503 | 1.4886 | Yes | Yes | Excellent |
| NLM+CLAHE | Parabasal | 24.96 | 0.8619 | 0.5267 | 1.3618 | Yes | Yes | Excellent |
| NLM+CLAHE | Superficial-Intermediate | 23.22 | 0.8925 | 0.5480 | 1.4915 | Yes | Yes | Excellent |

### Technique-level averages (across all 5 categories)
From `summary_results.csv`:

| Technique | SSIM | PSNR (dB) | EPI (Edge Pres.) | Contrast Enh. | Composite Score |
|-----------|------|-----------|------------------|---------------|-----------------|
| NLM+CLAHE (CLAHE→NLM) | 0.8691 | 22.83 | 0.6011 | 1.4248 | 0.7956 |
| NLM only | 0.8634 | 33.26 | 0.3748 | 0.9434 | 0.7786 |
| CLAHE only | 0.8234 | 22.23 | 0.5522 | 1.4865 | 0.7623 |
| PMD only | 0.8385 | 31.52 | 0.0567 | 0.9166 | 0.7175 |

**Chosen pipeline:** NLM + CLAHE (`CLAHE_NLM`) — the top-ranked combination by composite
score, balancing denoising (high SSIM) with strong contrast/edge enhancement. This is the
preprocessing used for the augmented training dataset.

---

## Table 2 — Training/validation accuracy & loss

| Model | Train Accuracy | Train Loss | Validation Accuracy | Validation Loss |
|-------|----------------|------------|---------------------|-----------------|
| **EfficientNetV2-S** | Not recorded* | 0.0067 (final) | 96.23% (final) / 96.56% (best) | Not recorded* |
| **ConvNeXtV2** | Not recorded** | 0.1177 (avg) / 0.0032 (final) | 96.79% (best) | 0.1760 (best) / 0.2149 (test) |

\* EfficientNetV2-S (`Fine Tuning/4_EfficientNetV2-S/sipakmed_efficientnetv2s.ipynb`,
20-epoch run) logged **only training loss and validation accuracy** per epoch. Training
accuracy and validation loss were never computed in that loop. Its held-out **test
accuracy = 96.56%**.

\** ConvNeXtV2 (`Fine Tuning/2_ConvNeXt Transfer Learning/ConvNeXt_Finetuning_v0_1.ipynb`)
was trained with the HuggingFace `Trainer`, which logs training loss + validation
(loss/accuracy/precision/recall/F1) but **not training accuracy**. Final test set:
**accuracy = 96.30%, loss = 0.2149**.

### ConvNeXtV2 per-step training log (5 epochs, 1015 steps)
| Step | Training Loss | Validation Loss | Val Accuracy | Val Precision | Val Recall | Val F1 |
|------|---------------|-----------------|--------------|---------------|------------|--------|
| 200 | 0.1876 | 0.2177 | 0.9259 | 0.9274 | 0.9259 | 0.9244 |
| 400 | 0.0968 | 0.1432 | 0.9654 | 0.9665 | 0.9654 | 0.9656 |
| 600 | 0.0354 | 0.2404 | 0.9531 | 0.9542 | 0.9531 | 0.9527 |
| 800 | 0.0064 | 0.2206 | 0.9531 | 0.9539 | 0.9531 | 0.9523 |
| 1000 | 0.0032 | 0.1760 | 0.9679 | 0.9682 | 0.9679 | 0.9679 |

### EfficientNetV2-S per-epoch log (20-epoch run)
Best validation accuracy 96.56% at epoch 9; final epoch 20 = 96.23% (train loss 0.0067).
Full epoch-by-epoch values are plotted in `EfficientNetV2S_learning_curves.png`.

---

## Table 3 — Precision / Recall / F1 (class-wise)

Data source: `Performance Evaluation/Evaluation Results_v0.1/classification_report.csv`
and `evaluation_summary.txt`.

### ConvNeXtV2 (test set, 405 samples) — AVAILABLE
| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Dyskeratotic | 0.9756 | 0.9756 | 0.9756 | 82 |
| Koilocytotic | 0.9375 | 0.9146 | 0.9259 | 82 |
| Metaplastic | 0.9157 | 0.9500 | 0.9325 | 80 |
| Parabasal | 1.0000 | 1.0000 | 1.0000 | 78 |
| Superficial-Intermediate | 0.9878 | 0.9759 | 0.9818 | 83 |
| **Macro avg** | **0.9633** | **0.9632** | **0.9632** | 405 |
| **Weighted avg** | **0.9632** | **0.9630** | **0.9630** | 405 |

### EfficientNetV2-S — NOT AVAILABLE in the repo
The EfficientNetV2-S notebook computed only overall test accuracy (96.56%). It never ran
`classification_report` / precision / recall / F1, and did not save ground-truth labels,
so **class-wise metrics for EfficientNetV2-S cannot be produced from the repository.**
To fill this row the EfficientNetV2-S model would need to be re-evaluated on the test set.

### Overall model comparison (macro/weighted)
| Model | Precision | Recall | F1-Score | Accuracy |
|-------|-----------|--------|----------|----------|
| EfficientNetV2-S | — (not computed) | — | — | 96.56% (test) |
| ConvNeXtV2 | 0.9632 | 0.9630 | 0.9630 | 96.30% (test) |

Additional ConvNeXtV2 advanced metrics (from `evaluation_summary.txt`):
Balanced Acc 0.9632 · Cohen's Kappa 0.9537 · MCC 0.9538 · ROC-AUC (macro) 0.9958 ·
Avg Specificity 0.9907 · Top-2 Acc 99.01% · Top-3 Acc 99.75%.

---

## Learning curves & confusion matrices (image deliverables)

Generated / located in this folder:

| File | Content |
|------|---------|
| `EfficientNetV2S_learning_curves.png` | EfficientNetV2-S validation accuracy + training loss (generated from the 20-epoch log) |
| `ConvNeXtV2_learning_curves.png` | ConvNeXtV2 validation accuracy + training/validation loss (generated from the step log) |
| `ConvNeXtV2_confusion_matrices.png` | ConvNeXtV2 confusion matrix (raw + normalized) — original from repo |

**Confusion matrix for EfficientNetV2-S is NOT available** (no saved predictions/labels).
**Full train-vs-val accuracy AND loss on the same axes is only fully possible for
ConvNeXtV2**; EfficientNetV2-S lacks train-accuracy and val-loss series.

Original repo evaluation images (ConvNeXtV2) also available in
`Project-Phoenix/Performance Evaluation/Evaluation Results_v0.1/`:
per_class_metrics.png, roc_curves.png, precision_recall_curves.png,
sensitivity_specificity.png, topk_accuracy.png, confidence_distribution.png,
misclassification_patterns.png, overall_metrics.png.

---

## Summary of gaps (what the repo does NOT contain)

1. **CNR** metric — never computed in preprocessing (have PSNR, SSIM, EPI, Contrast).
2. **"Enhanced CLAHE"** technique — does not exist; techniques are NLM, PMD, CLAHE, NLM+CLAHE.
3. **EfficientNetV2-S train accuracy & validation loss** — not logged.
4. **EfficientNetV2-S class-wise precision/recall/F1** — never computed.
5. **EfficientNetV2-S confusion matrix** — predictions/labels not saved.

Everything else requested is present and filled in above.
