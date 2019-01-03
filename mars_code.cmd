java -jar Mars_modified.jar a db mc CompactDataAtZero dump .text HexText code.txt %1%
java -jar Mars_modified.jar a db mc CompactDataAtZero dump 0x00004180-0x00004ffc HexText code_handler.txt %1%
java -jar Mars_modified.jar a db mc CompactDataAtZero dump .data HexText data.txt %1%