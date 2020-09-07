import cv2
import numpy as np
import sys, importlib, os, glob, shutil

if __name__ == "__main__":
    try:
        spam_spec = importlib.util.find_spec("filetype")
        if spam_spec is None:
            raise(Exception)
        

    except:
        print('This program requires filetype package to run. Please install it through: \npip install filetype')
        exit()
        
import filetype



def compressFrames(video, ratio):
    
    try:
        os.mkdir('temp')
    except Exception as e:
        print('Error creating directory temp' + str(e), file=sys.stderr)
        return 

    cap = cv2.VideoCapture(video)

    if not cap.isOpened():
        print(f'Error Opening File {video}', file=sys.stderr)
        return

    if not cap.isOpened():
        print(f'Error Opening File {video}', file=sys.stderr)
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    

    try:
        i=0
        while True:
            # print('In while True!', file=sys.stderr)
          
            ret, frame = cap.read()
            # print('Frame read!', file=sys.stderr)
            if(not ret):
                print('Can\'t capture frames/Video End', file=sys.stderr)
                break
            i+=1
            height, width, layers =  frame.shape
            # print('Shape taken', file=sys.stderr)
            height=int(height*(ratio/100))
            width=int(width*(ratio/100))
            compressedframe = cv2.resize(frame, (width, height))
            # print('Resizing!', file=sys.stderr)
            # print(f'{width} {height} {fps}', file=sys.stderr)
            
            cv2.imwrite('./temp/temp_frame_'+ str(i) + '.jpg', compressedframe)

        return width, height, fps
    
    except Exception as e:
        print('In except' + str(e), file=sys.stderr)
        cap.release()
        cv2.destroyAllWindows()
        return

        cap.release()

def combineFramesAndSaveVideo(video, width, height, fps):

    images = [image for image in os.listdir('./temp')]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    name = ''
    if(os.path.splitext(video)[1] == '' ):
        name = 'compressed_' + video + '.mp4'
    else:
        name = 'compressed_' + video
    compressedVideo = cv2.VideoWriter(name, fourcc, fps, (width, height))
    images = glob.glob('./temp/*.jpg')

    images = [os.path.splitext(os.path.basename(images[i]))[0] for i in range(len(images))]
    images = sorted(images, key=lambda x: int(x[11:]))

    for filename in images:
        img = cv2.imread('./temp/' + filename + '.jpg')
        compressedVideo.write(img)

    compressedVideo.release()

    try:
        shutil.rmtree('./temp')
    
    except:
        print('Error removing temp files', file=sys.stderr)

    return name


if __name__ == "__main__":

    try:
    
        try:
            spam_spec = importlib.util.find_spec("filetype")
            if spam_spec is None:
                raise(Exception)
            
        except:
            print('This program requires filetype package to run. Please install it through: \npip install filetype')
            exit()

        import filetype

        if(len(sys.argv) < 3):
            print(f'Insufficient Arguments - {len(sys.argv)} given, 3 required.\nExample: python convert.py filename')
            exit()

        if(sys.argv[1] not in os.listdir()):
            print('Error: File does not exist')
            exit()


        if(type(int(sys.argv[2])) != type(1) or int(sys.argv[2]) not in range(1,100)):
            print('Error: Invalid ratio given')
            exit()
        video = sys.argv[1]
        ratio = int(sys.argv[2])

        if filetype.guess(video).mime.split('/')[0] != 'video':
            print('Given file is not a video file. Please give a video file.')
            exit()
        if('temp' in os.listdir()):
            print('Please rename the already present temp folder and then run again')
            exit()

        width, height, fps = compressFrames(video, ratio)

        combineFramesAndSaveVideo(video, width, height, fps)
    except:
        shutil.rmtree('./temp')