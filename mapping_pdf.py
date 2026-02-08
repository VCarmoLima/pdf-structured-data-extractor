import pdfplumber
from PIL import Image, ImageDraw, ImageFont

caminho_pdf = "exemplo.pdf"  # Substitua pelo caminho do seu arquivo


def mapear_coordenadas():
    with pdfplumber.open(caminho_pdf) as pdf:
        pagina = pdf.pages[0]

        print(
            f"--- Dimensões da Página: Largura {pagina.width} x Altura {pagina.height} ---"
        )
        print("Imprimindo as primeiras 20 palavras e suas posições para exemplo:\n")
        palavras = pagina.extract_words()
        for i, palavra in enumerate(palavras):
            if i > 20:
                break
            print(
                f"Texto: '{palavra['text']}' | Coordenadas: x0={palavra['x0']:.2f}, top={palavra['top']:.2f}, x1={palavra['x1']:.2f}, bottom={palavra['bottom']:.2f}"
            )

        im = pagina.to_image(resolution=200)

        im.draw_rects(palavras, stroke="red", stroke_width=2)

        im.save("mapa_visual.png")
        print("\nArquivo 'mapa_visual.png' gerado com sucesso! Abra para ver as áreas.")


def criar_gabarito(caminho_pdf):
    print(f"Mapeando arquivo: {caminho_pdf}...")

    with pdfplumber.open(caminho_pdf) as pdf:
        pagina = pdf.pages[0]

        largura_pdf = pagina.width
        altura_pdf = pagina.height

        im = pagina.to_image(resolution=200)
        original = im.original
        draw = ImageDraw.Draw(original)

        largura_img, altura_img = original.size
        escala_x = largura_img / largura_pdf
        escala_y = altura_img / altura_pdf

        print(f"Dimensões PDF: {largura_pdf:.0f}x{altura_pdf:.0f}")
        print(f"Dimensões Imagem: {largura_img}x{altura_img}")
        print(f"Fator de Escala: {escala_x:.2f}x")

        passo = 20

        for x in range(0, int(largura_pdf), passo):
            pos_pixel = x * escala_x

            cor = "red" if x % 100 == 0 else "salmon"
            largura = 3 if x % 100 == 0 else 1

            draw.line(
                [(pos_pixel, 0), (pos_pixel, altura_img)], fill=cor, width=largura
            )

            if x % 50 == 0:
                draw.text((pos_pixel + 2, 10), str(x), fill="red")

        for y in range(0, int(altura_pdf), passo):
            pos_pixel = y * escala_y

            cor = "blue" if y % 100 == 0 else "lightblue"
            largura = 3 if y % 100 == 0 else 1

            draw.line(
                [(0, pos_pixel), (largura_img, pos_pixel)], fill=cor, width=largura
            )

            if y % 50 == 0:
                draw.text((5, pos_pixel + 2), str(y), fill="blue")

        nome_saida = "gabarito_final.png"
        original.save(nome_saida)
        print(f"\nSucesso! Abra o arquivo '{nome_saida}'.")


if __name__ == "__main__":
    mapear_coordenadas()
    criar_gabarito(caminho_pdf)
