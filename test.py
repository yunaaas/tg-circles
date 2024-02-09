import moviepy.editor as mp
import moviepy.video.fx.all as vfx
    
# Create a temp video clip for this example

# This is where you load in your original clip    
clip_16_9 = mp.VideoFileClip("start.mp4")
    
# Now lets crop out a 9:16 section from the original
# x1=0, y1=0 will take the section from the top left corner
clip_9_16 = vfx.crop(clip_16_9, x1=0, y1=0, width=500, height=500)
clip_9_16.write_videofile("output.mp4")