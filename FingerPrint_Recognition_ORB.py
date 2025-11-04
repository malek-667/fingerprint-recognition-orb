import cv2
import os
import numpy as np
from tkinter import filedialog
from tkinter import Tk



DATABASE_FOLDER = 'C:\\Users\\malek\\Desktop\\img analysis worksapce\\fingerprint recongition ORB\\fingerprint_database'



def load_fingerprint_database(folder_path):
    database = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(folder_path, filename)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                name = os.path.splitext(filename)[0]
                database[name] = img
    return database

def apply_gabor_filter(img):
    # Define a bank of Gabor filters with multiple orientations
    filters = []
    ksize = 21
    sigma = 5
    lambd = 10
    gamma = 0.5

    for theta in np.arange(0, np.pi, np.pi / 8):  # 8 orientations
        kern = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, 0, ktype=cv2.CV_32F)
        filters.append(kern)

    # Apply each filter and take the maximum response
    accum = np.zeros_like(img, dtype=np.float32)
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_32F, kern)
        accum = np.maximum(accum, fimg)

    # Normalize to 8-bit
    accum = cv2.normalize(accum, None, 0, 255, cv2.NORM_MINMAX)
    return accum.astype(np.uint8)

def preprocess_fingerprint(img):
    # Histogram Equalization
    equalized = cv2.equalizeHist(img)

    # Apply Gabor Filter Bank
    filtered = apply_gabor_filter(equalized)

    return filtered



def orb_match_score(img1, img2):
    orb = cv2.ORB_create()

    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None or des2 is None:
        return 0, None, None, []

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    num_good = min(len(matches), 40)
    good_matches = matches[:num_good]
    match_score = sum([m.distance for m in good_matches]) / num_good if num_good > 0 else float('inf')

    normalized_score = 1 - (match_score / 100)
    return normalized_score, kp1, kp2, good_matches


def match_fingerprint(input_image, database):
    preprocessed_input = preprocess_fingerprint(input_image)

    best_score = -1
    best_match_name = None
    best_match_img = None
    best_kp1 = best_kp2 = best_matches = None

    for name, db_image in database.items():
        preprocessed_db = preprocess_fingerprint(db_image)

        score, kp1, kp2, matches = orb_match_score(preprocessed_input, preprocessed_db)
        print(f" {name}: ORB Match Score = {score:.2f}")

        if score > best_score:
            best_score = score
            best_match_name = name
            best_match_img = db_image
            best_kp1, best_kp2, best_matches = kp1, kp2, matches

    return best_match_name, best_match_img, best_score, best_kp1, best_kp2, best_matches




def show_result(input_img, matched_img, matched_name, score, kp1, kp2, matches, input_filename):
    def resize_with_aspect(img):
        width = int(img.shape[1] * 70 / 100)
        height = int(img.shape[0] * 70 / 100)
        return cv2.resize(img, (width, height))

    input_img_resized = resize_with_aspect(input_img)
    matched_img_resized = resize_with_aspect(matched_img)

    # Annotated copies
   # input_annotated = input_img_resized.copy()
    #matched_annotated = matched_img_resized.copy()
    #converting to BGR for OpenCV compatibility
    input_annotated = cv2.cvtColor(input_img_resized, cv2.COLOR_GRAY2BGR)
    matched_annotated = cv2.cvtColor(matched_img_resized, cv2.COLOR_GRAY2BGR)


    # Adjust keypoint coordinates according to resize
    scale_x = input_img_resized.shape[1] / input_img.shape[1]
    scale_y = input_img_resized.shape[0] / input_img.shape[0]

    for m in matches:
        pt1 = kp1[m.queryIdx].pt
        pt2 = kp2[m.trainIdx].pt
        pt1_scaled = (int(pt1[0] * scale_x), int(pt1[1] * scale_y))
        pt2_scaled = (int(pt2[0] * scale_x), int(pt2[1] * scale_y))
        cv2.circle(input_annotated, pt1_scaled, 8, (0, 0, 255), 2)  # 🔴 Red circle
        cv2.circle(matched_annotated, pt2_scaled, 8, (0, 0, 255), 2)

    
    stacked = np.hstack((input_annotated, matched_annotated))

    if len(stacked.shape) == 2:
        stacked = cv2.cvtColor(stacked, cv2.COLOR_GRAY2BGR)

    
    top_padding = 80
    bottom_padding = 50
    canvas_height = stacked.shape[0] + top_padding + bottom_padding
    canvas_width = stacked.shape[1]
    canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255

    # Place stacked images
    canvas[top_padding:top_padding + stacked.shape[0], :] = stacked

   
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 0.9
    thickness = 1
    label_color = (30, 30, 30)

    # Get filenames for labels
    submitted_name = os.path.splitext(os.path.basename(input_filename))[0]

    # Bottom labels
    cv2.putText(canvas, "Submitted: " + submitted_name,
                (30, canvas_height - 15), font, font_scale, label_color, thickness, cv2.LINE_AA)

    cv2.putText(canvas, "Matched: " + matched_name,
                (stacked.shape[1] // 2 + 30, canvas_height - 15),
                font, font_scale, label_color, thickness, cv2.LINE_AA)

    
    match_percent = f"{score * 100:.2f}%"
    if score >= 0.75:
        result_text = f"Match Found ({match_percent})"
        result_color = (0, 180, 0)
    elif score > 0.4:
        result_text = f"Partial Match ({match_percent})"
        result_color = (0, 0, 255)
    else:
        result_text = f"No Match ({match_percent})"
        result_color = (0, 0, 255)

    
    
    text_size = cv2.getTextSize(result_text, font, font_scale + 0.2, 2)[0]
    text_x = (canvas_width - text_size[0]) // 2
    cv2.putText(canvas, result_text, (text_x, 45),
                font, font_scale + 0.2, result_color, 2, cv2.LINE_AA)


    cv2.imshow("Fingerprint Match Result", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    report_filename = f"match_report_{submitted_name.replace(' ', '_')}.jpg"
    cv2.imwrite(report_filename, canvas)
    print(f" Match report saved as: {report_filename}")





def main():
    print(" Fingerprint Recognition with ORB")

    if not os.path.exists(DATABASE_FOLDER):
        print(f"❌ Database folder not found: {DATABASE_FOLDER}")
        return

    database = load_fingerprint_database(DATABASE_FOLDER)
    if not database:
        print("❌ No fingerprint images found in database.")
        return

    
    Tk().withdraw()
    input_path = filedialog.askopenfilename(title="Select a fingerprint image to recognize",
                                            filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not input_path:
        print("❌ No image selected.")
        return

    input_image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if input_image is None:
        print("❌ Failed to load the selected image.")
        return

    matched_name, matched_img, score, kp1, kp2, matches = match_fingerprint(input_image, database)
   
    show_result(input_image, matched_img, matched_name, score, kp1, kp2, matches, input_path)


if __name__ == "__main__":
    main()
