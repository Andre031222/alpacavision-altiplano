"""Generate fig8 (YOLOv11n detections: ground truth vs predictions) for the paper.
Self-contained: reads the val_batch images produced by the leakage-free detector
evaluation (outputs/figures/stage1_test_eval/) and annotates with the honest metrics.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "outputs" / "figures" / "stage1_test_eval"
OUT = ROOT / "paper" / "figures"
DPI = 300
DARK = "#2C3E50"

pred = sorted(SRC.glob("val_batch*_pred.jpg"))
lbl = sorted(SRC.glob("val_batch*_labels.jpg"))
pairs = list(zip(lbl, pred))[:3]
n = len(pairs)
if n == 0:
    raise SystemExit("No val_batch images in %s (run scripts/eval_detector.py first)" % SRC)

fig, axes = plt.subplots(2, n, figsize=(5 * n, 5.5),
                         gridspec_kw={"hspace": 0.05, "wspace": 0.03})
axes = np.atleast_2d(axes)
rows = ["Ground Truth", "YOLOv11n Predictions"]
for col, (lp, pp) in enumerate(pairs):
    for row, img in enumerate([lp, pp]):
        axes[row, col].imshow(np.array(Image.open(img)))
        axes[row, col].axis("off")
        if col == 0:
            axes[row, col].set_ylabel(rows[row], fontsize=9, fontweight="bold", labelpad=6)
    axes[0, col].set_title(f"Batch {col + 1}", fontsize=9)

fig.suptitle("YOLOv11n Body Detection -- Ground Truth vs. Predictions (test set)",
             fontsize=11, fontweight="bold", y=1.01)
fig.text(0.5, -0.02,
         "mAP@0.5 = 0.860 | Precision = 0.913 | Recall = 0.731  "
         "(leakage-free test set, n = 308 images)",
         ha="center", fontsize=8.5, color=DARK)
plt.tight_layout(pad=0.5)
for ext in ("png", "pdf"):
    fig.savefig(OUT / f"fig8_yolo_detections.{ext}", dpi=DPI, bbox_inches="tight")
plt.close(fig)
print("fig8_yolo_detections regenerated.")
