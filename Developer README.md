If you're building your own version of this, you'll probably want to get rid of my Sparkle auto-update code.

To set it up to use your own update settings, follow the configuration instructions on the [Sparkle website](https://github.com/andymatuschak/Sparkle/wiki). To remove it entirely, follow these steps:
1. Delete "dsa_pub.pem" and "Sparkle.framework", and make sure Sparkle.framework is removed from the list of "Linked Frameworks"
2. Remove the keys "SUPublicDSAKeyFile" and "SUFeedURL" from Info.plist
3. Remove the "Check for Updates..." button from the application menu in MainMenu.xib, then remove the entire preferences window, and delete the SUUpdater object
4. That's it! You should now have a completely auto update free system.