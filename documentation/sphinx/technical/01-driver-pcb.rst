Driver PCB
----------

The Micro Dot pHAT PCB includes three IS31FL3730 driver chips, each 
able to drive two matrix displays wired in opposing polarities.

The chips are given sequential i2c addresses: 0x61, 0x62 and 0x63.

Each chip is configured to 8x8, bi-directional matrix mode and the matrix
pairs are wired such that the rows of one are connected to the colums of 
the second.

