# size of input is: 1280x528
INPUT=header-video-source.mp4

DURATION=00:00:10
FFMPEG=ffmpeg -i $(INPUT) -t $(DURATION) -an

ALL=header-video-1024.webm header-video-1280.webm header-video-1024.mp4 header-video-1280.mp4
ALL: $(ALL)

#Mobile:
#$FFMPEG -vf crop=320:528:480:191 header-video-320.mp4
#$FFMPEG -vf crop=640:720:320:0   header-video-640.mp4

# 320x568
header-video-320.mp4:
	$(FFMPEG) -vf crop=320:528:480:0 $@

header-video-320.webm:
	$(FFMPEG) -vf crop=320:528:480:0 -c:v libvpx -b:v 0.4M $@

header-video-1024.mp4:
	$(FFMPEG) -vf crop=1024:528:128:0 $@

header-video-1024.webm:
	$(FFMPEG) -vf crop=1024:528:128:0 -c:v libvpx -b:v 1.2M $@

header-video-1280.mp4:
	$(FFMPEG) -vf scale=1280:-1 $@

header-video-1280.webm:
	$(FFMPEG) -vf scale=1280:-1 -c:v libvpx -b:v 1.7M $@



.PHONY: clean
clean:
	rm -rf $(ALL)
