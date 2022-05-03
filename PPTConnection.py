import tempfile
import os
import win32com.client
import mss

powerpointInstance = win32com.client.Dispatch("PowerPoint.Application")
activePresentation = False
tempDir = False            
monitors = 0  
     
     

with mss.mss() as sct:

    #return true if succesful
    def selectPresentation( filename):
        global activePresentation
        global tempDir
        try:
            
        
            activePresentations = []
            for x in range(powerpointInstance.SlideShowWindows.Count):
                activePresentations.append(powerpointInstance.SlideShowWindows.Item(x+1).Presentation.Name)
                
            for x in range(powerpointInstance.Presentations.Count):
                if (filename.startswith("*") and (filename.endswith(" (Active)"))):
                    filename = filename[1:-9]
                    
                if filename == powerpointInstance.Presentations.Item(x+1).Name:
                    if filename in activePresentations: #If this slideshow is already running
                        powerpointInstance.Presentations.Item(x+1).SlideShowWindow.Activate()
                    else:
                        powerpointInstance.Presentations.Item(x+1).SlideShowSettings.Run()
                    activePresentation = powerpointInstance.Presentations.Item(x+1)
                    return True
        except Exception as e:
            print(e)
        return False

    def listPresentations():
        global activePresentation
        global tempDir
        presentationFilenames = []
        #try:
        
        activePresentations = []
        for x in range(powerpointInstance.SlideShowWindows.Count):
            activePresentations.append(powerpointInstance.SlideShowWindows.Item(x+1).Presentation.Name)
            
            
        for x in range(powerpointInstance.Presentations.Count):
            presentationName = powerpointInstance.Presentations.Item(x+1).Name
            if (presentationName in activePresentations):
                presentationName = "*" + presentationName + " (Active)"
            presentationFilenames.append(presentationName)
                # First presentation index is 1 not 0 because microsoft is  
        #except Exception as e:
        #    print(e)
        return presentationFilenames   

    def loadSlidePreviews():
        global activePresentation
        global tempDir
        if not activePresentation: return
        try:
            if not tempDir:
                tempDir = tempfile.TemporaryDirectory()
            for x in range(activePresentation.Slides.Count):
                activePresentation.Slides.Item(x+1).Export(tempDir.name + "\\" + str(activePresentation.Slides.Item(x+1).SlideID) + ".png", 'png');
            return tempDir.name
        except Exception as e:
            print(e)
            return False
        
    def loadSlidePreview(slideID):
        global activePresentation
        global tempDir
        if not activePresentation: return
        if not tempDir:
            tempDir = tempfile.TemporaryDirectory()
        slidePath = (str(activePresentation.Slides.FindBySlideID(slideID).SlideID) + ".png", tempDir.name)
        activePresentation.Slides.FindBySlideID(slideID).Export(slidePath[1] + "\\" +  slidePath[0], 'png');
        return slidePath

    def getActivePresentationName():
        global activePresentation
        global tempDir
        if not activePresentation: return False
        try:
            return activePresentation.name
        except Exception as e:
            print(e)
            return False
        
    def getSlideCount():
        global activePresentation
        global tempDir
        if not activePresentation: return 0
        try:
            return activePresentation.Slides.Count
        except Exception as e:
            print(e)
            return 0
        
    def getSlidesInfo():
        global activePresentation
        global tempDir
        if not activePresentation: return False
        curIndex = getCurrentSlideIndex();
        if curIndex == -1: return False
        slides = [curIndex]
        for slide in activePresentation.Slides:
            imgTuple = getSlideImage(slide.SlideID);
            slides.append({"slide-index" : slide.SlideIndex, "slide-id" :  slide.SlideID})
        return slides
        
    def getCurrentSlideIndex():
        global activePresentation
        global tempDir
        if not activePresentation: return -1
        try:
            return activePresentation.SlideShowWindow.View.Slide.SlideIndex
        except Exception as e:
            print(e)
            return -1
        
    def getSlideIDFromIndex(slideIndex):
        global activePresentation
        global tempDir
        if not activePresentation: return -1
        try:
            return activePresentation.Slides.Item(slideIndex).SlideID
        except Exception as e:
            print(e)
            return -1
        
    def getCurrentSlideID():
        global activePresentation
        global tempDir
        if not activePresentation: return -1
        try:
            return activePresentation.SlideShowWindow.View.Slide.SlideID
        except Exception as e:
            print(e)
            return -1

    def getSlideImage(slideID):
        global activePresentation
        global tempDir
        if not activePresentation: return False
        if tempDir and (os.path.exists(tempDir.name + "\\" + str(slideID) + ".png")):
            return (str(slideID) + ".png", tempDir.name)
        else:
            return loadSlidePreview(slideID)
            
            
    def getMonitorImage(monitor):
        if monitor >= len(sct.monitors):
            return False
        img_io = BytesIO()
        shot = sct.grab(sct.monitors[monitor])
        img_io.write(mss.tools.to_png(shot.rgb,shot.size))
        img_io.seek(0)
        return img_io
            
    def getMonitorCount():
        return len(sct.monitors) - 1
                    
        
        

    def goToX(slideIndex):
        global activePresentation
        global tempDir
        if not activePresentation: return False
        try:
            activePresentation.SlideShowWindow.View.GoToSlide(slideIndex)
            return True
        except Exception as e:
            print(e)
        return False

    def goToFirst():
        global activePresentation
        global tempDir
        if not activePresentation: return False
        try:
            activePresentation.SlideShowWindow.View.First()
            return True
        except Exception as e:
            print(e)
        return False

    def goToLast():
        global activePresentation
        global tempDir
        if not activePresentation: return False
        try:
            activePresentation.SlideShowWindow.View.Last()
            return True
        except Exception as e:
            print(e)
        return False

    def goToNext():
        global activePresentation
        global tempDir
        if not activePresentation: return False
        if not activePresentation.SlideShowWindow.View.Slide.SlideIndex < activePresentation.Slides.Count: return False
        print("activePresentation")
        print(activePresentation)
        print("activePresentation.SlideShowWindow.View")
        print(activePresentation.SlideShowWindow.View)
        #try:
        activePresentation.SlideShowWindow.View.Next()
        return True
        #except Exception as e:
        #    print(e)
        return False

    def goToPrevious():
        global activePresentation
        global tempDir
        if not activePresentation: return False
        try:
            activePresentation.SlideShowWindow.View.Previous()
            return True
        except Exception as e:
            print(e)
        return False

    
