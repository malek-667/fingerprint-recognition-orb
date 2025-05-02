# 🔍 Fingerprint Recognition using ORB and Image Processing

This project performs fingerprint recognition using the ORB (Oriented FAST and Rotated BRIEF) algorithm. It combines image preprocessing techniques such as histogram equalization and Gabor filtering with feature extraction and matching, providing a reliable method for comparing fingerprint images — even when they are rotated or altered.

When running the code it will ask the user to import the fingerprint that he wants to match , loads the database and  performs the  process explained above ( processing  filtering the input , matching the score with each image in the database and return the best match  while showing the score of each  comparession  in the terminal window ) and generates a report with the input and the best match.

 we used the same name of the original and altred fingerpints to confirm the accuracy of the code.

 we recommmend that you to use fignerprints with same size as the ones in the original databse or choose from the edited fingerprints folder.

---

Authors : TALEB A MALEK  & BOUMAZA CHOAYB

## Features

- Image preprocessing with histogram equalization and Gabor filtering.
- ORB keypoint detection and descriptor matching.
- Handles rotated and slightly altered fingerprint images.
- Visualizes matching keypoints with annotated comparison results.
- Generates a side-by-side fingerprint match report with score.
- Interactive image input using a file dialog.

---

## Folder Structure

├── FingerPrint_Recognition_ORB.py # Main Python script
├── fingerprint_database/ # Folder containing known fingerprint images
├── edited fingerprints/ # Test set with rotated/smudged/sketched variants
├── How ORB Works.md # Documentation on how ORB functions
├── match_report_*.jpg # Auto-generated match reports (after running)

---

## ⚙️ Installation & Requirements

Make sure you have Python installed (version 3.6+ recommended).

### Install dependencies

bash
```pip install opencv-python numpy```

---

### How to Run

Clone or download this repository to your local machine.

Make sure your fingerprint images are in the fingerprint_database/ folder.

Run the Python script:

```python FingerPrint_Recognition_ORB.py```

---
A file dialog will open. Select a fingerprint image to match.

The program will preprocess the image, match it against the database, and display a visual result with the match score.

A JPG report of the match will also be saved locally.

---

### How It Works – Code Breakdown

1. Loading the Database

```load_fingerprint_database()```

Reads all fingerprint images from the fingerprint_database/ folder.

2.Preprocessing Step

```preprocess_fingerprint()```

Applies Histogram Equalization to enhance contrast.

Applies Gabor Filtering (commonly used in fingerprint analysis) to emphasize ridge patterns.

3.Feature Extraction and Matching

```orb_match_score()```

Uses ORB to detect keypoints and extract binary descriptors.

Matches descriptors using Brute Force Hamming Matcher with cross-checking.

Computes a match score from the average distance of top matches.

4.Comparison and Result

``` show_result() ```

Displays both the input and matched fingerprint side by side.

Annotates the matched keypoints in red.

Prints match classification: Match, Partial Match, or No Match.

Saves the result as a .jpg file.

✅ Matching Capability
Thanks to the rotation-invariant nature of ORB and the Gabor filtering preprocessing, this system performs well even with:

Rotated fingerprints

Slightly smudged or altered inputs

Low-contrast or noisy images (to a limit)

 Sample Result:
 Submitted: fngr1_edited.png     Matched: fngr1.png
🔴 Keypoint matches are drawn
✅ Match Found (92.75%)

---

License

This project is open source and free to use for educational and non-commercial purposes.
