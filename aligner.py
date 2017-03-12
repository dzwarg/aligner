#!/usr/bin/env python
# Copyright (c) 2012 David Zwarg
# david.zwarg@gmail.com
# http://www.zwarg.com/
#
# An image alignment tool.  This tool will allow one to cycle through
# a folder full of images, and nudge each image individually.
#
# Pass in a directory full of images with the -i command line option.
#
# Commands:
#    next image: Page_Down
#    prev image: Page_Up
#    nugde: arrow keys (Left, Right, Down, Up)
#    quit: Esc

import pygtk
import gtk
from optparse import OptionParser
import glob
import os

class Aligner:
    """
    Create a class for the main application.
    """
    def __init__(self, folder):
        """
        Intialize the Aligner class. Load the image files, create
        the window and context, and show the first image.
        
        @param folder: The folder name from where to load images.
        """
        self.changed = False
        self.files = glob.glob( folder + '/*.jpg' )
        if len(self.files) < 2:
            raise IOError('No files found in the input folder.')
            
        self.files.sort()
        self.index = 0
        
        self.image = gtk.Image()
        self.image.set_from_file( self.files[self.index] )
        self.image.show()
        
        self.status = gtk.Statusbar()
        context = self.status.get_context_id("statusbar")
        self.status.push( context, self.files[self.index] )
        self.status.show()
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.connect("key_press_event", self.keypress)
        
        vbox = gtk.VBox(False,1)
        self.window.add(vbox)
        vbox.show()
        
        vbox.pack_start(self.image, False, 0)
        vbox.pack_start(self.status, False, 0)
        
        self.window.show()

    def destroy(self, widget, data=None):
        """
        Quit the application.
        """
        gtk.main_quit()

    def keypress(self, widget, data):
        """
        Respond to a key press event.
        """
        context = self.status.get_context_id("statusbar")
        keyname = gtk.gdk.keyval_name(data.keyval)
        if keyname == 'Left':
            self.wrap( self.files[self.index], -1, 0 )
        elif keyname == 'Right':
            self.wrap( self.files[self.index], 1, 0 )
        elif keyname == 'Up':
            self.wrap( self.files[self.index], 0, -1 )
        elif keyname == 'Down':
            self.wrap( self.files[self.index], 0, 1 )
        elif keyname == 'Page_Down':
            if self.changed:
                pixbuf = self.image.get_pixbuf()
                pixbuf.save(self.files[self.index], "jpeg", {"quality":"100"})
                self.changed = False

            if self.index == len(self.files) - 1:
                self.index = 0
            else:
                self.index += 1
                
            self.status.pop(context)
            self.status.push(context,self.files[self.index])
            
            self.image.set_from_file( self.files[self.index] )
            self.image.show()
        elif keyname == 'Page_Up':
            if self.changed:
                pixbuf = self.image.get_pixbuf()
                pixbuf.save(self.files[self.index], "jpeg", {"quality":"100"})
                self.changed = False

            if self.index == 0:
                self.index = len(self.files) - 1
            else:
                self.index -= 1

            self.status.pop(context)
            self.status.push(context,self.files[self.index])

            self.image.set_from_file( self.files[self.index] )
            self.image.show()
        elif keyname == 'Escape':
            gtk.main_quit()
        else:
            print 'Unrecognized keycode/keyname: %d/%s' % (data.hardware_keycode, keyname)

    def wrap(self, img, x, y):
        """
        Wrap an image pixel data around it's edge.
        
        @param img: The image. Seems to be ignored.
        @param x: The amount to shift in the X coordinate.
        @param y: The amount to shift in the Y coordinate.
        """
        pixbuf0 = self.image.get_pixbuf()
        pixbuf1 = gtk.gdk.Pixbuf( gtk.gdk.COLORSPACE_RGB, False, 8, pixbuf0.get_width(), pixbuf0.get_height() )
        
        # twiddle the bits
        if x == 0:
            if y < 0:
                pixbuf0.copy_area( x, 1, pixbuf0.get_width(), pixbuf0.get_height()-1, pixbuf1, x, 0 )
                pixbuf0.copy_area( x, 0, pixbuf0.get_width(), 1, pixbuf1, x, pixbuf0.get_height()-1 )
            else: # y > 0:        
                pixbuf0.copy_area( x, 0, pixbuf0.get_width(), pixbuf0.get_height()-1, pixbuf1, x, 1 )
                pixbuf0.copy_area( x, pixbuf0.get_height()-1, pixbuf0.get_width(), 1, pixbuf1, x, 0 )
        elif x < 0:
            pixbuf0.copy_area( 0, y, 1, pixbuf0.get_height(), pixbuf1, pixbuf0.get_width()-1, y )
            pixbuf0.copy_area( 1, y, pixbuf0.get_width()-1, pixbuf0.get_height(), pixbuf1, 0, y )
        else: # x > 0:        
            pixbuf0.copy_area( 0, y, pixbuf0.get_width()-1, pixbuf0.get_height(), pixbuf1, 1, y )
            pixbuf0.copy_area( pixbuf0.get_width()-1, y, 1, pixbuf0.get_height(), pixbuf1, 0, y )

        self.changed = True;                
        self.image.set_from_pixbuf( pixbuf1 )
        self.image.show()
        
    def main(self):
        """
        The main loop for this class
        """
        gtk.main()

if __name__ == "__main__":
    oParser = OptionParser()
    oParser.add_option("-i","--input",dest="input", help="specify an input folder")
    (options, args) = oParser.parse_args()
    
    if options.input is None:
        print "Please provide an input folder with -i or --input"
        exit(1)

    input = os.path.abspath(options.input)
    if not os.path.exists(input):
        print "The provided input folder does not exist."
        exit(1)

    align = Aligner(input)
    align.main()

