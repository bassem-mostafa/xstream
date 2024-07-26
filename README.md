# X-Stream
X-Stream is a multi-source stream with a unified interface

# Currently Supported
- [x] RTSP streams 
- [x] Youtube streams 
- [x] Internal/USB camera streams 
- [x] Local video/image streams 
- [ ] ... others to be supported 

---

# Reference(s)
- [pafy introduction](https://www.geeksforgeeks.org/introduction-to-pafy-module-in-python/)
- [pafy know-how](https://www.geeksforgeeks.org/pafy-getting-https-url-of-stream/)
- [youtube stream handling](https://stackoverflow.com/questions/37555195/is-it-possible-to-stream-video-from-https-e-g-youtube-into-python-with-ope)
- [OpenCV real time stream](https://stackoverflow.com/questions/58293187/opencv-real-time-streaming-video-capture-is-slow-how-to-drop-frames-or-get-sync)

# Known Issue(s)
- If encountered any error related to `pafy`\
  make sure you've installed both `pafy` and `youtube-dl`\
  using `python3 -m pip install -U youtube-dl pafy` command\
  Also, refer to the following link(s) 
    - `https://stackoverflow.com/a/75602237`
    - `https://github.com/mps-youtube/pafy/pull/288#issuecomment-812841914`
    - `https://stackoverflow.com/a/75504772`
