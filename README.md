# Athlete-LENS
 
This project uses YOLOv8 for detecting bib numbers in marathon images and OCR for extracting the numbers. Photographers can upload marathon pictures, and participants can search for their photos by entering their bib numbers.

## Key Technologies Used:

### YOLOv8 (You Only Look Once - Version 8):
YOLOv8 is a powerful, real-time object detection model that is particularly well-suited for identifying objects in images and videos. In this project, YOLOv8 was trained to detect bib numbers in marathon pictures. Its ability to perform high-speed and high-accuracy detection enables swift processing of large volumes of race photos. (see the training file "training.ipynb")

### Optical Character Recognition (OCR):
After detecting the bib regions in the images, an OCR model was applied to extract the text (bib number) from the cropped areas. This step ensures that the bib number is read accurately, even in challenging conditions such as low resolution, blurry images, or different lighting scenarios.

### Roboflow:
Roboflow was used to annotate and prepare the training data for YOLOv8. It provides a user-friendly interface for annotating images, enabling efficient labeling of bib numbers within marathon pictures. The annotated dataset was then used to train the YOLOv8 model, improving detection accuracy for bib numbers across various images.

##Functionality:

###Photographer Uploads:
Photographers can upload marathon pictures to the platform, where the system automatically processes the images to detect and extract the bib numbers using YOLOv8 and OCR.

###User Search:
Participants or users can search for their own pictures by entering their bib number. The system will then retrieve the relevant images by matching the detected bib numbers with the search query.

##Project Workflow:

###Upload Pictures:
Uploaded images are preprocessed for optimal detection, including resizing, contrast enhancement, and noise reduction.

###Bib Detection with YOLOv8:
YOLOv8 detects the bib regions and marks them with bounding boxes, preparing the image for text extraction.

###OCR for Text Extraction:
The OCR technology extracts the bib numbers from the detected regions, converting the image data into readable text.

###User Interaction:
Users can enter their bib numbers to find their images. The system matches the entered bib number with the detected ones, enabling a smooth search process.
