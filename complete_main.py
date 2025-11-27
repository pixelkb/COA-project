import serial
import time
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

# ------------------------------------------------------------
# 1. SETUP SERIAL + CAMERA
# ------------------------------------------------------------

ser = serial.Serial("COM5", 115200)  # change COM port if needed
cam = cv2.VideoCapture(0)

colors = ["RED", "YELLOW", "GREEN"]

# Create required directories
os.makedirs("results/saved_imgs", exist_ok=True)
os.makedirs("results/metrics/plots", exist_ok=True)

# ------------------------------------------------------------
# 2. METRIC FUNCTIONS
# ------------------------------------------------------------

def compute_metrics(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    metrics = {}
    metrics["sharpness"] = cv2.Laplacian(gray, cv2.CV_64F).var()
    metrics["contrast"] = np.std(gray)
    metrics["brightness"] = np.mean(gray)

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
    hist /= hist.sum()
    metrics["entropy"] = -np.sum(hist * np.log2(hist + 1e-10))

    return metrics


# ------------------------------------------------------------
# 3. CAPTURE IMAGES USING HANDSHAKE WITH NODEMCU
# ------------------------------------------------------------

def capture_images():
    for color in colors:

        # Send handshake: request next LED
        ser.write(b"NEXT\n")
        print("Sent: NEXT")

        # Wait for NodeMCU to confirm LED is ON
        while True:
            line = ser.readline().decode().strip()
            print("Received:", line)

            if line == f"READY {color}":
                print(f">>> {color} LED active. Capturing image…")
                break

        # Capture image
        ret, frame = cam.read()
        filename = f"results/saved_imgs/{color}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")

        time.sleep(0.5)  # small buffer

# ------------------------------------------------------------
# 4. COMPUTE METRICS FOR EACH IMAGE
# ------------------------------------------------------------

def analyze_metrics():
    metrics_list = []

    for color in colors:
        img_path = f"results/saved_imgs/{color}.jpg"
        img = cv2.imread(img_path)

        if img is None:
            print(f"Error: Could not load {img_path}")
            continue

        m = compute_metrics(img)
        m["color"] = color
        metrics_list.append(m)

    df = pd.DataFrame(metrics_list)
    df.to_csv("results/metrics/metrics.csv", index=False)

    print("\nMetrics saved to results/metrics/metrics.csv\n")
    return df


# ------------------------------------------------------------
# 5. DETERMINE BEST LIGHTING SHADE
# ------------------------------------------------------------

def find_best(df):
    best_row = df.loc[df["sharpness"].idxmax()]
    best_color = best_row["color"]

    with open("results/metrics/best_color.txt", "w") as f:
        f.write(f"Best lighting condition: {best_color}\n")
        f.write(best_row.to_string())

    print(f"\n>>> BEST LIGHTING: {best_color}\n")
    return best_color


# ------------------------------------------------------------
# 6. PLOT COMPARISON GRAPHS
# ------------------------------------------------------------

def plot_graphs(df):

    # SHARPNESS
    plt.figure(figsize=(6,4))
    plt.bar(df["color"], df["sharpness"])
    plt.title("Sharpness Comparison")
    plt.xlabel("Color")
    plt.ylabel("Sharpness")
    plt.savefig("results/metrics/plots/sharpness_plot.png")
    plt.close()

    # CONTRAST
    plt.figure(figsize=(6,4))
    plt.bar(df["color"], df["contrast"])
    plt.title("Contrast Comparison")
    plt.xlabel("Color")
    plt.ylabel("Contrast")
    plt.savefig("results/metrics/plots/contrast_plot.png")
    plt.close()

    # BRIGHTNESS
    plt.figure(figsize=(6,4))
    plt.bar(df["color"], df["brightness"])
    plt.title("Brightness Comparison")
    plt.xlabel("Color")
    plt.ylabel("Brightness")
    plt.savefig("results/metrics/plots/brightness_plot.png")
    plt.close()

    print("Plots saved in results/metrics/plots/")


# ------------------------------------------------------------
# 7. MAIN PIPELINE
# ------------------------------------------------------------

print("Starting capture process...\n")
capture_images()

print("\nComputing metrics...\n")
df = analyze_metrics()

print("\nDetermining best color...\n")
best = find_best(df)

print("\nGenerating comparison graphs...\n")
plot_graphs(df)

print("\n\n>>> PROCESS COMPLETE! <<<\n")

cam.release()
