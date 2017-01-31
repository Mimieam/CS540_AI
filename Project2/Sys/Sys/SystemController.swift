//
//  SystemController.swift
//  VysSys
//
//  Created by Aman Miezan Echimane on 12/2/15.
//  Copyright © 2015 Miezel. All rights reserved.
//
import UIKit
import Foundation

class VySys {
    
    var original:UIImage!
    var Manager: VSImage!
    var view: UIImageView!
    var MainViewController:ViewController?
    var lines:[(p1:point2D, p2:point2D)]!
    var axis:[(p1:point2D, p2:point2D)]!

    init( img:UIImage){
        
        self.Manager = VSImage(img: img, scaleDownBy: 1)
        self.original = Manager.modified.display()
        self.view = UIImageView()
        
        
        lines = []
        axis = [((1,1),(1, original.size.width)), ((1, 1), (original.size.height, 1)) ]
    }
    
    
    func setView(let _view:UIImageView) {
        self.view = _view
        print(self.view.frame.size)
        self.view.sizeThatFits(self.original.size)
    }
    
    func addViewController(let vc:ViewController ){
        self.MainViewController = vc
    }
    
    func start(let brightness:Int=110, let contrast:Int=5) {
        let w =  self.original.size.width
        let h =  self.original.size.height
//        anisotropicDiffusion(self.Manager.original.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h))



//        Brightness(self.Manager.original.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h), brightness: 110)
////
//        Contrast(self.Manager.original.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h), contrast: 1)

        
        
//        Convolve(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), Mask:MASKS.LaplacianOfGaussianMask) //edge_detection
//        GeometricMean(self.Manager.original.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h) )
//
//        Mean(self.Manager.modified.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h))//,windowSize: 9 )
        //
//        HistogramEqualization(&self.Manager.original.pixelPtr, w: Int(w) , h:Int(h))
        //

//
//
//        Convolve(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), Mask:[[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
        Median(self.Manager.original.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h) )
//        Convolve(self.Manager.original.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h), Mask:MASKS.Gaussian5X5Mask, maskCoeff:(1/159))
        
//        Convolve(self.Manager.original.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h), Mask:MASKS.Gaussian7X7Mask, maskCoeff:(1/159))
//        Convolve(self.Manager.modified.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h), Mask:MASKS.Gaussian5X5Mask, maskCoeff:(1/159))
//        Convolve(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), Mask:MASKS.Gaussian7X7Mask, maskCoeff:(1/159))
        
//        Dilation(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), Mask:[[1,1,1],[1,1,1],[1,1,1]])

//        Erosion(self.Manager.modified.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h), Mask:[[1,1,1],[1,1,1],[1,1,1]])
        
//        Erosion(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), Mask:[[1,1,1],[1,1,1],[1,1,1]])
        
//        Mean(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h) )
        
//        Outline(self.Manager.modified.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h), Mask:[[0,0,0],[0,1,0],[0,0,0]])
//        
//        //sharpening
        Convolve(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), Mask:[[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
//        //sharpening
//        Convolve(self.Manager.modified.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h), Mask:[[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
//       //edge_detection

//        //smoothing

//        //edge detection
         Convolve(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), Mask:MASKS.LaplacianOfGaussianMask)
        KirschEdges(&self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), thresh: 200)
//        lineDetector4Direction(&self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h))
//
//        
//        applyHighTreshold(self.Manager.modified.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h), tresh: 0)
//        CloseGray(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.original.pixelPtr, w: Int(w) , h:Int(h), Mask:[[1,1,1],[1,1,1],[1,1,1]])
////
////
//////        SobelGradientImg(&self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), thresh: 0)
////        
//////        thinningIteration(binarize(self.Manager.modified.pixelPtr, w: Int(w), h: Int(h)), outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), iter: 0)
////
////       
//        Skeleton(self.Manager.original.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), Mask: [[0,1,0],[0,1,0],[0,1,0]])
////
////        applyLowTreshold(self.Manager.original.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), tresh: 200)
//        
//
//        
////        thinningIteration(self.Manager.modified.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), iter: 0)
////        thinningIteration(self.Manager.modified.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), iter: 1)
////        
////        binarize(self.Manager.modified.pixelPtr, w: Int(w), h: Int(h), Flag: false)
////        Convolve(self.Manager.modified.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h), Mask:MASKS.LaplacianOfGaussianMask) //edge_detection
//
////
////        Contrast(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), contrast: 10)
////        GeometricMean(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h) , windowSize: 9)
//
//        
////        Convolve(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), Mask:MASKS.LaplacianOfGaussianMask) //edge_detection
//        
//     
////        Erosion(self.Manager.modified.pixelPtr, outputImg: &self.Manager.buffer.pixelPtr, w: Int(w) , h:Int(h), Mask:[[1,1,1],[1,1,1],[1,1,1]])
////        Erosion(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), Mask:[[1,1,1],[1,1,1],[1,1,1]])
//
//        // extra geometrical shapes... DANGEROUS !
////        HitMiss(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h))
////        Convolve(self.Manager.buffer.pixelPtr, outputImg: &self.Manager.modified.pixelPtr, w: Int(w) , h:Int(h), Mask:[[0,1,0],[1,-4,1],[0,1,0]])
//        let linesDetected = HoughTransform(self.Manager.modified.pixelPtr, w: Int(w), h: Int(h), thresh: 100)
//////        for var (rho, theta) in linesDetected{
//////            rho
//////        }
//        self.lines = axis + GetLines(linesDetected)
//        //self.view.image = overlayLinesOnImage(self.Manager.modified.display(), lines: [( (1,1) , (1,w)), ( (1,1) , (h,1))])
        // LOOK @ startProcessingThread() it's the one diplaying the result from the MODIFIED buffer only it replaces the line above
    }
    
}