
//
//  imageManager.swift
//  VysSys
//
//  Created by Aman Miezan Echimane on 12/2/15.
//  Copyright © 2015 Miezel. All rights reserved.
//

import Foundation
import UIKit
import CoreGraphics

func CreateBitmapContext (inImage:CGImageRef, dividingFactor:Int = 1) -> (cgctx:CGContextRef, pixelPtr:UnsafeMutablePointer<UInt8>, ctxWidth: Int, ctxHeight: Int) {
    
    
    var context: CGContextRef!;
    let bitmapData: UnsafeMutablePointer<UInt8>;
    var bitmapByteCount: Int;
    var bitmapBytesPerRow: Int;
    
    // Get image width, height. We'll use the entire image.
    let pixelsWide = CGImageGetWidth(inImage)/dividingFactor;
    let pixelsHigh = CGImageGetHeight(inImage)/dividingFactor;
    
    // Declare the number of bytes per row. Each pixel in the bitmap in this
    // example is represented by 4 bytes; 8 bits each of red, green, blue, and
    // alpha.
    bitmapBytesPerRow   = (pixelsWide * 4);
    bitmapByteCount     = (bitmapBytesPerRow * pixelsHigh);
    
    // Allocate memory for image data. This is the destination in memory
    // where any drawing to the bitmap context will be rendered.
    bitmapData = UnsafeMutablePointer<UInt8>(malloc(bitmapByteCount))
    
    context = CGBitmapContextCreate (bitmapData,
        pixelsWide,
        pixelsHigh,
        CGImageGetBitsPerComponent(inImage),      // bits per component
        CGImageGetBytesPerRow(inImage),
        CGColorSpaceCreateWithName(kCGColorSpaceGenericGray),
        CGImageGetBitmapInfo(inImage).rawValue
    );
    
//    let scale: CGFloat = 0.0 // Automatically use scale factor of main screen

    let rect:CGRect = CGRectMake(0, 0, CGFloat(pixelsWide) , CGFloat(pixelsHigh))
//    UIGraphicsBeginImageContextWithOptions(rect.size, false, scale)
    

    CGContextDrawImage(context, rect, inImage);
//    UIImage(CGImage: inImage).drawInRect(rect)
    
//    UIGraphicsEndImageContext()

    let data = CGBitmapContextGetData (context)
    let pixelPtr = UnsafeMutablePointer<UInt8>(data)
    
    //    let imageRef = CGBitmapContextCreateImage(context)
    //    UIImage(CGImage: imageRef!)
    
    return (context, pixelPtr, pixelsWide, pixelsHigh);
}




func overlayLinesOnImage(let img:UIImage, let lines:[(p1:point2D, p2:point2D )]) -> UIImage {
    //    UIGraphicsBeginImageContext(CGSizeMake(img.size.width, img.size.height))
    UIGraphicsBeginImageContextWithOptions(CGSizeMake(img.size.width, img.size.height), true, UIScreen.mainScreen().scale)
    let context = UIGraphicsGetCurrentContext()
    
    
    let rect:CGRect = CGRectMake(0, 0, CGFloat(img.size.width) , CGFloat(img.size.height))
    //    CGContextDrawImage(context, rect, img.CGImage);  // draw IT UPSIDE DOWN !! WTH !!??
    img.drawInRect(rect)  // USE THIS INSTEAD !
    
    //            var context = self.vsimg.original.cgctx
    CGContextSetStrokeColorWithColor(context, UIColor.redColor().CGColor)
    
    for line in lines{
        CGContextMoveToPoint(context, line.0.x, line.0.y)
        CGContextAddLineToPoint(context, line.1.x, line.1.y)
        CGContextStrokePath(context)
    }
    
    let newImage = UIGraphicsGetImageFromCurrentImageContext()
    UIGraphicsEndImageContext()
    
    return newImage
}



class VSPhoto {
    
    var CGRef:CGImageRef!
    var pixelPtr:UnsafeMutablePointer<UInt8>;
    var width:Int = 0;
    var height:Int = 0;
    
    var cgctx: CGContextRef
    var count:Int = 0 ;
    
    init(img:UIImage! , scaleDownBy:Int = 1){
        CGRef = img.CGImage
        
        (cgctx, pixelPtr, width, height) = CreateBitmapContext(img.CGImage!, dividingFactor: scaleDownBy)
        print("\(width) * \(height)")
        count = width * height
    }
    
    func display() -> UIImage{
        let imageRef = CGBitmapContextCreateImage(cgctx)
        return UIImage(CGImage: imageRef!)
    }
    
}

// Visual Sytem Image class


class VSImage {
    
    var UIimg: UIImage!
    var scaleDownBy:Int!
    
    var original: VSPhoto!
    var modified: VSPhoto!
    var buffer: VSPhoto!
    
    init(img:UIImage, scaleDownBy:Int = 1){
        original = VSPhoto(img: img, scaleDownBy: 1)
        buffer = VSPhoto(img: img, scaleDownBy: scaleDownBy)
        modified = VSPhoto(img: UIImage(CGImage: CGBitmapContextCreateImage(buffer.cgctx)!), scaleDownBy: 1)
    }
    
    func reset(){
        modified = VSPhoto(img: UIimg, scaleDownBy: scaleDownBy)
    }
    
    func resetWithNewImg (img:UIImage, scaleDownBy:Int = 1) -> UIImage{
        original = VSPhoto(img: img, scaleDownBy: 1)
        buffer = VSPhoto(img: img, scaleDownBy: scaleDownBy)
        modified = VSPhoto(img: UIImage(CGImage: CGBitmapContextCreateImage(buffer.cgctx)!), scaleDownBy: 1)
        return img
    }
    
    func displayOrignal() -> UIImage{ return UIImage(CGImage: original.CGRef) }
    
    func displayProcessed() -> UIImage{
        let imageRef = CGBitmapContextCreateImage(modified.cgctx)
        return UIImage(CGImage: imageRef!)
    }
    
}




