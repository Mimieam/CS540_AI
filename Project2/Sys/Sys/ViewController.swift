//
//  ViewController.swift
//  VysSys
//
//  Created by Aman Miezan Echimane on 12/2/15.
//  Copyright © 2015 Miezel. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UIPickerViewDataSource, UIPickerViewDelegate {

    @IBOutlet var imageView1: UIImageView!
    @IBOutlet weak var pickerView: UIPickerView!
    @IBOutlet weak var activityIndicatorView: UIActivityIndicatorView!
    
    private var pickerDataSource = ["im1-c.bmp","im2-c.bmp","im3-c.bmp","im4-c.bmp","im5-c.bmp","im6-c.bmp","im7-c.bmp"]
    private var system:VySys
    
    required init?(coder aDecoder: NSCoder){
//        Int(arc4random_uniform(7))
    let image = UIImage(named: pickerDataSource[1])
        system = VySys(img: image!)
        super.init(coder: aDecoder)
    }
    
    override func viewDidLoad() {
        
        super.viewDidLoad()
        self.pickerView.dataSource = self
        self.pickerView.delegate = self
        self.activityIndicatorView.startAnimating()
        
        system.setView(imageView1)
        system.addViewController(self)

        startProcessingThread()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    /*===============IBActions===========*/

    
    /*===============END IBActions===========*/

    func numberOfComponentsInPickerView(pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return pickerDataSource.count
    }
    
    func pickerView(pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return pickerDataSource[row]
    }
    
    func pickerView(pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        print("Selected Img: \(pickerDataSource[row])")
        let newImg = UIImage(named: pickerDataSource[row])!
        
        system.original = system.Manager.resetWithNewImg(newImg)
        imageView1.image = newImg
        startProcessingThread()
        
    }
    
    
    func startProcessingThread(){
        imageView1.image = system.original
        activityIndicatorView.startAnimating()
        dispatch_async(dispatch_get_global_queue(Int(QOS_CLASS_USER_INITIATED.rawValue), 0)) {
            self.system.start()
            dispatch_async(dispatch_get_main_queue()){
                [weak self] in
                if let weakSelf = self {
                    print("Thread returning")
                    weakSelf.imageView1.image = overlayLinesOnImage(weakSelf.system.Manager.modified.display(), lines: weakSelf.system.lines!)
                    weakSelf.activityIndicatorView.stopAnimating()
                }
            }
        }
    }
    
}

