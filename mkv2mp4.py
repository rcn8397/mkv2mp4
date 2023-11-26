#!/usr/bin/env python3
import pdb
import os, sys
from pycore.core.fsutil import *
import subprocess

class Converter( object ):
    def __init__( self, path, output = './outputs', verbose = True, debug = False ):
        self.path = path
        self.output = output
        self.inputs = None
        self.outputs = []
        self.find_files()
        self.calc_outputs()
        self.validate()

    def find_files( self, ext = 'mkv' ):
        print( 'find all the things' )
        walker = FileWalker( self.path )
        self.inputs = walker.find( ext )

    def replace_ext( self, path ):
        fname, ext = os.path.splitext( path )
        replaced   = '{}.mp4'.format( fname )
        return( replaced )
                
    def path2output( self, path ):
        dirname    = os.path.dirname( path )
        basename   = os.path.basename( path )
        fname, ext = os.path.splitext( basename )
        replaced   = '{}.mp4'.format( fname )
        output     = os.path.join( self.output, replaced )
        return( output )

    def calc_outputs( self ):
        for path in self.inputs:
            self.outputs.append( self.path2output( path ) )

    def validate( self ):
        self.compare_inputs2outputs()

    def compare_inputs2outputs( self ):
        if len( self.inputs ) != len( self.outputs ):
            sys.exit( 'Size of inputs does not match outputs' )

    def convert( self, src, dest ):
        assert( os.path.exists( src ) )
        cmd = [
            'ffmpeg',
            '-i', '{}'.format( src ),
            '-c', 'copy', '{}'.format( dest )
        ]
        print( cmd )
        proc = subprocess.run( cmd, capture_output = True )
        print( proc.stdout )
        
    def inplace_convert( self ):
        for path in self.inputs:
            output = self.replace_ext( path )
            print( output )
            self.convert( path, output )
            #pdb.set_trace() 

    

def main(args):
    converter = Converter( path = args.path, verbose = args.verbose )

    converter.inplace_convert()
    
    pdb.set_trace()
    

    print( cmd )
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser( description='mkv2mp4' )

    # Common parameters
    parser.add_argument( '-p', '--path', help='Input path (defaults: .)', default = '.' )
    parser.add_argument( '-s', '--sine',
                         help   = 'Create since source', 
                         action ='store_true' )

    parser.add_argument( '-v', '--verbose',
                         help   = 'Increase verbosity',
                         action ='store_true' )

    # Parse the arguments
    args = parser.parse_args()

    # Process the subcommand
    main( args )

