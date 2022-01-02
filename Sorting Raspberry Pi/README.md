# Sorting Raspberry Pi Code
There is only one file in it. You can use it to control 4 servo motors and one electric steering engine. When an object is detected by the active infrared intrusion detector, 4 servo motors and one electric steering engine start to work. When the inductive proximity sensor has no output voltage, the electric steering engine will turn 180 °. 

If you have any questions, feel free to contact me via email address: 12010837@mail.sustech.edu.cn.

# Usage
 Make sure you have install all the required packages, then, type the command "sudo pigpiod" to enable the pigpio, use python 3 to run the python code.

# About GPIO
GPIO pins(BCM mode) are signed in the beginning of the file, you can change the number if you want to, it's going to setup for itself.
