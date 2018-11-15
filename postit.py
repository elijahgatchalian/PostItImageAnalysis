import numpy as np
import cv2
import skimage
from skimage import color

#Python3

#Global Variables - Pink HSV Values
low = np.array([.73,.52,.78])
high = np.array([.98,.7,.98])

def analyze_(image):
    #This conversion is very costly. The reason this was chosen was I found hsv
    #was more accurate when finding the post it color when compared to rgb.
    hsv = color.rgb2hsv(image)
    
    #Creating color conditions from original image
    first_cond = np.logical_and(hsv[:,:,0] > low[0], hsv[:,:,1] > low[1], hsv[:,:,2] > low[2])
    second_cond = np.logical_and(first_cond, hsv[:,:,0] < high[0])
    third_cond = np.logical_and(second_cond, hsv[:,:,1] < high[1])
    fourth_cond = np.logical_and(third_cond, hsv[:,:,2] < high[2])
    
    #Mapping True values to coordinates from fourth_cond
    #True values indicate pixel post it locations
    final_cond = np.where(fourth_cond)
    
    #To have black background and show only postit, pass back fourth_cond instead of final_cond
    #Then change main to instead execute image[pi_mask == False] = (0,0,0)
    return final_cond

cap = cv2.VideoCapture(0)
cv2.namedWindow('finding post-it')
    
while(True):
    ret, image = cap.read()
        
    postit_mask = analyze_(image)
    image[postit_mask] = (0,0,0)
        
    cv2.imshow('finding post-it', image)
    #Exit loop by pushing e
    if cv2.waitKey(5) & 0xFF == ord('e'):
        break
    
cap.release()
cv2.destroyAllWindows()
