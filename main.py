#
#  main.py
#  MineSeeder X
#
#  Created by Kyrox on 11-01-24.
#  Copyright __MyCompanyName__ 2011. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import MineSeeder_XAppDelegate
import MSXAppController

# pass control to AppKit
AppHelper.runEventLoop()
