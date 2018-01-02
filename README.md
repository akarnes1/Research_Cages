Automated Food Delivery Cages for rats
=============================
This project was to outfit a rat cage with a system that record the revolutions of an excersize wheel and dispense food automatically.

To start the code was written on a Raspberry Pi so it is recommended to implement this there.

Required components
-----------------------------
| Software | Hardware | Optional |
| -------- | -------- | -------- |
| Python 2.7.9 | Servos and the mounting hardware | Custom PCB (Breakout board for servo powering and sensor connecting) |
| Bash | IR Sensors |     | 
| Local version of this repository | Layfeyette Instruments Rat Cage with excersize wheel |    |

Quick Start
-----------------------------
Have everything connected to the GPIO Pins outlined in the GPIOClient.
Start running the files in order.

1. Double Click and execute the 1startup.sh
2. Open the file with a 2 in the name and run that from idle
3. Repeat step 2 with file 3
4. Repeat step 2 with file 4

That should open a GUI and you should be good to go from there as long as everything is connected correctly.
