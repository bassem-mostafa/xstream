## #############################################################################
## #### Copyright ##############################################################
## #############################################################################

'''
Copyright 2024 BaSSeM

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

## #############################################################################
## #### Description ############################################################
## #############################################################################

## #############################################################################
## #### Control Variable(s) ####################################################
## #############################################################################

## #############################################################################
## #### Import(s) ##############################################################
## #############################################################################

import numpy
import cv2
from threading import Thread, Event
from collections import deque
from time import time

from xstream import XStream

## #############################################################################
## #### Private Type(s) ########################################################
## #############################################################################

## #############################################################################
## #### Private Method(s) Prototype ############################################
## #############################################################################

## #############################################################################
## #### Private Variable(s) ####################################################
## #############################################################################

## #############################################################################
## #### Private Method(s) ######################################################
## #############################################################################

def _moving_average(sample, mean=0, window=0, max_window=1):
    """
    Apply moving average filter on given `sample` with respect to supplied `mean`, `window`, and `max_window`
    """
    assert window >= 0, f"Argument `window` = `{window}` cannot be less than 0"
    assert max_window >= 1, f"Argument `max_window` = `{max_window}` cannot be less than 1"
    if window < max_window:
        window += 1
    mean = mean + (sample - mean) / window
    return mean, window

def _smooth(sample, old_sample, factor=1):
    """
    Apply smoothing filter on given `sample` with respect to supplied `old_sample`, and `factor`
    """
    assert 1 >= factor and factor >= 0, "Argument `factor` MUST be 1 >= factor >= 0"
    sample = factor * sample + (1 - factor) * old_sample
    return sample

def _resize(image, size):
    """
    Resize an `image` to the required `size` maintaining the image aspect ratio with padding
    """
    size = type("size", (), dict(height=size[0], width=size[1]))
    image = type("image", (), dict(canvas=image))
    image.height, image.width = image.canvas.shape[:2]
    # Resizing on higher dimension
    scale = type("scale", (), dict(height=image.height / size.height, width = image.width / size.width))
    image.resized = type("image.resized", (), dict(height=int(image.height/max([scale.width, scale.height])), width=int(image.width/max([scale.width, scale.height]))))
    image.resized.canvas = cv2.resize(image.canvas, (image.resized.width, image.resized.height), interpolation=cv2.INTER_LINEAR)
    
    # Padding
    pad = type("pad", (), {})
    pad.left   = (size.width - image.resized.width) // 2
    pad.right  = (size.width - image.resized.width) - pad.left
    pad.top    = (size.height - image.resized.height) // 2
    pad.bottom = (size.height - image.resized.height) - pad.top
    image.resized.padded = cv2.copyMakeBorder(image.resized.canvas,
                       top=pad.top,
                       bottom=pad.bottom,
                       left=pad.left,
                       right=pad.right,
                       borderType = cv2.BORDER_CONSTANT,
                       value=0,
                       )
    return image.resized.padded

## #############################################################################
## #### Public Method(s) Prototype #############################################
## #############################################################################

## #############################################################################
## #### Public Type(s) #########################################################
## #############################################################################

## #############################################################################
## #### Public Method(s) #######################################################
## #############################################################################

## #############################################################################
## #### Public Variable(s) #####################################################
## #############################################################################

## #############################################################################
## #### Main ###################################################################
## #############################################################################

if __name__ == "__main__":
    print(f"Stream class usage demo started")
    
    # Demo Thread Class
    class StreamThread(Thread):
        def __init__(self, name, source, queue):
            super().__init__(name=name)
            self.terminate = Event()
            self.source = source
            self.queue = queue
            self.capture_time = 0
            self.capture_rate = 9999
    
        def run(self):
            print(f"Thread `{self.name}` handling source `{self.source}` Started")                
            stream = XStream(self.source)
            if stream.open():
                average_window = 0
                time_start = time()
                for frame in stream:
                    time_end = time()
                    self.capture_time, average_window = _moving_average(time_end - time_start, self.capture_time, average_window, 5)
                    capture_rate = 1/self.capture_time if self.capture_time > 0 else 9999
                    self.capture_rate = _smooth(capture_rate, self.capture_rate, 0.01) if self.capture_rate != 9999 else capture_rate
                    if self.terminate.is_set(): break
                    self.queue.append(frame)
                    time_start = time()
                stream.close()
            print(f"Thread `{self.name}` Terminated")
    
    # list of threads to handle
    threads = [
        StreamThread(
            name="Internal Camera",
            source = 0,
            queue = deque(iterable = [], maxlen = 1)
            ),
        StreamThread(
            name="USB Camera",
            source = 1,
            queue = deque(iterable = [], maxlen = 1)
            ),
        StreamThread(
            name="Local Image",
            source = "sample.jpg",
            queue = deque(iterable = [], maxlen = 1)
            ),
        StreamThread(
            name="Local Video",
            source = "sample.mp4",
            queue = deque(iterable = [], maxlen = 1)
            ),
        StreamThread(
            name="RTSP",
            source = "rtsp://rtsp-test-server.viomic.com:554/stream", # useful rtsp from `https://github.com/grigory-lobkov/rtsp-camera-view/issues/3#issuecomment-1962084348`,
            queue = deque(iterable = [], maxlen = 1)
            ),
        StreamThread(
            name="Youtube",
            source = "https://www.youtube.com/watch?v=wDchsz8nmbo",
            queue = deque(iterable = [], maxlen = 1)
            ),
        ]
    
    # Start ALL threads
    for thread in threads:
        thread.start()
    
    # Set the following to `True` to display single window, `False` for multiple windows
    use_canvas = True
    if use_canvas:
        row_cells = 3
        width, height, channels = 320, 240, 3
        canvas = numpy.zeros((height * numpy.ceil(len(threads) / row_cells).astype(int), width * row_cells, channels), dtype=numpy.uint8)
    
    while True:
        canvas_index = -1
        for thread in threads:
            canvas_index += 1
            if len(thread.queue) < 1: continue
            frame = thread.queue.popleft()

            if not use_canvas:
                # This will show a window for EACH stream
                cv2.imshow(thread.name, frame)
            
            if use_canvas:
                # This will show single window for ALL streams
                frame = _resize(frame, (height, width))
                canvas[height * (canvas_index // row_cells) : height * (canvas_index // row_cells) + height,
                        width * (canvas_index % row_cells)  : width  * (canvas_index % row_cells)  + width,
                        :] = frame

                # The following is to highlight each stream in canvas
                text = type(f"text", (), {})
                text.content = f"{thread.name} {thread.capture_rate:6.1f} FPS"
                text.font = cv2.FONT_HERSHEY_SIMPLEX
                text.scale = 0.5
                text.thickness = 2
                text.size = cv2.getTextSize(
                                text.content,   # Text string
                                text.font,      # Font Family
                                text.scale,     # Font Scale
                                text.thickness  # Line Thickness in px
                                )
                (text.width, text.height), text.baseline = text.size
                text.linetype = cv2.LINE_AA
                cv2.putText(
                        img              = canvas,                                                  # Image to manipulate
                        text             = text.content,                                            # Text string to be written
                        org              = (width  * (canvas_index % row_cells),                    # Text bottom-left corner position
                                            height * (canvas_index // row_cells) + text.height),    
                        fontFace         = text.font,                                               # Font Family
                        fontScale        = text.scale,                                              # Font Scale
                        color            = (255, 255, 100),                                         # Color in BGR
                        thickness        = text.thickness,                                          # Line Thickness in px
                        lineType         = text.linetype,                                           # Line Type
                        bottomLeftOrigin = False                                                    # Image Origin bottom-left if True, top-left otherwise
                        )
        if use_canvas:
            cv2.imshow("canvas", canvas)
        key = cv2.waitKey(1)
        if key in [27, ord('q'), ord('Q')]:
            break

    # Wait for ALL threads to terminate
    for thread in threads:
        thread.terminate.set()
        thread.join()
    
    # Destroy all OpenCV opened windows
    cv2.destroyAllWindows()

    print(f"Stream class usage demo completed")
    
## #############################################################################
## #### END OF FILE ############################################################
## #############################################################################