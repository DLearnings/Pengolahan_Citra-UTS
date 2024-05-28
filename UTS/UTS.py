import streamlit as st
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Fungsi untuk mengubah RGB menjadi HSV
def convert_rgb_to_hsv(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return hsv_image


# Fungsi untuk mengatur kecerahan dan kontras
def adjust_brightness_contrast(image, brightness=0, contrast=0):
    brightness = int((brightness - 50) * 2.55)
    contrast = int((contrast - 50) * 2.55)
    
    img = image.copy()
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        img = cv2.addWeighted(img, alpha_b, img, 0, gamma_b)

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        img = cv2.addWeighted(img, alpha_c, img, 0, gamma_c)

    return img

# Fungsi untuk mendeteksi kontur
def detect_contours(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = image.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
    return contour_image, contours

# Menampilkan judul dan deskripsi aplikasi
st.title("Manipulasi gambar menggunakan Streamlit")
st.subheader("Muhammad Dikaisa Ibnu Amin (312210289)")
st.subheader("Rio Haryono (312210681)")
st.write("Unggah sebuah gambar yang ingin di Manipulasi")

# Upload gambar
uploaded_file = st.file_uploader("Pilih gambar yang ingin diolah...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Membaca gambar
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    # Konversi gambar dari BGR ke RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    st.image(image_rgb, caption='Uploaded Image', use_column_width=True)
    st.write("Choose an action to perform on the image:")

    # Convert RGB to HSV
    if st.button('Convert RGB to HSV'):
        hsv_image = convert_rgb_to_hsv(image)
        st.image(hsv_image, caption='HSV Image', use_column_width=True, channels="HSV")


    # Adjust Brightness and Contrast
    brightness = st.slider('Brightness', 0, 100, 50)
    contrast = st.slider('Contrast', 0, 100, 50)
    st.write(f"Brightness: {brightness}, Contrast: {contrast}")
    adjusted_image = adjust_brightness_contrast(image, brightness, contrast)
    adjusted_image_rgb = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)
    st.image(adjusted_image_rgb, caption='Adjusted Image', use_column_width=True)

    # Detect Contours
    if st.button('Detect Contours'):
        contour_image, contours = detect_contours(image)
        contour_image_rgb = cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB)
        st.image(contour_image_rgb, caption='Contour Image', use_column_width=True)
        st.write(f'Number of contours found: {len(contours)}')