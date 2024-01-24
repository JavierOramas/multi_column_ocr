import cv2
import sys

SCALE = 4
AREA_THRESHOLD = 427505.0 / 2

# utility function to display images
def show_scaled(name, img):
    try:
        h, w  = img.shape
    except ValueError:
        h, w, _  = img.shape
    cv2.imshow(name, cv2.resize(img, (w // SCALE, h // SCALE)))

def get_contours(image_path="image.jpg",img=None, save_partial_images=True):
    
    if img is None:        
        img = cv2.imread(image_path)
  
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # black and white, and inverted, because
    # white pixels are treated as objects in
    # contour detection
    thresholded = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                25,
                15
            )

    # I use a kernel that is wide enough to connect characters
    # but not text blocks, and tall enough to connect lines.
    # Modify this to get the desired results if needed
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 33))
    closing = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    images = []
    
    i = 0
    for cnt in contours:
        # Get bounding box coordinates for the contour
        x, y, w, h = cv2.boundingRect(cnt)
        i += 1
        # Crop the original image
        cropped = img[y:y+h, x:x+w]

        if save_partial_images:
            # Save the cropped image
            cv2.imwrite(f'cropped_image_{i}.png', cropped)
        
        images.append(cropped)
    if save_partial_images:
        for contour in contours:
            convex_contour = cv2.convexHull(contour)
            area = cv2.contourArea(convex_contour)
            # if area > AREA_THRESHOLD:
            cv2.drawContours(img, [convex_contour], -1, (255,0,0), 3)        
    
        show_scaled("contours", img)
        cv2.imwrite("./contours.png", img)
    
    return images
if __name__ == '__main__':
    get_contours(sys.argv[1])