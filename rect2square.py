import sys
import cv2 as cv

file_name = sys.argv[1]
extension = sys.argv[2]

print('Working on it...')

img = cv.imread(f'{file_name}.{extension}')

# Original width and height
width, height = img.shape[1],img.shape[0]

radius = (height**2+width**2)**0.5

# Width and height to resize image
new_width, new_height = (round(radius),round((height/width)*radius)) if height>=width else (round((width/height)*radius),round(radius))

# Resizing image
resized = cv.resize(img, (new_width,new_height))

# Applying Gaussian blur to image
percentage = 16
blur_width, blur_height = int(new_width*percentage/100), int(new_height*percentage/100)
blur_width, blur_height = blur_width+(1-blur_width%2), blur_height+(1-blur_height%2)
gaussian = cv.GaussianBlur(resized, (blur_width,blur_height),0)


# Cropping image
cropped_image = gaussian[round((new_height-new_width)/2):round(new_height-(new_height-new_width)/2),:] if new_height>=new_width else gaussian[:,round((new_width-new_height)/2):round(new_width-(new_width-new_height)/2)]

new_width, new_height = cropped_image.shape[0],cropped_image.shape[1]

# compute xoff and yoff for placement of upper left corner of resized image   
yoff = round((new_height-height)/2)
xoff = round((new_width-width)/2)

# use numpy indexing to place the resized image in the center of background image
result = cropped_image.copy()
result[yoff:yoff+height, xoff:xoff+width] = img
result = cv.resize(result, (max(width,height),max(width,height)))

cv.imwrite(f'{file_name}_squared.{extension}',result)

print(f"{file_name}.{extension}'s squared image is saved as {file_name}_squared.{extension}.")