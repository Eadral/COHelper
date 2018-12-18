set input1=%1%
set input2=%2%
rm mars_output.txt
java -jar Mars_modified.jar db mc CompactDataAtZero %input1% %input2% >> mars_output.txt