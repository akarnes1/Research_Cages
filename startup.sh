cd
cd Desktop/cages
cd mjpg-streamer
sleep 5
./mjpg_streamer -i "./input_uvc.so -n -y -f 15 -r 640x480" -o "./output_http.so -n -c cages:research -w ./www"&
cd 
cd Desktop/cages
sleep 5
python cagesServer.py&
sleep 5
python cagesGPIOClient.py&
sleep 5
python cagesGUIClient.py&
sleep 5