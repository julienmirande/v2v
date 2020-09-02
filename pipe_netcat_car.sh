mkfifo pipe;
netcat -l -p 9001 < pipe;
