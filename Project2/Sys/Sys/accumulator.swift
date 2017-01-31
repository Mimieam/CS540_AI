//
//  accumulator.swift
//  Sys
//
//  Created by Aman Miezan Echimane on 12/3/15.
//  Copyright © 2015 Miezel. All rights reserved.
//

import Foundation
import CoreGraphics

struct accumulatorStruct: CustomStringConvertible {
    var _acc = [String:[String:[point2D]]]()
    var distancePrecision = 3;
    var thetaPrecision = 1
    
    init (let distPrecision:Int=3, let thetaPrecision:Int = 1) {
        self.distancePrecision = distPrecision
        self.thetaPrecision = thetaPrecision
    }
    
    func formatDisIdx( let _idx1: CGFloat) -> String{
        return String(NSString(format: "%.\(self.distancePrecision)f ", _idx1))
    }
    func formatThetaIdx( let _idx1: CGFloat) -> String{
        return String(NSString(format: "%.\(self.thetaPrecision)f° ", _idx1))
    }
    
    subscript(_idx1: CGFloat) -> [String:[point2D]] {
        get {
            let idx1 = formatDisIdx(_idx1)
            if (_acc[idx1] != nil) {
                return _acc[idx1]!
            }
            return ["":[(0.0,0.0)]]
        }
        set {
            let idx1 = formatDisIdx(_idx1)
            //Note (newValue) here is derived from the getter and given the current getter definition
            // it will return the entire array and add the 'new item to it' that's why we  do = instead of += here.
            _acc[idx1] = newValue
        }
    }
    subscript(_idx1: CGFloat, _idx2: CGFloat) -> [point2D] {
        mutating get {
            let idx1 = formatDisIdx(_idx1)
            let idx2 = formatThetaIdx(_idx2)
            if(_acc[idx1] != nil) {
                idx2
                if (_acc[idx1]![idx2] != nil){
                    return _acc[idx1]![idx2]!
                }
                _acc[idx1]![idx2] = []
                return _acc[idx1]![idx2]!
            }
            _acc[idx1] = [idx2 : []]
            //_acc[idx1]![idx2] = [(0.0, 0.0)]
            return _acc[idx1]![idx2]!
        }
        set {
            let idx1 = formatDisIdx(_idx1)
            let idx2 = formatThetaIdx(_idx2)
            if (_acc[idx1] != nil){
                _acc[idx1]![idx2] = newValue
            }else {
                _acc[idx1] = [idx2 : []]
                _acc[idx1]![idx2] = newValue
            }
        }
    }
    var description: String {
        return "\(_acc)"
    }
    
}

func + ( var left: [point2D] , right: (CGFloat,CGFloat)) -> [point2D]  {
    left += [right]
    return left
}

func += (inout left: [point2D] , right: (CGFloat,CGFloat)) {
    left.append(right)
}

