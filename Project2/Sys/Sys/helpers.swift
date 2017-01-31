//
//  helpers.swift
//  Sys
//
//  Created by Aman Miezan Echimane on 12/3/15.
//  Copyright © 2015 Miezel. All rights reserved.
//

import Foundation
import CoreGraphics
import UIKit

func Transform1Dto2D (let _1D:UnsafeMutablePointer<UInt8>, let width:Int, let height:Int) ->[[UInt8]] {
    var pixel2D = [[UInt8]](count: height, repeatedValue: [UInt8](count: width, repeatedValue: 0))
    for (var row = 0; row < height; row++) {
        for (var col = 0; col < width; col++) {
            pixel2D[row][col] =  _1D[(row * width + col)];
        }
    }
    return pixel2D;
}


func Transform2Dto1D (let _2D:[[UInt8]], _1D:UnsafeMutablePointer<UInt8>, let width:Int, let height:Int) -> UnsafeMutablePointer<UInt8>{
    for (var row = 0; row < height; row++) {
        for (var col = 0; col < width; col++) {
            _1D[(row * width + col)] = _2D[row][col];
        }
    }
    return _1D;
}

struct SobelMasks {
    var Sx = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]
    var Sy = [
        [1 ,2, 1],
        [0 ,0, 0],
        [-1, -2 ,-1]
    ]
}


struct LineDetectorMasks {
    var H = [
        [-1, -1, -1],
        [2, 2, 2],
        [-1, -1, -1]
    ]
    var V = [
        [-1, 2, -1],
        [-1, 2, -1],
        [-1, 2, -1]
    ]
    var LD = [
        [2, -1, -1],
        [-1, 2, -1],
        [-1, -1, 2]
    ]
    var RD = [
        [-1, -1, 2],
        [-1, 2, -1],
        [2, -1, -1]
    ]
}


struct KirschMasks {
    
    var N = [
        [-3, -3, 5],
        [-3, 0 , 5],
        [-3, -3, 5],
    ]
    var NW = [
        [-3, 5 , 5],
        [-3, 0 , 5],
        [-3, -3, -3],
    ]
    var W = [
        [5, 5,  5],
        [-3,0 , -3],
        [-3,-3, -3],
    ]
    var SW = [
        [5 , 5 , -3],
        [5 , 0 , -3],
        [-3, -3, -3],
    ]
    var S = [
        [5, -3, -3],
        [5, 0 , -3],
        [5, -3, -3],
    ]
    var SE  = [
        [-3, -3, -3],
        [5 , 0 , -3],
        [5 , 5 , -3],
    ]
    var E = [
        [-3, -3, -3],
        [-3, 0 , -3],
        [5 , 5 , 5],
    ]
    var NE = [
        [-3, -3,-3],
        [-3, 0, 5],
        [-3, 5, 5],
    ]
    
}


struct FilterMasks {
    var LaplacianOfGaussianMask:[[Int]]=[[0,0,-1,0,0],
    [0,-1,-2,-1,0],
    [-1,-2,16,-2,-1],
    [0,-1,-2,-1,0],
    [0,0,-1,0,0]]
    
    var Gaussian7X7Mask:[[Int]]=[
        [1,1,2,2,2,1,1],
        [1,2,2,4,2,2,1],
        [2,2,4,8,4,2,2],
        [2,4,8,16,8,4,2],
        [2,2,4,8,4,2,2],
        [1,2,2,4,2,2,1],
        [1,1,2,2,2,1,1]
    ]
    
    var Gaussian5X5Mask:[[Int]] = [
        [2,4,5,4,2],
        [4,9,12,9,4],
        [5,12,15,12,5],
        [4,9,12,9,4],
        [2,4,5,4,2]
    ]
    
    var LineDetector = LineDetectorMasks()
    var Kirsch = KirschMasks()
    var Sobel = SobelMasks()
}

let MASKS = FilterMasks()