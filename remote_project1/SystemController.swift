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
    
    var _view:UIImageView
    
    init(var view:UIImageView, var img:UIImage){
        
        _view = view
        _view.image = img
    }
}