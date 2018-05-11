cd mjpg-streamer
sleep 5
./mjpg_streamer -i "./input_uvc.so -n -y -f 15 -r 640x480" -o "./output_http.so -n -c cages:research -w ./www"&

cd ..
python3 cageCommandLine.py