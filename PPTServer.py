from flask import Flask, render_template, request, send_file
import time
import PPTConnection
import json
import jsonify




app = Flask(__name__)
    
@app.route("/get/slide/<int:slideId>")
def getImage(slideId):
    slideImg = PPTConnection.getSlideImage(slideId);
    print(slideId)
    print("slide Image Tuple:")
    print(slideImg)
    return send_file(slideImg[1] + "\\" + slideImg[0]);
    
@app.route("/get/monitor/<int:monitor>")
def getMonitor(monitor):
    print("Monitor grab: " + str(monitor))
    monitorImage = PPTConnection.getMonitorImage(monitor)
    return send_file(monitorImage, mimetype='image/png')






@app.route("/", methods= ['GET', 'POST'])            
def doPost():
    
    
    
    if request.method == 'GET':
        return render_template('pptcontrol.html');
        
        
    
    elif request.method == 'POST':
        payload = request.get_json()
        print(request.method)
        print("doPost:(payload)")
        print(payload)
        if (payload['action'] == "get-presentations"):
            return json.dumps(PPTConnection.listPresentations())
            
        if (payload['action'] == "get-slides"):
            return json.dumps(PPTConnection.getSlidesInfo())
        
        if (payload['action'] == "get-monitor-count"):
            return str(PPTConnection.getMonitorCount())
            
        if (payload['action'] == "get-monitor-image"):
            monitorImage = PPTConnection.getMonitorImage(payload['monitorNumber'])
            return send_file(monitorImage, 'monitor-1.png')
            
        if (payload['action'] == "get-slide-image"):
            slideImage = PPTConnection.getSlideImage(payload['slide-id'])
            return static_file(slideImage[0], slideImage[1], mimetype='image/png')
            
            
            
        if (payload['action'] == "select-presentation"):
            if PPTConnection.selectPresentation(payload['presentation']):
                return "1"
            else:
                return "0"
            
            
        if (payload['action'] == "navigate-next"):
            if PPTConnection.goToNext():
                return "1"
            else:
                return "0"
            
        if (payload['action'] == "navigate-previous"):
            if PPTConnection.goToPrevious():
                return "1"
            else:
                return "0"
            
        if (payload['action'] == "navigate-first"):
            if PPTConnection.goToFirst():
                return "1"
            else:
                return "0"
            
        if (payload['action'] == "navigate-last"):
            if PPTConnection.goToLast():
                return "1"
            else:
                return "0"
        
        
        
        
        
    return "ERROR, END OF doPost()"












app.run(host='0.0.0.0', port=7770, threaded=False) 
