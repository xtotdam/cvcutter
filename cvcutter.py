#!/usr/bin/python2

import cv2
from glob import glob
import numpy as np
import os
import sys

save_jpgs_too = False

srcfolder = sys.argv[-1]

if save_jpgs_too:
    folder = 'out'
    try:
        os.mkdir(srcfolder + os.sep + folder)
    except OSError:
        print 'Can\'t create ' + folder + ' folder. Maybe it exists? pass\n'
        pass
    
pngfolder = 'outpng'
try:
    os.mkdir(srcfolder + os.sep + pngfolder)
except OSError:
    print 'Can\'t create ' + pngfolder + ' folder. Maybe it exists? pass\n'
    pass


for f in sorted(glob(srcfolder + os.sep + '*.jpg')):
    orig = cv2.imread(f)

    # TODO add preferred rotation direction via sys.argv
    if orig.shape[0] > orig.shape[1]:
        orig = np.rot90(orig)

    size = np.array(orig.shape)[1::-1]
    figsize = size / 250.
    print '{}: size {} x {}'.format(f, size[0], size[1])

    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (49, 49), 0)
    ret, th = cv2.threshold(blur, 
                            200, 
                            255, 
                            cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    verhist = np.sum(th, axis=0) / 255. / size[1]
    horhist = np.sum(th, axis=1) / 255. / size[0]
    
    def borders(hist, d, frac=0.5, error=0.04):
        '''
            Arguments:
            hist    - image histogram in 'd' direction
            d       - direction; is in ('h','v')
            frac    - fraction between 'all black' and 'all white' to be border
            error   - resulting area will be increased in 'error' * size in every 
                direction

            Returns:
            xmin    - left border of our region
            xmax    - right border of our region
            
            Not very good version of borders recognising function, 
            just takes whole white region instead of finding the biggest one
            But it is simple at least
        '''

        x = np.where(hist > frac * np.max(hist))
        xmin, xmax = \
            np.min(x) - error * len(hist), \
            np.max(x) + error * len(hist)
        
        # catching 'out of border'
        if xmin < 0: 
            xmin = 0
        if xmax > len(hist)-1: 
            xmax = len(hist)-1

        return int(xmin), int(xmax)
    
    def bordersx(hist, d, frac=0.4, error=0.04):
        '''
            Arguments:
            hist    - image histogram in 'd' direction
            d       - direction; is in ('h','v')
            frac    - fraction between 'all black' and 'all white' to be border
            error   - resulting area will be increased in 'error' * size in every 
                direction

            Returns:
            xmin    - left border of our region
            xmax    - right border of our region
            b       - compatibility with bordersx()

            This one recognises white region with biggest area. This creates 
            problem with zeros in histogram, which I hope is now solved
        '''
        # to recognise white at the edge of image
        hist[0] = 0
        hist[-1] = 0

        # I define border like point where histogram goes from '+' to '-' 
        #   and vice versa
        hist -= frac * np.max(hist)
        
        # Trying to get rid of zeros
        for i in xrange(1, hist.shape[0] - 1):
            if hist[i] == 0:
                print d.upper() + '. Trying to fix zeros on', i, ':', hist[i-1:i+2],
                hist[i] = hist[i-1] * hist[i+1]
                print ' -> ', hist[i-1:i+2]
        
        b = list()
        # Finding potential borders
        for i in xrange(0, hist.shape[0] - 1):
            if hist[i] * hist[i+1] <= 0:
                b.append(i)                
                
        # print d.upper() + '. Borders: ', len(b), b
            
        xmin = 0
        xmax = len(hist) - 1
        mdx = 0
        # Finding the biggest white region
        for i in range(0, len(b), 2):
            if b[i+1] - b[i] > mdx:
                mdx = b[i+1] - b[i]
                xmin = b[i]
                xmax = b[i+1]        
        
        xmin -= error * len(hist)
        xmax += error * len(hist)
        
        # Catching 'out of range'
        if xmin < 0: 
            xmin = 0
        if xmax > len(hist)-1: 
            xmax = len(hist)-1
        
        return int(xmin), int(xmax)
    
    xmin, xmax = bordersx(verhist, 'h')
    ymin, ymax = bordersx(horhist, 'v')
    print 'Result size: {} x {} @ [{}, {}]->[{}, {}]'.format(
        xmax-xmin, ymax-ymin, xmin, ymin,xmax, ymax)
           
    th2 = cv2.adaptiveThreshold(gray[ymin:ymax, xmin:xmax], 
                                150, 
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                cv2.THRESH_BINARY, 
                                49, 
                                15)
    
    ret, th3 = cv2.threshold(th2, 100, 255, cv2.THRESH_BINARY)

    if save_jpgs_too:
        outf = srcfolder + os.sep + folder + os.sep + f.split(os.sep)[-1]
        print 'Saving jpg to ', outf
        cv2.imwrite(outf, th3)

    outfpng = srcfolder + os.sep + pngfolder + os.sep + f.split(os.sep)[-1] + '.png'
    print 'Saving png to ', outfpng
    cv2.imwrite(outfpng, th3)

    print '='*70