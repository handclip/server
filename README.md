# Algorithm

1. Receive and store video from the client.
2. Process video.
   1. Look for hand gestures (open --> closed --> open --> closed).
      1. Capture 4 previous gesture.
      2. If more than 3 seconds passed from last one, dump previous gestures.
   2. Record the position in video.
3. Send the positions to the client.

## Thoughts

- Hash videos to avoid analyzing the same video.
