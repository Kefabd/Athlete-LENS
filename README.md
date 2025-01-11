# Athlete-LENS
 
This project uses YOLOv8 for detecting bib numbers in marathon images and OCR for extracting the numbers. Photographers can upload marathon pictures, and participants can search for their photos by entering their bib numbers.

## Key Technologies Used:

### YOLOv8 (You Only Look Once - Version 8):
YOLOv8 is a powerful, real-time object detection model that is particularly well-suited for identifying objects in images and videos. In this project, YOLOv8 was trained to detect bib numbers in marathon pictures. Its ability to perform high-speed and high-accuracy detection enables swift processing of large volumes of race photos.

### Optical Character Recognition (OCR):
After detecting the bib regions in the images, an OCR model was applied to extract the text (bib number) from the cropped areas. This step ensures that the bib number is read accurately, even in challenging conditions such as low resolution, blurry images, or different lighting scenarios.
