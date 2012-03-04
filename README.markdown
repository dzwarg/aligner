# Aligner

Aligner is a tool for shifting images one at a time out of a sequence of images.

## Requirements

Python and PyGTK are required to run Aligner.

## Usage

    ./aligner.py -i path/to/images/
    
**Note**: the trailing slash is required.

When the application loads, it will display the first image file (sorted by filename)
in the provided directory. When the image is loaded and displayed, the following keys
navigate through the images:

 * Up arrow: nudge image up 1 pixel
 * Down arrow: nudge image down 1 pixel
 * Right arrow: nudge image right 1 pixel
 * Left arrow: nudge image left 1 pixel
 * PageDown: load the next image
 * PageUp: load the previous image
 * Escape: quit
