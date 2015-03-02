import time
import cv2
import ipcv 
import numpy

def makeTarget(im, number, quantizeLevels, numberOfSeconds, verbose=False):

   print 'Making target ...' 

   for iteration in range(0,number):

      print 'iteration: ', iteration
      value = numpy.random.randint(1,5)
      print 'value: ', value

      if value == 1:   # blur 

         print '   Blurring'
         kernel = numpy.asarray([[1,1,1],[1,1,1],[1,1,1]])/9.0
         im = cv2.filter2D(im, -1, kernel)
         if verbose == True:
            cv2.imshow('target', im)
            cv2.waitKey(0)

      elif value == 2:   # sharpen
        
         print '   Sharpening'
         kernel = numpy.asarray([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
         im = cv2.filter2D(im, -1, kernel)
         if verbose == True:
            cv2.imshow('target', im)
            cv2.waitKey(0)

      elif value == 3:   # quantize

         print '   Quantizing'
         im = ipcv.quantize(im, quantizeLevels, qtype='uniform', displayLevels=256)
         if verbose == True:
            cv2.imshow('target', im)
            cv2.waitKey(0)

      else:   # invert

         print '   Inverting' 
         im = numpy.abs(im.astype(numpy.float64)-255.0).astype(numpy.uint8)
         if verbose == True:
            cv2.imshow('target', im)
            cv2.waitKey(0)

   return im

def play(target, im, number, playMenu, beginningPlayer):

   imRows, imColumns, imBands, dataType = ipcv.dimensions(im)
   print imRows
   print imColumns
#   cv2.namedWindow(player + ' is playing', cv2.WINDOW_AUTOSIZE)
   
   # Make window for target (left) and player's image (right)
   window = numpy.zeros((imRows+150,2*imColumns,imBands),dtype=dataType)  
   
   # Player __  begins
   window[0:imRows,0:2*imColumns,:] = beginningPlayer
   window[imRows:imRows+150,:,:] = playMenu
   cv2.imshow('DIP Game', window)
   cv2.waitKey(0)

   window[0:imRows,0:imColumns,:] = target
   window[0:imRows,imColumns:2*imColumns,:] = im 
   cv2.imshow('DIP Game', window)

   for iteration in range(0,number):

      key = cv2.waitKey(0)

      if key == 98: # W Blur
         print '   Blurring'
         kernel = numpy.asarray([[1,1,1],[1,1,1],[1,1,1]])/9.0
         im = cv2.filter2D(im, -1, kernel)
         window[0:imRows,imColumns:2*imColumns,:] = im[:,:,:]
         cv2.imshow('DIP Game', window)
   
      if key == 115: # A Sharpen 
         
         print '   Sharpen'
         kernel = numpy.asarray([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
         im = cv2.filter2D(im, -1, kernel)
         window[0:imRows,imColumns:2*imColumns,:] = im[:,:,:]
         cv2.imshow('DIP Game', window)

      if key == 113: # Quantize
         print '   Quantize'
         im = ipcv.quantize(im, quantizeLevels, qtype='uniform', displayLevels=256)
         window[0:imRows,imColumns:2*imColumns,:] = im[:,:,:]
         cv2.imshow('DIP Game', window)

      if key == 105: # Invert
         print '   Inverting'
         im = numpy.abs(im.astype(numpy.float64)-255.0).astype(numpy.uint8)
         window[0:imRows,imColumns:2*imColumns,:] = im[:,:,:]
         cv2.imshow('DIP Game', window)

   time.sleep(2)
   # After done, calculate psnr and delta E
   psnr = ipcv.demosaic.psnr(target,im)
   deltaE = numpy.mean(ipcv.demosaic.deltaE(target,im))

   return im, psnr, deltaE

   

if __name__ == '__main__':

   import cv2
   import ipcv
   import numpy

   filename = '/cis/faculty/cnspci/public_html/courses/common/images/lenna_color.tif'
   im = cv2.imread(filename, cv2.CV_LOAD_IMAGE_UNCHANGED)
   imRows, imColumns, imBands, dataType = ipcv.dimensions(im)

   player1B = cv2.imread('begin_player1.tif', cv2.CV_LOAD_IMAGE_UNCHANGED)
   player2B = cv2.imread('begin_player2.tif', cv2.CV_LOAD_IMAGE_UNCHANGED)
   playMenu = cv2.imread('play_menu.tif', cv2.CV_LOAD_IMAGE_UNCHANGED)
   player1W = cv2.imread('player1_wins.tif', cv2.CV_LOAD_IMAGE_UNCHANGED)
   player1L = cv2.imread('player1_loses.tif', cv2.CV_LOAD_IMAGE_UNCHANGED)
   player2W = cv2.imread('player2_wins.tif', cv2.CV_LOAD_IMAGE_UNCHANGED)
   player2L = cv2.imread('player2_loses.tif', cv2.CV_LOAD_IMAGE_UNCHANGED)
   intro = cv2.imread('intro.tif', cv2.CV_LOAD_IMAGE_UNCHANGED)
   play_again = cv2.imread('play_again.tif', cv2.CV_LOAD_IMAGE_UNCHANGED)
   grey_bar = cv2.imread('grey_bar.tif', cv2.CV_LOAD_IMAGE_UNCHANGED)
   howToPlay = cv2.imread('how_to_play2.tif',cv2.CV_LOAD_IMAGE_UNCHANGED)

   number = 5   # Number of enhancements applied to image to make target
   quantizeLevels = 7   # Levels to quantize
   secondsOfPlay = 30

   showTargetMake = False
   #showTargetMake = True
   
   key = 121
   while key == 121:
   
      target = ipcv.makeTarget(im.astype('uint8'), number, quantizeLevels, secondsOfPlay, verbose=showTargetMake)
  
   #if showTargetMake == True: 
   #   cv2.imshow('target', target)
   #   cv2.waitKey(0)   

      cv2.namedWindow('DIP Game', cv2.WINDOW_AUTOSIZE)
      window = numpy.zeros((imRows+150,2*imColumns,imBands),dtype=dataType)
      window[0:imRows,:,:] = intro
      window[imRows:imRows+150,:,:] = grey_bar
      cv2.imshow('DIP Game', window)
      cv2.waitKey(0)

      window[0:imRows,:,:] = howToPlay
      window[imRows:imRows+150,:,:] = playMenu
      cv2.imshow('DIP Game', window)
      cv2.waitKey(0)

      im1, psnr1, deltaE1 = play(target, im, number, playMenu, player1B)
      print 'Player 1 PSNR: ', psnr1
      print 'Player 1 Delta E: ', deltaE1

      im2, psnr2, deltaE2 = play(target, im, number, playMenu, player2B)

      print 'Player 2 PSNR: ', psnr2
      print 'Player 2 Delta E: ', deltaE2

      if psnr1 > psnr2: # and deltaE1 < deltaE2:
         print '\nPlayer 1 wins! '
         window[0:imRows,0:imColumns,:] = player1W
         window[0:imRows, imColumns:2*imColumns,:] = player2L
         window[imRows:imRows+150,:,:] = play_again
         cv2.imshow('DIP Game', window)
         key = cv2.waitKey(0)

      else:
         print '\nPlayer 2 wins! ' 
         window[0:imRows,0:imColumns,:] = player1L
         window[0:imRows, imColumns:2*imColumns,:] = player2W
         window[imRows:imRows+150,:,:] = play_again
         cv2.imshow('DIP Game', window)
         key = cv2.waitKey(0)

