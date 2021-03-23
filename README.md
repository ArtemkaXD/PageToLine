# PageToLine
 Utility for converting a paged addressing to lane addressing MCU dump according to a given addressing map.
 "map.ini" structure:
 [DEFAULT] -> def_root - last dump path
 [MCUmodel] - addressing map
Addressing map structure:
[OFFSET] - offse of lane addressing dump
[START] - the starting address in the page address dump, which is projected to the beginning of the line dump
[SIZE] - size of projected block
[START] - the starting address in the page address dump, which is projected next
[END] - the ending address in the page address dump, which is projected next
You can use START-SIZE or START-END statements as you want.