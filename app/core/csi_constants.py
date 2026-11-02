"""CSI 前後端共用常數（與 footprint-csi/csi_row_width.py、webui-lab 一致）。"""

FLAT_THRESHOLD = 62.7
FOREFOOT_BAND = (0.15, 0.40)
ARCH_BAND = (0.40, 0.70)
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1440
LETTERBOX_FILL = "white"
# 使用者移動小於這個像素距離視為未校正（相對標記圖尺寸）
CORRECTION_PIXEL_EPS = 2.0
# 目錄「掃描」的 class.cid
SCAN_CLASS_CID = 2
