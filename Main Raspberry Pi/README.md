# The Main Raspberry Pi Code
The "main" file is in the "python" directory, it uses "IRsensor", "PAJ7620U2", "Serialing", "Ultrasonic", and "VL53L0X" classes for specific functionalities.


The "VL53L0X" module is supported by https://github.com/johnbryanmoore/VL53L0X_rasp_python and https://github.com/cassou/VL53L0X_rasp, Click the URL to find original repositories for this module.

If you have any questions, feel free to contact me via email address: 12012706@mail.sustech.edu.cn.

# Usage
To run the code, download or clone the repository to your raspberry pi, "cd" to the directory, use command "make".

 Make sure you have install all the required packages, then, type the command "sudo pigpiod" to enable the pigpio, use python 3 to run the main python code: "Main"(python folder).

# About Serial Connection
Check out the "Serialling" class in the "python" folder, you need to buy a "USB to TTL" converter so that you could send message to the RoboMaster Board.

# About GPIO
GPIO pins(BCM mode) are signed in the beginning of the "main" folder, you can change the number if you want to, it's going to setup for itself.
