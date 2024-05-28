import cv2
import pytesseract

def caminho_tesseract():
    '''
    INSIRA O CAMINHO DE ONDE O TESSERACT TA INSTALADO
    '''
    return r"C:\Users\jorge.douettes\AppData\Local\Programs\Tesseract-OCR"


def encontra_roi():
    img = cv2.imread('Carro.png')
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('imagem_original', img)

    _, bin = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)

    desfoque = cv2.GaussianBlur(bin, (5,5), 0)

    contornos, hier = cv2.findContours(desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.imshow('imagem_binarizada', desfoque)

    for c in contornos:
        perimetros = cv2.arcLength(c, True)
        if perimetros > 150:
            aprox = cv2.approxPolyDP(c, 0.03 * perimetros, True)
            if len(aprox) == 4:
                (x, y, alt, lag) = cv2.boundingRect(c)
                cv2.rectangle(img, (x, y), (x + alt, y + lag), (0,255,0), 2)
                cv2.imshow('imagem_binarizada222', img)
                roi = img[y:y+lag, x:x+alt]
                nome = 'roi.jpg'
                cv2.imwrite(nome, roi)
                return nome

    cv2.imshow('draw', img)
    cv2.waitKey(0)

def processamento_roi():
    img_roi = cv2.imread('roi.jpg')

    img_resize = cv2.resize(img_roi, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    img_cinza = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)



    _, img_binary = cv2.threshold(img_cinza, 60, 255, cv2.THRESH_BINARY)

    cv2.imshow("res", img_binary)

    cv2.imwrite("roi-ocr.png", img_binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def ocr_image():
    img_roi = cv2.imread("roi-ocr.png")
    caminho = caminho_tesseract()
    pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"
    saida = pytesseract.image_to_string(img_roi, lang="eng")
    print(saida)


if __name__ == "__main__":
    encontra_roi()
    processamento_roi()
    ocr_image()