# COA-project
ClearLens: Chromatic Influence on Image Clarity
Overview:
ClearLens is a low-cost imaging setup that studies how different LED light colors (Red, Yellow, Green)
affect the clarity of webcam-captured images. The system uses NodeMCU (ESP8266) for LED control
and Python + OpenCV for automated image capture and clarity analysis.
Features:
- Automated LED switching (Red → Yellow → Green)
- Webcam image capture
- Image clarity analysis (Sharpness, Contrast, Brightness, Entropy)
- Auto-generated plots & best-color detection

Hardware:
- NodeMCU ESP8266
- Laptop webcam
- Red, Yellow, Green LEDs
- 220Ω resistors, jumper wires, breadboard
  
Software:
- Arduino IDE
- Python 3 (OpenCV, NumPy, Matplotlib, Pandas, PySerial)
  
Workflow:
1. Python sends NEXT → NodeMCU switches LED.
2. Webcam captures image under each color.
3. OpenCV computes clarity metrics.
4. Results saved as CSV + plots.
5. Best illumination color identified
6.  Results Summary:
Green light performed best overall.
Color | Sharpness | Brightness
Red | Low | Low
Yellow| Medium | Medium
Green | Highest | Highest

Conclusion:
Green illumination provides the clearest images due to higher sharpness and brightness. The project
shows how simple IoT hardware + image processing can optimize imaging conditions.<img width="1600" height="1080" alt="ClearLens" src="https://github.com/user-attachments/assets/32a8fdf4-ef28-4651-9323-f72c5d1a2ddf" />


