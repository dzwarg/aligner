#!/usr/bin/env python
# Author: David Zwarg, http://www.zwarg.com/
#
# An image alignment tool.  This tool will allow one to cycle through
# a folder full of images, and nudge each image individually.
#
# Pass in a directory full of images with the -i command line option.
#
# Commands:
#    next image: PgDn
#    prev image: PgUp
#    nugde: arrow keys (Left, Right, Down, Up)
#    quit: Esc

import pygtk;
import gtk;
from optparse import OptionParser;
import glob;

class Aligner:
	def __init__(self, folder):
		self.changed = False;
		self.files = glob.glob( folder + "*.jpg" );
		if ( len(self.files) < 2 ):
			gtk.main_quit();
			
		self.files.sort();
		self.index = 0;
		
		self.image = gtk.Image();
		self.image.set_from_file( self.files[self.index] );
		self.image.show();
		
		self.status = gtk.Statusbar();
		context = self.status.get_context_id("statusbar");
		self.status.push( context, self.files[self.index] );
		self.status.show();
		
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL);
		self.window.connect("destroy", self.destroy);
		self.window.connect("key_press_event", self.keypress);
		
		vbox = gtk.VBox(False,1);
		self.window.add(vbox);
		vbox.show();
		
		vbox.pack_start(self.image, False, 0);
		vbox.pack_start(self.status, False, 0);
		
		self.window.show();

	def destroy(self, widget, data=None):
		gtk.main_quit();

	def keypress(self, widget, data):
		context = self.status.get_context_id("statusbar");
		if (data.hardware_keycode == 100):
			self.wrap( self.files[self.index], -1, 0 );
		elif (data.hardware_keycode == 102):
			self.wrap( self.files[self.index], 1, 0 );
		elif (data.hardware_keycode == 98):
			self.wrap( self.files[self.index], 0, -1 );
		elif (data.hardware_keycode == 104):
			self.wrap( self.files[self.index], 0, 1 );
		elif (data.hardware_keycode == 105):
			if ( self.changed ):
				pixbuf = self.image.get_pixbuf();
				pixbuf.save(self.files[self.index], "jpeg", {"quality":"100"});
				self.changed = False;

			if ( self.index == len(self.files) - 1 ):
				self.index = 0;
			else:
				self.index += 1;
				
			self.status.pop(context);
			self.status.push(context,self.files[self.index]);
			
			self.image.set_from_file( self.files[self.index] );
			self.image.show();
		elif (data.hardware_keycode == 99):
			if ( self.changed ):
				pixbuf = self.image.get_pixbuf();
				pixbuf.save(self.files[self.index], "jpeg", {"quality":"100"});
				self.changed = False;

			if (self.index == 0):
				self.index = len(self.files) - 1;
			else:
				self.index -= 1;

			self.status.pop(context);
			self.status.push(context,self.files[self.index]);

			self.image.set_from_file( self.files[self.index] );
			self.image.show();
		elif (data.hardware_keycode == 9):
			gtk.main_quit();
		elif (data.hardware_keycode == 21):
			print "More Opaque";
		elif (data.hardware_keycode == 20):
			print "More Transparent";
		else:
			print data.hardware_keycode;

	def wrap(self, img, x, y):
		pixbuf0 = self.image.get_pixbuf();
		pixbuf1 = gtk.gdk.Pixbuf( gtk.gdk.COLORSPACE_RGB, False, 8, pixbuf0.get_width(), pixbuf0.get_height() );
		
		# twiddle the bits
		if ( x == 0 ):
			if ( y < 0 ):
				pixbuf0.copy_area( x, 1, pixbuf0.get_width(), pixbuf0.get_height()-1, pixbuf1, x, 0 );
				pixbuf0.copy_area( x, 0, pixbuf0.get_width(), 1, pixbuf1, x, pixbuf0.get_height()-1 );
			else: # ( y > 0 ):		
				pixbuf0.copy_area( x, 0, pixbuf0.get_width(), pixbuf0.get_height()-1, pixbuf1, x, 1 );
				pixbuf0.copy_area( x, pixbuf0.get_height()-1, pixbuf0.get_width(), 1, pixbuf1, x, 0 );
		elif ( x < 0 ):
			pixbuf0.copy_area( 0, y, 1, pixbuf0.get_height(), pixbuf1, pixbuf0.get_width()-1, y );
			pixbuf0.copy_area( 1, y, pixbuf0.get_width()-1, pixbuf0.get_height(), pixbuf1, 0, y );
		else: # ( x > 0 ):		
			pixbuf0.copy_area( 0, y, pixbuf0.get_width()-1, pixbuf0.get_height(), pixbuf1, 1, y );
			pixbuf0.copy_area( pixbuf0.get_width()-1, y, 1, pixbuf0.get_height(), pixbuf1, 0, y );

		self.changed = True;				
		self.image.set_from_pixbuf( pixbuf1 );
		self.image.show();
		
	def main(self):
		gtk.main();

if __name__ == "__main__":
	oParser = OptionParser();
	oParser.add_option("-i","--input",dest="input", help="specify an input folder");
	(options, args) = oParser.parse_args();
	
	if ( options.input is None ):
		print "Please provide an input folder with -i or --input";
		exit(1);

	align = Aligner( options.input );
	align.main();

