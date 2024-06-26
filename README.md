# Squat-O-Meter

Squat-O-Meter is a Python GUI application that counts the number of squats performed by the user using accelerometer data from the [Phyphox](https://phyphox.org/) smartphone app. It provides real-time feedback and voice notifications to the user.

![Squat-O-Meter Screenshot](screenshot.png)

## Features

- Counts the number of squats performed by the user.
- Provides voice feedback to the user.
- Allows the user to set a target number of squats.
- Adjustable parameters for squat detection:
  - **Moving window size**: The number of samples considered in the moving window for analyzing accelerometer data. Higher values may improve accuracy but increase processing time. A Higher value may affect real-time performance if your pc is slow.
  - **Minimum time between squats**: The minimum time interval (in seconds) allowed between two consecutive squat detections. This helps prevent rapid, false detections.
  - **Change between absolute and acceleration in the z-direction**: Allows the user to choose between using absolute acceleration or acceleration in the z-direction for squat detection. While using absolute acceleration the phone can be held in any orientation. It uses acceleration in z-direction by default, and phone should be held parallel to the ground plane (if used in default mode).
  - **Acceleration threshold**: The minimum value of acceleration required to detect a squat. Squat detection occurs when the acceleration surpasses this threshold.
- **Analyze data tab**: View squat progress over the month.

![Analyze Data tab Screenshot](Progress_Report.png)

## Prerequisites

- Python 3.x
- Required Python packages (install using pip):
  - tkinter
  - PIL
  - ttkbootstrap
  - requests
  - scipy
  - numpy
  - pyttsx3
  - pandas
  - matplotlib

## Installation (Note: Currently it is only supported in Windows)

1. Clone the repository:

```
git clone https://github.com/manavthakkar/squat-o-meter
```

2. Navigate to the project directory:

```
cd squat-o-meter
```
3. Create a virtual python environment:
```
python -m venv myenv
```
4. Activate the created virtual environment:
```
.\myenv\Scripts\activate
```

5. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

It uses the Phyphox app for receiving the accelerometer sensor data from the phone. The app can be installed from the [Google Play (Android)](https://play.google.com/store/apps/details?id=de.rwth_aachen.phyphox&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1) or the [App Store (iOS)](https://itunes.apple.com/us/app/phyphox/id1127319693?l=de&ls=1&mt=8). Start the app and select `Acceleration with g` and then click on `Allow remote access`. You'll see an IP address displayed on the bottom of the screen.

**Note:** Your phone and PC should be on the same network. For best performance and to avoid any latency, use personal mobile hotspot from the phone.

1. Run the `main.py` file:

```
python main.py
```

2. Enter the IP address from the smartphone app when prompted (without the port number 8080).

3. Set the target number of squats and adjust other parameters as needed.

4. Start performing squats, and the application will count them in real-time.

5. Save your progress after each set by clicking on the `Save to Database` button. In case of fake detections, the count can be updated by clicking and dragging on the meter.

6. View squat progress over months in the "Analyze Data" tab.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests to suggest improvements or fix any bugs.

## License

This project is licensed under the [MIT License](LICENSE).
