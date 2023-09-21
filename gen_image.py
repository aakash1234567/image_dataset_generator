import cv2
import numpy as np
import os,time
import PySimpleGUI as sg
import threading
def apply_brightness_contrast(input_img, brightness = 255, contrast = 127):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    if contrast != 0:
        f = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    return buf

def long_operation_thread(n,values,seconds, window):
    
    print('Starting thread - will sleep for {} seconds'.format(seconds))
                    # sleep for a while
    img_no=file+1
    while img_no < int(n)+file+1:
        if values["jpg"]:
                if values["mod2"]:
                    cv2.imwrite("./images/{}/{}.jpg".format(values["-GNAME-"],img_no),frame[y1:y2,x1:x2])
                else:
                    cv2.imwrite("./images/{}/{}.jpg".format(values["-GNAME-"],img_no),frame)
        else:
            if values["mod2"]:
                cv2.imwrite("./images/{}/{}.png".format(values["-GNAME-"],img_no),frame[y1:y2,x1:x2])
            else:
                cv2.imwrite("./images/{}/{}.png".format(values["-GNAME-"],img_no),frame)
        img_no+=1
#         print(img_no)
        window.write_event_value('-THREAD-', img_no)  # put a message into queue for GUI
        if values["mod2"]:
            pre = cv2.resize(frame[y1:y2,x1:x2], (200, 200),
                   interpolation = cv2.INTER_AREA)
        else:
            pre = cv2.resize(frame, (200, 200),
                   interpolation = cv2.INTER_AREA)
        pre = cv2.imencode('.png', pre)[1].tobytes()
        window['preview'].update(data=pre)
        time.sleep(seconds)  
        
    
file_list_column = [
    [
        sg.Text("Enter gesture name:"),
        sg.In(size=(25, 1), key="-GNAME-"),        
    ],
    [
        sg.Text("Enter number of images you want to take:"),
        sg.In(size=(25, 1),key="-N-"),        
    ],
    [
        sg.Text("Enter time interval after which the image should be taken:"),
        sg.In(size=(25, 1),key="-TIME-"),
        
    ],
    [sg.Button('Submit'), sg.Button('Clear')],
    [sg.Text('_'*1200)] ,
        
]
col = [
    [sg.Image(filename='', key='image')],
        [sg.Button('Capture')],
]
options = [
    [
        sg.Column([[sg.Radio("PNG",1,default = True,size = (25, 1),key='png')]]),
        sg.Column([[sg.Radio("JPG",1,default = False,size = (25, 1),key='jpg')]])      
    ],
    [
        sg.Checkbox("Grayscale",default = False,size = (25, 1),key="gray")
    ],
    [
        sg.Checkbox("flip",default = False,size = (25, 1),key="flip")
    ],
    [
        sg.Column([[sg.Radio("Autonomous",2,default = True,size = (25, 1),key='auto')]]),
        sg.Column([[sg.Radio("Manual",2,default = False,size = (25, 1),key='man')]])      
    ],
    [
        sg.Column([[sg.Radio("Mode 1",3,default = True,size = (25, 1),key='mod1')]]),
        sg.Column([[sg.Radio("Mode 2",3,default = False,size = (25, 1),key='mod2')]])      
    ],
    [   sg.Text("Brightness"),
        sg.Slider(range = (-255, 255),
    default_value = 50,
    tick_interval = 40,
    orientation = "h",
    enable_events = True,
    size = (50, 15),
    key="bright")
    ],
    [  sg.Text("Contrast"),
       sg.Slider(range = (-127, 127),
    default_value = 50,
    tick_interval = 30,
    orientation = "h",
    enable_events = True,
    size = (50, 15),key="contrast") 
    ],
    [   sg.Column([[sg.Text("count",key="cnt", auto_size_text=True,pad=(20,20))]]),
        sg.Column([[sg.Image(filename='',size=(200,200),background_color = "white", key='preview',pad=(20,20))]]),
     sg.Column([
         [sg.Radio("TL",4,default = True,size = (25, 1),key='TL')],
         [sg.Radio("TR",4,default = False,size = (25, 1),key='TR')],
         [sg.Radio("C",4,default = False,size = (25, 1),key='C')],
         [sg.Radio("TC",4,default = False,size = (25, 1),key='TC')],
         [sg.Radio("BC",4,default = False,size = (25, 1),key='BC')],
         [sg.Radio("BR",4,default = False,size = (25, 1),key='BR')],
         [sg.Radio("BL",4,default = False,size = (25, 1),key='BL')],
     ])
    ],
    
]
def coor(values):
    
    if values["TL"]:
        x1 = 5
        y1 = 5
        x2 = 220
        y2 = 220
    elif values["TR"]:
        x1 = frame.shape[1]-220
        y1 = 5
        x2 = frame.shape[1]
        y2 = 220
    elif values["C"]:
        x1 = (frame.shape[1]//2)-115
        y1 = (frame.shape[0]//2)-115
        x2 = (frame.shape[1]//2)+115
        y2 = (frame.shape[0]//2)+115
    elif values["TC"]:
        x1 = (frame.shape[1]//2)-115
        y1 = 5
        x2 = (frame.shape[1]//2)+115
        y2 = 220
    elif values["BC"]:
        x1 = (frame.shape[1]//2)-115
        y1 = frame.shape[0]-220
        x2 = (frame.shape[1]//2)+115
        y2 = frame.shape[0]
    elif values["BR"]:
        x1 = frame.shape[1]-220
        y1 = frame.shape[0]-220
        x2 = frame.shape[1]
        y2 = frame.shape[0]
    elif values["BL"]:
        x1 = 5
        y1 = frame.shape[0]-220
        x2 = 220
        y2 = frame.shape[0]
    return x1,y1,x2,y2
layout = [
    [
        file_list_column,
        sg.Column(col),
        sg.VSeperator(),
        sg.Column(options),
    ]
]
sg.theme('Black')
window = sg.Window("GetImage", layout,size=(1200, 700),return_keyboard_events=True, location=(0, 0), keep_on_top=False)
# window.Maximize()

if not os.path.exists("./images"):
    os.mkdir("./images")
cap = cv2.VideoCapture(0)
start=0
while True:
    event, values = window.read(timeout=0, timeout_key='timeout')
    if event == "Exit" or event == sg.WIN_CLOSED:
        cv2.destroyAllWindows()
        cap.release() 
        break
    ret, frame = cap.read()
    frame = apply_brightness_contrast(frame,values["bright"],values["contrast"])
    if values["gray"]:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if values["flip"]:
        frame = cv2.flip(frame, 1)
    if values["mod1"]:
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window['image'].update(data=imgbytes)
    
    elif values["mod2"]:
        x1,y1,x2,y2 = coor(values)
        start_point = (x1, y1)
        end_point = (x2, y2)
        color = (255, 0, 0)
        thickness = 2
        im = cv2.rectangle(frame, start_point, end_point, color, thickness)
        imgbytes = cv2.imencode('.png', im)[1].tobytes()
        window['image'].update(data=imgbytes)
    if values["man"]:
        if event == 19:
            if values["jpg"]:
                if values["mod2"]:
                    cv2.imwrite("./images/{}/{}.jpg".format(values["-GNAME-"],img_no),frame[y1:y2,x1:x2])
                else:
                    cv2.imwrite("./images/{}/{}.jpg".format(values["-GNAME-"],img_no),frame)
            else:
                if values["mod2"]:
                    cv2.imwrite("./images/{}/{}.png".format(values["-GNAME-"],img_no),frame[y1:y2,x1:x2])
                else:
                    cv2.imwrite("./images/{}/{}.png".format(values["-GNAME-"],img_no),frame)
            img_no+=1
            window['cnt'].update(str(img_no))
    if start==1 and values["auto"]:
        seconds = float(values['-TIME-'])
        print('Thread ALIVE! Long work....sending value of {} seconds'.format(seconds))
        threading.Thread(target=long_operation_thread, args=(n,values,seconds, window,), daemon=True).start()
        start=0
    
    if event == '-THREAD-':
        print('Got a message back from the thread: ', values[event])
        window['cnt'].update(str(values[event]))
    if event == "Clear":
        window['-GNAME-'].update('')
        window['-N-'].update('')
        window['-TIME-'].update('')
    if event == "Submit":
        n = values["-N-"]
        ti = values["-TIME-"]
        file=0
        if not os.path.exists("./images/{}".format(values["-GNAME-"])):
            os.mkdir("./images/{}".format(values["-GNAME-"]))
        else:
            try:
                arr = os.listdir("./images/{}/".format(values["-GNAME-"]))
                file = sorted([int(f.split(".")[0]) for f in arr])[-1]
                print(file)
            except:
                file = 0
    if event == "Capture":
        start=1
        img_no = file+1
        frame_no = 0
#     if len(event) == 1:
#         print(event, ord(event))
window.close()
