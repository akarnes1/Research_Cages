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

Quick Start: Hardware
-----------------------------
This is designed for the custom PCB. If you aren't using that find the signal connections in GPIOClient.

1. Make sure all connections are secure the first time and that your sensor and motors are paired correctly.
2. Make sure the wires have ground on the correct side of the connection.

| Sensor | Motor |
| ------ | ----- |
| ![](https://lh3.googleusercontent.com/CyHQHp_gyRZi1RiNRQOPvoaEqXWMIcf3Y5qkNMpYhTz1t7dunJgunefS9ZR5Sy2crX_G11bjUQ6Arrk06gCkY1zWmBzbOE7IJ0s2aHbWTmacdgypAAnsK8Kjci7nHH-ZOkPgRSvKSi8z2-8cYtwPG6ulzBYLpeh_DJWwDnOC22vdY79U7Cq5xHupjPmoyvCnnPYBsZbqbfbowdQJeDCmttCz8YaJbWKDtifauzrEB_qR3fJiijd6Z_4RiDIxSw_UbEHVxY0_-5mz7fLW9gHm06Y8YCOt4lb1Q6wYcXWVEs1tGpJVTxGLHT0iXS_22MjsnBf-KX6zPteFCUhGqjDTJJd-E0YMcGFRfB6mMwtSo0D9mOXsw8UdKmctV58I0nzafJQQYp0H4ct6B_qN8jOmjAyjwUA_8_senduNV0uF1aYV0ZjwGH6CTHGAhnfUG1cy3qElLGumQCZkA-X_JaOfRG-juQtO5qyz0oqlohmpSr6jKyv5WcyiEWK-upmfDjXgdpkYTCd7dlIaUEsZtyEFaBYxn-RNfcB4sNUgKurzgw_C6v0hGlywqWGmi6Zq8KJrycRL1pPRUACJaolTlT21oF3_VEdgIfzGH8lclmY=w1133-h637-no) | ![](https://lh3.googleusercontent.com/Nzl6fbfCIcb1eJahO3TojPSWh3duDhu6H8w_7QUi00dGhTMj3SdqI-qrGEeQ3NtUckCVcSzu36bNemTdlLX4u4nEg6ec6EqoxvP7bw1fDg8Ye9A6-NeGsMx6j0Ye1SHq0oS5mdj2mJGCMZJff0u0S2M2GP_WdPJS6qE5zhEjRyZte6aSC8278dQX_2JcoHkUi0vX3W6kXpE2hivBUulwdTq5FayGya9zntbLTVjeJ7K_jYWJ_o56WpldJim1SZO4qbKfOkKJEZmPCu3n7i2k2Y2LrjkSLCmTDJihOLR9EZYgXMRBEp1mCasbTm3fkE42h51Wy5Ap2LuGpAfWOzGJbxz6Jy9UMQrmSok075exfxDfBaz9FsaEvZsGqQb1_0Xml3srxDeApHTNyZ44rSXgiOSXaxcTp2Lm8nYyfX4kk6fBNTjBAe4qnHtPRIVeG5ZyW631NFB3uVSm1jcYQ5_GQq_GKKqHIPUoofvkxBPlwCh7zN4b3Ii-Eyyeiu5jihigQSnaDTuXoDbI1ZZGP-l-hXHsxWl7OWnyEv9nmq7a4AXvUSsshaiRvm_wWRXQKsA-TPds7NtTc4y68nTtzerdRuSIvo3sHiF-9DlOxzI=w1133-h637-no)


Quick Start: Software
-----------------------------
Have everything connected to the GPIO Pins outlined in the GPIOClient.
Start running the files in order.

1. Double Click and execute the 1startup.sh
2. Open the file with a 2 in the name and run that from idle
3. Repeat step 2 with file 3
4. Repeat step 2 with file 4

That should open a GUI and you should be good to go from there as long as everything is connected correctly.
