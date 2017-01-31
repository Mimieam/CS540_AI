//
//  preprocessing.swift
//  Sys
//
//  Created by Aman Miezan Echimane on 12/3/15.
//  Copyright © 2015 Miezel. All rights reserved.
//

import UIKit
import Foundation
import CoreGraphics


typealias point2D = (y: CGFloat, x: CGFloat)

extension Int {
    var toRad : Float {
        return Float(self) * Float(M_PI) / 180.0
    }
}

infix operator ^^ { }
//func ^^ (radix: Int, power: Int) -> Int {return Int(pow(Double(radix), Double(power)))}
func ^^ (radix: Float, power: Float) -> Float {return Float(pow(Double(radix), Double(power)))}


func Median(let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, let h:Int) {
    print("Median...")
    var x,y,i,j,n,a,z:Int
    var ar:[Int] = [Int](count: 121, repeatedValue: 0)
    n = 7
    
    for( y = n/2; y <= h - n/2; y++) {
        for( x = n/2; x <= w - n/2; x++) {
            z = 0
            for (j = -n/2; j <= n/2; j++){
                for (i = -n/2; i <= n/2; i++){
                    ar[z] = Int(img[ x + i + (y + j) * w])
                    z++
                }
            }
            
            for(j = 0; j <= (n * (n - 1)); j++ ) {
                a = ar[j]
                i = j - 1
                while ( i >= 0 && ar[i] > a) {
                    ar[i + 1] = ar[i];
                    i = i - 1
                }
                ar[i + 1] = a
            }
            var tmp = ar[Int(n*n/2)]
            outputImg[x + y * w] = UInt8(tmp)
        }
    }

}

func Mean (let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, let h:Int) {
   print("\(w) * \(h)")
    var x,y,i,j,n,sum:Int

    n = 9
    for( y = n/2; y < h - n/2; y++) {
        for( x = n/2; x < w - n/2; x++) {
            sum = 0
            for (j = -n/2; j <= n/2; j++){
                for (i = -n/2; i <= n/2; i++){
                    sum = sum + Int(img[x + i + (y + j)*w])
                    
                }
            }
            outputImg[x + y * w] = UInt8(sum/n/n)
        }
    }
}


func GeometricMean (let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, let h:Int, let windowSize:Int = 5){
    print("GeometricMean...")
    var x,y,i,j,z:Int
//    var a:Int
    var ar:[Int] = [Int](count: 121, repeatedValue: 0)
    var product:Float
    var tar:[Float] = [Float](count: 121, repeatedValue: 0.0)
    let n = windowSize
    
    for( y = n/2; y <= h - n/2; y++) {
        for( x = n/2; x <= w - n/2; x++) {
            z = 0
            for (j = -n/2; j <= n/2; j++){
                for (i = -n/2; i <= n/2; i++){
                    ar[z] = Int(img[ x + i + (y + j) * w])
                    z++
                }
            }

            for(j = 0; j <= (n * (n - 1)); j++ ) {
                tar[j] =  Float(ar[j]) ^^ (1.0/Float(n*n))
            }
            product = 1.0
            for(j = 0; j <= (n * (n - 1)); j++ ) {
                product *= tar[j];
            }
            if (product > 255) {
                outputImg[x + y * w] = 255
            } else {
                outputImg[x + y * w] = UInt8(product)
            }
            
        }
    }
    

}

func anisotropicDiffusion (var img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>,  let w:Int, let h:Int, let Iteration:Int = 80) {
    // var res = img
    let K:Double = 0.0001
    var temp:Double = 0.0
    
    for _ in 0..<Iteration {
        for (var r = 1; r < h - 3; r++) {
            for (var c = 1; c < w - 3 ; c++) {
                
                temp  = K/(K + pow(Double(img[(r-1)*w + c]) - Double(img[r * w + c]), 2)) * (Double(img[(r-1) * w + c]) - Double(img[r * w + c]))
                temp += K/(K + pow(Double(img[(r+1)*w + c]) - Double(img[r * w + c]), 2)) * (Double(img[(r+1) * w + c]) - Double(img[r * w + c]))
                temp += K/(K + pow(Double(img[r * w + c-1]) - Double(img[r * w + c]), 2)) * (Double(img[r * w + c-1]) - Double(img[r * w + c]))
                temp += K/(K + pow(Double(img[r * w + c+1]) - Double(img[r * w + c]), 2)) * (Double(img[r * w + c+1]) - Double(img[r * w + c]))
                
                outputImg[r * w + c] =  UInt8((Double(img[r * w + c]) + 0.25 * Double(temp)))
                
            }
        }
        img = outputImg
    }
}


func Brightness (let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, h:Int, let brightness:Int) {
    // h = rows
    // w = cols
    var x, y, i:Int
    
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            i = Int(img[x + y * w]) + brightness
            if (i > 255){
                i = 255
            }
            if (i < 0){
                i = 0
            }
            outputImg[x + y * w] = UInt8(i)
        }
    }
}


func Contrast(let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, h:Int, let contrast:Int) {
    
    var x, y, i, sum, j:Int
    var avg:Float
    j = 0
    sum = 0
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            sum += Int(img[x + y * w])
            j++
        }
        
        avg = Float(sum)/Float(j)
        for (y = 0; y < h; y++) {
            for (x = 0; x < w; x++) {
                i = Int(Float(contrast) * (Float(img[x + y * w]) - avg) + avg)
                if (i > 255){
                    i = 255
                }
                if (i < 0){
                    i = 0
                }
                outputImg[x + y * w] = UInt8(i)
            }
        }
    }
}


func Dilation(let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, h:Int, let Mask:[[Int]] = [[1,1,1],[1,1,1],[1,1,1]] ) {
    var a:[[Int]] = Mask
    for( var m = 0; m < Mask.count; m++) {
        for( var n = 0; n < Mask[0].count; n++) {
            a[m][n] = 0
        }
    }
        
    var x,y,i,j,n,smax:Int
    n = Mask[0].count
       
//    var a:[[Int]] = [[0,0,0],[0,0,0],[0,0,0]]
    for( y = n/2; y < h - n/2; y++) {
        for( x = n/2; x < w - n/2; x++) {
            smax = 0
            for (j = -n/2; j <= n/2; j++){
                for (i = -n/2; i <= n/2; i++){
                    a[i + n/2][j + n/2] = Int(img[x + j + (y + j) * w]) + Mask[i + n/2][j + n/2]
                }
            }
            
            for (j = -n/2; j <= n/2; j++){
                for (i = -n/2; i <= n/2; i++){
                    if ( Int(a[i + n/2][j + n/2]) > smax){
                        smax = Int(a[i + n/2][j + n/2])
                    }
                
                }
            }
            if ( smax > 255){
                smax = 255
            }
            outputImg[x + y * w] = UInt8(smax)
        }
    }
}


func Erosion (let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, h:Int, let Mask:[[Int]] = [[1,1,1],[1,1,1],[1,1,1]] ){
    
    var a:[[Int]] = Mask
    for( var m = 0; m < Mask.count; m++) {
        for( var n = 0; n < Mask[0].count; n++) {
            a[m][n] = 0
        }
    }
        
     var x,y,i,j,n,smin:Int
        n = Mask[0].count
        for( y = n/2; y < h - n/2; y++) {
            for( x = n/2; x < w - n/2; x++) {
                smin = 255
                for (j = -n/2; j <= n/2; j++){
                    for (i = -n/2; i <= n/2; i++){
                        a[i + n/2][j + n/2] = Int(img[x + j + (y + j) * w]) + Mask[i + n/2][j + n/2]
                    }
                }
                
                for (j = -n/2; j <= n/2; j++){
                    for (i = -n/2; i <= n/2; i++){
                        if ( Int(a[i + n/2][j + n/2]) < smin){
                            smin = Int(a[i + n/2][j + n/2])
                        }
                        
                    }
                }
                if ( smin < 0){
                    smin = 0
                }
                outputImg[x + y * w] = UInt8(smin)
            }
        }
   
        
     
        
}


func lineDetector(let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, h:Int, let tresh:UInt8=100, let Mask:[[Int]]){
    var x,y,i,j,sum:Int;
    
    for (y = 1; y < h-1; y++) {
        for (x = 1; x < w-1; x++) {
            sum = 0
            
            for( i = -1; i <= 1; i++) {
                for( j = -1; j <= 1; j++) {
                    sum = sum + Int(img[(x + i) + (y + j) * w]) * Mask[i + 1][j + 1]
                }
            }
            
            if (sum > 255){
                sum = 255
            }
            if (sum < 0) {
                sum = 0
            }
            outputImg[x + y * w] = UInt8(sum)
            
        }
    }
    
}

func applyLowTreshold(let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, h:Int, let tresh:UInt8=100 , let bgrd:UInt8 = 0) {
    var x, y:Int
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            let idx = x + y * w
            if (img[idx] < tresh){
                outputImg[idx] = img[idx]
            } else {
                outputImg[idx] = bgrd
            }
        }
    }
}

func applyHighTreshold(let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, h:Int, let tresh:UInt8=100 , let bgrd:UInt8 = 0) {
    var x, y:Int
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            let idx = x + y * w
            if (img[idx] > tresh){
                outputImg[idx] = img[idx]
            } else {
                outputImg[idx] = bgrd
            }
        }
    }
}

func CloseGray(let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, h:Int, let Mask:[[Int]]) {
    var x, y:Int
    
    print("CloseGray...")
    Dilation(img, outputImg: &outputImg, w: w, h: h, Mask: Mask)
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            img[ x + y * w] = outputImg[x + y * w]
        }
    }
    Erosion(img, outputImg: &outputImg, w: w, h: h)
    
}


func Convolve(let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, h:Int, let Mask:[[Int]], let maskCoeff:Float=1) {
    var i,j,m,n,idx,jdx,im,val:Int
    var ms:Float
    im = 0
    for( i = 0; i < h; i++) {
        for( j = 0; j < w; j++) {
            val = 0
            for( m = 0; m < Mask.count; m++) {
                for( n = 0; n < Mask[0].count; n++) {
                    ms = Float(Mask[m][n]) * maskCoeff
                    idx = i - m
                    jdx = j - n
                    if (idx >= 0 && jdx >= 0) {
                        im = Int(img[idx * w + jdx])
                    }
                    val += Int(ms * Float(im))
                }
            }
            if(val > 255) {val = 255}
            if(val < 0) {val = 0}
            outputImg[j + i * w] = UInt8(val)
        }
    }
}



func Histogram(inout img:UnsafeMutablePointer<UInt8>, inout Hist:[Float], let w:Int, let h:Int) {

    var IHist = [Int](count: 256, repeatedValue: 0)
    
    var x,y,i,j,sum:Int
    for ( i = 0; i <= 255; i++) {
        IHist[i] = 0;
    }
    sum = 0
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            j = Int(img[ x + y * w])
            IHist[j] = IHist[j] + 1
            sum += 1
        }
    }
    
    for ( i = 0; i <= 255; i++) {
        Hist[i] = Float(IHist[i])/Float(sum)
    }
    
}


func HistogramEqualization(inout img:UnsafeMutablePointer<UInt8>, let w:Int, let h:Int) {
    var x,y,i,j:Int
    var sum:Float
    
    var Histeq = [Int](count: 257, repeatedValue: 0)
    var Hist = [Float](count: 257, repeatedValue: 0)
    Histogram(&img, Hist: &Hist, w: w, h: h)

    for ( i = 0; i <= 255; i++) {
        sum = 0
        for ( j = 0; j <= i; j++) {
            sum += Hist[j]
        }
        Histeq[i] = Int(Float(255 * sum) + 0.5)
    }
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            img[x + y * w] = UInt8(Histeq[Int(img[x + y * w])])
        }
    }
}


func HitMiss(var img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, let h:Int,
    let M1:[[Int]]=[[0,0,0],[0,1,1],[0,0,0]],
    let M2:[[Int]]=[[0,0,0],[1,0,0],[0,0,0]]) {
    var x, y:Int
    
    let imgc = UnsafeMutablePointer<UInt8>(malloc(w * h))
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            imgc[x + y * w] = 255 - img[x + y * w]
        }
    }
    Erosion(img, outputImg: &outputImg, w: w, h: h, Mask: M1)
    Erosion(imgc, outputImg: &img, w: w, h: h, Mask: M2)
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
           outputImg[x + y * w] = outputImg[x + y * w] & img[x + y * w]
        }
    }
}

func Outline (let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, h:Int, let Mask:[[Int]]) {
    
    var x,y,i,j:Int
    
    Erosion(img, outputImg: &outputImg, w: w, h: h, Mask: Mask)
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            let tmp = Int(img[x + y * w]) - Int(outputImg[x + y * w])
            outputImg[x + y * w] = tmp > 255 ? 255 : tmp < 0 ? 0 : UInt8(tmp)
        }
    }
    
}

func anisotropicDiffusion (var pixel2D:[[UInt8]], let w:Int, let h:Int, let Iteration:Int = 80) ->[[UInt8]]{
    var res = pixel2D
    let K:Double = 0.0001
    var temp:Double = 0.0
    
    for _ in 0..<Iteration {
        for (var r = 1; r < h - 3; r++) {
            for (var c = 1; c < w - 3 ; c++) {
                
                temp  = K/(K + pow(Double(pixel2D[r-1][c]) - Double(pixel2D[r][c]), 2)) * (Double(pixel2D[r-1][c]) - Double(pixel2D[r][c]))
                temp += K/(K + pow(Double(pixel2D[r+1][c]) - Double(pixel2D[r][c]), 2)) * (Double(pixel2D[r+1][c]) - Double(pixel2D[r][c]))
                temp += K/(K + pow(Double(pixel2D[r][c-1]) - Double(pixel2D[r][c]), 2)) * (Double(pixel2D[r][c-1]) - Double(pixel2D[r][c]))
                temp += K/(K + pow(Double(pixel2D[r][c+1]) - Double(pixel2D[r][c]), 2)) * (Double(pixel2D[r][c+1]) - Double(pixel2D[r][c]))
                
                res[r][c] =  UInt8((Double(pixel2D[r][c]) + 0.25 * Double(temp)))
                
            }
        }
        pixel2D = res
    }
    return res
}

func KirschEdges (inout img:UnsafeMutablePointer<UInt8>, let w:Int, let h:Int, let thresh:UInt8, let backgrdValue:UInt8 = 0){
    print("KirschEdges...")
    var Nimg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    var NWimg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    var Wimg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    var SWimg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    var Simg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    var SEimg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    var Eimg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    var NEimg = UnsafeMutablePointer<UInt8>(malloc(w * h))

    Convolve(img, outputImg: &Nimg, w: w, h: h, Mask: MASKS.Kirsch.N)
    Convolve(img, outputImg: &NWimg, w: w, h: h, Mask: MASKS.Kirsch.NW)
    Convolve(img, outputImg: &Wimg, w: w, h: h, Mask: MASKS.Kirsch.W)
    Convolve(img, outputImg: &SWimg, w: w, h: h, Mask: MASKS.Kirsch.SW)
    Convolve(img, outputImg: &Simg, w: w, h: h, Mask: MASKS.Kirsch.S)
    Convolve(img, outputImg: &SEimg, w: w, h: h, Mask: MASKS.Kirsch.SE)
    Convolve(img, outputImg: &Eimg, w: w, h: h, Mask: MASKS.Kirsch.E)
    Convolve(img, outputImg: &NEimg, w: w, h: h, Mask: MASKS.Kirsch.NE)
    
    /*scan for large values*/
    for (var y = 0; y < h; y++) {
        for (var x = 0; x < w; x++) {
            let idx = x + y * w
            img[idx] = max(Nimg[idx], NWimg[idx], Wimg[idx], SWimg[idx], Simg[idx], SEimg[idx], Eimg[idx], NEimg[idx])
            if (img[idx] < thresh) {
                img[idx] = backgrdValue
            }
        }
    }
}

func lineDetector4Direction (inout img:UnsafeMutablePointer<UInt8>, let w:Int, let h:Int, let thresh:UInt8 = 0, let backgrdValue:UInt8 = 0){
    print("lineDetector4Direction...")
    var Himg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    var Vimg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    var LDimg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    var RDimg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    
    lineDetector(img, outputImg: &Himg, w: w, h: h, Mask: MASKS.LineDetector.H)
    lineDetector(img, outputImg: &Vimg, w: w, h: h, Mask: MASKS.LineDetector.V)
    lineDetector(img, outputImg: &LDimg, w: w, h: h, Mask: MASKS.LineDetector.LD)
    lineDetector(img, outputImg: &RDimg, w: w, h: h, Mask: MASKS.LineDetector.RD)
    
    /*scan for large values*/
    for (var y = 0; y < h; y++) {
        for (var x = 0; x < w; x++) {
            let idx = x + y * w
            img[idx] = max(Himg[idx], Vimg[idx], LDimg[idx], RDimg[idx])
            if (img[idx] < thresh) {
                img[idx] = backgrdValue
            }
        }
    }

}


func SobelGradientImg (inout img:UnsafeMutablePointer<UInt8>, let w:Int, let h:Int, let thresh:UInt8, let backgrdValue:UInt8 = 0){
    var Gximg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    var Gyimg = UnsafeMutablePointer<UInt8>(malloc(w * h))
    
    Convolve(img, outputImg: &Gximg, w: w, h: h, Mask: MASKS.Sobel.Sx)
    Convolve(img, outputImg: &Gyimg, w: w, h: h, Mask: MASKS.Sobel.Sy)
    
    /*scan for large values*/
    for (var y = 0; y < h; y++) {
        for (var x = 0; x < w; x++) {
            let idx = x + y * w
            let gradient = abs(Int(Gximg[idx])) + abs(Int(Gyimg[idx]))
            img[idx] = UInt8(gradient > 255 ? 255 : gradient < 0 ? 0 : gradient)
            if (img[idx] < thresh) {
                img[idx] = backgrdValue
            }
        }
    }
}


func overlayLayers (let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, let h:Int, let thresh:UInt8, let backgrdValue:UInt8 = 0){
    /*scan for large values*/
    for (var y = 0; y < h; y++) {
        for (var x = 0; x < w; x++) {
            let idx = x + y * w
            outputImg[idx] = max(outputImg[idx], img[idx])
            if (outputImg[idx] < thresh) {
                outputImg[idx] = backgrdValue
            }
        }
    }
    
}



func binarize(var img:UnsafeMutablePointer<UInt8>, let w:Int, let h:Int, let low_tresh:UInt8 = 200, let Flag:Bool=true) -> UnsafeMutablePointer<UInt8>{
    for (var i = 0; i < h; i++)
    {
        for (var j = 0; j < w; j++)
        {
            if (Flag){
                img[i * w + j] = (img[i * w + j] < low_tresh) ? 0 : 1
            } else {
                img[i * w + j] = (img[i * w + j] == 1) ? 255 : 0
            }
            
        }
    }
    return img
}


func thinningIteration(var img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>,  let w:Int, let h:Int, let iter:Int)
{
    var marker = img
    
    for (var i = 1; i < w-1; i++)
    {
        for (var j = 1; j < h-1; j++)
        {
            let p2 = img[(i-1) * w + j];
            let p3 = img[(i-1) * w + j+1]
            let p4 = img[(i) * w + j+1]
            let p5 = img[(i+1) * w + j+1]
            let p6 = img[(i+1) * w + j]
            let p7 = img[(i+1) * w + j-1]
            let p8 = img[(i) * w + j-1]
            let p9 = img[(i-1) * w + j-1]
            
            var A  = ((p2 == 0 && p3 == 1) ? 0 : 1 ) + ((p3 == 0 && p4 == 1) ? 0 : 1 ) +
                ((p4 == 0 && p5 == 1) ? 0 : 1 ) + ((p5 == 0 && p6 == 1) ? 0 : 1)
            A += ((p6 == 0 && p7 == 1) ? 0 : 1) + ((p7 == 0 && p8 == 1) ? 0 : 1) +
                ((p8 == 0 && p9 == 1) ? 0 : 1) + ((p9 == 0 && p2 == 1) ? 0 : 1);
            let B  = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9;
            let m1 = iter == 0 ? (p2 * p4 * p6) : (p2 * p4 * p8);
            let m2 = iter == 0 ? (p4 * p6 * p8) : (p2 * p6 * p8);
            
            if (A == 1 && (B >= 2 && B <= 6) && m1 == 0 && m2 == 0){
                marker[i * w + j] = 1;
            }
        }
    }
    
    for (var i = 1; i < h-1; i++){
        for (var j = 1; j < w-1; j++){
            let tmp = Int(img[i * w + j]) - Int(marker[i * w + j])
            img[i * w + j] = marker[i * w + j] == 0 ? 1 : 0
        }
    }
}


func Skeleton(let img:UnsafeMutablePointer<UInt8>, inout outputImg:UnsafeMutablePointer<UInt8>, let w:Int, h:Int, let Mask:[[Int]]) {
    
    print("Skeleton...")
    var x,y,i,j:Int
    var pixel_on:Bool
    var pixel:Int
    var n:Int = Mask[0].count
    
    
    var Filter = UnsafeMutablePointer<UInt8>(malloc(w * h))
    var Filter1 = UnsafeMutablePointer<UInt8>(malloc(w * h))
    
//    True = 1
//    False = 0;
    pixel_on = true;
    for( y = n/2; y < h - n/2; y++) {
        for( x = n/2; x < w - n/2; x++) {
            outputImg[x + y * w] = 0
        }
    }
    
    while (pixel_on) {
        pixel_on = false
        Erosion(img, outputImg: &Filter, w: w, h: h, Mask: Mask)
        Dilation(img, outputImg: &Filter1, w: w, h: h, Mask: Mask)
        for( y = n/2; y < h - n/2; y++) {
            for( x = n/2; x < w - n/2; x++) {
                pixel =  Int(img[x + y * w]) - Int(Filter[x + y * w])
                if (pixel < 0) { pixel = 0 }
                outputImg[x + y * w] = outputImg[x + y * w] | UInt8(pixel)
            }
        }
    }
    
}


func HoughTransform(let img:UnsafeMutablePointer<UInt8>, let w:Int, let h:Int, var thresh:Int) -> [(rho: Int, theta: Int)]{
    var i,j,k,trho:Int

    var linesRT = [(rho: Int, theta: Int)]()
    let hough_h:Float = ((sqrt(2.0) * (Float)(h > w ? h : w)) / 2.0);
    let _accu_h = hough_h * 2.0; // -r -> +r
    let _accu_w = 180;
    
    var acc = [Int](count: _accu_w * Int(_accu_h), repeatedValue:0)
    var _acc = accumulatorStruct()
    print("Line Identification Started")
    /*check each pixel*/
    for (i = 0; i < w; i++) {
        for (j = 0; j < h; j++) {
            if( img[j + i * w] >= 253) {
                /* there is a pixel in the edge image we want*/
                
                for( k = 0 ; k < _accu_w ; k += 15 ){
                    var tmp = (Float(i) * cos(Float(k.toRad)) + Float(j) * sin(Float(k.toRad))) / hough_h
                    trho = Int(tmp + Float(h)/2)
                    acc[Int(Float(k) * Float(_accu_w) + Float(trho))]++
                    
                    _acc[CGFloat(trho), CGFloat(k)] += (CGFloat(i), CGFloat(j))
                    
                }
            }
        }
    }
    
    /*scan for large values*/
    for (i = 0; i < Int(_accu_h); i++) {
        for (j = 0; j < _accu_w; j++) {
            if ( acc[i * _accu_w + j] >= thresh ) {
                thresh = acc[i * _accu_w + j]
                linesRT.append((i, j))
            }
        }
    }
    /*scan for large values*/
    for (var y = 0; y < h; y++) {
        for (var x = 0; x < w; x++) {
            img[x + y * w] = 0
        }
    }
    for (_rho, items) in _acc._acc {
        for (_theta, pts) in items {
            if (pts.count >= thresh) {
                for pt in pts {
                    img[Int(pt.x + pt.y * CGFloat(w) )] = 255
                }
            }
        }
    }
    
    print("Found \(linesRT.count) lines")
    return linesRT
}

func GetLines(let RhoThetaLines:[(rho: Int, theta: Int)]) -> [(p1:point2D, p2:point2D)]{
    var xyLines = [(p1:point2D, p2:point2D)]()
    
    var a,b,x0,y0:CGFloat
    var p1,p2:point2D
    print(RhoThetaLines)
    for (rho, theta) in RhoThetaLines{
        a = cos(CGFloat(theta.toRad))
        b = sin(CGFloat(theta.toRad))
        x0 = a * CGFloat(rho)
        y0 = b * CGFloat(rho)
        
        p1.x = x0 + 1000 * (-b)
        p1.y = y0 + 1000 * (a)
        p2.x = x0 - 1000 * (-b)
        p2.y = y0 - 1000 * (a)
        
        xyLines.append((p1, p2))
    }
    
    print(xyLines)
    
    return xyLines
}




