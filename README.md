# Algorithm

1. Receive and store video from the client.
2. Process video.
   1. Look for specific hand gestures sequence.
      1. Capture previous gesture.
      2. If more than X seconds passed from last one, dump previous gestures.
   2. Record the position in video.
3. Send the positions to the client.

## Problems

- Processing takes too long.
- The model is really inaccurate from longer distances.

## Thoughts

- Hash videos to avoid analyzing the same video.
