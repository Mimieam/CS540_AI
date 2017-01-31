//
//  ViewController.swift
//  VysSys
//
//  Created by Aman Miezan Echimane on 12/2/15.
//  Copyright © 2015 Miezel. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet var imageView1: UIImageView!
    
    private var system:VySys
    
    required init?(coder aDecoder: NSCoder){
//        let data2 = NSData(contentsOfFile: "/im1-c.bmp")
        
        if let image = UIImage(named: "im1-c.bmp") {
            system = VySys(view: imageView1, img: image)
        }
        system  = VySys()

        super.init(coder: aDecoder)
    }
    
    override func viewDidLoad() {
        
        super.viewDidLoad()
        
//        system = VySys(view: imageView1)
//
//        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

