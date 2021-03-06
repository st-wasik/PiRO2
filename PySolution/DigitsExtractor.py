import cv2 as cv
from PIL import Image

from Preprocessor import *

class DigitsExtractor:

    @staticmethod
    def extract(words):
        if words == []:
            return []

        digits = []

        for word in [words[-1]]:

            x, y = word.shape
            kx, ky = (8, 16)
            x = (x if x < kx else kx) - 2
            y = (y if y < ky else ky) - 2
            rect_kernel_size = x, y

            kernel_rect = cv.getStructuringElement(cv.MORPH_RECT, rect_kernel_size)

            word_copy = word.copy()
            word_copy = Preprocessor.erode(word_copy, 2)
            word_copy = Preprocessor.dilate(word_copy, kernel=kernel_rect)
            contours, _ = cv.findContours(word_copy, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            for i, c in enumerate(contours):
                boundRect = cv.boundingRect(c)

                x = boundRect[0]
                y = boundRect[1]
                width = boundRect[2]
                height = boundRect[3]

                marginX = 0
                marginY = 0
                rect_kernel_size = kernel_rect.shape
                if width > (rect_kernel_size[0] + marginX) and height > (rect_kernel_size[1] + marginY):

                    digit = word[boundRect[1]:boundRect[1] + boundRect[3], boundRect[0]:boundRect[0] + boundRect[2]].copy()
                    digits.append((boundRect[0], digit))

        digits = sorted(digits, key=lambda x: x[0])
        digits = [d[1] for d in digits]

        return [DigitsExtractor.format_for_mnist(d) for d in digits]

    @staticmethod
    def place_in_center(img):
        img = img.astype(int)
        rows, cols = img.shape
        new_size = (rows if rows > cols else cols) + 16

        new_image = np.zeros((new_size, new_size)).astype(int)

        x = int(new_size / 2) - int(rows / 2)
        y = int(new_size / 2) - int(cols / 2)

        new_image[x:x + rows, y:y + cols] = img
        return new_image

    @staticmethod
    def format_for_mnist(digit_image):
        t = digit_image
        t = DigitsExtractor.place_in_center(t).astype('uint8')
        t = Image.fromarray(t)
        t = t.resize((28, 28), Image.ANTIALIAS)
        t = np.asarray(t)
        return t
