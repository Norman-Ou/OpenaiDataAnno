import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 读取图像（以灰度或 RGB 形式）
image = cv2.imread("data/CrowdAI/val/images/000000020289.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 提供的 annotation 示例
annotation = {
    "bbox": [14, 14, 189, 16],
    "segmentation": [
        [30, 190, 23, 203, 14, 200, 20, 187, 30, 190]
    ]
}

# 创建画布
fig, ax = plt.subplots(figsize=(3, 3))
ax.imshow(image)

# === 可视化 bbox ===
x, y, w, h = annotation["bbox"]
rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='red', facecolor='none')
ax.add_patch(rect)

# === 可视化 segmentation ===
for seg in annotation["segmentation"]:
    # 转成 Nx2 的 numpy 数组
    poly = np.array(seg).reshape((-1, 2))
    polygon = patches.Polygon(poly, linewidth=2, edgecolor='blue', facecolor='none')
    ax.add_patch(polygon)

plt.title("BBox + Segmentation")
plt.axis('off')
plt.savefig("test.png")