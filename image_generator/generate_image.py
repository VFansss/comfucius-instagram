# coding=utf-8
import textwrap
import os
from PIL import Image, ImageFont, ImageDraw, ImageOps

def generate_image(path_background_image, generated_image_directory, generated_image_filename_no_extension, text_to_use):

    # Carica l'immagine di sfondo
    background_image = Image.open(path_background_image)

    # Scala fino alla risoluzione ideale
    background_image = ImageOps.fit(background_image, (1080, 1350), centering=(0.5,0.5))

    # Converti l'immagine di sfondo in formato RGBA
    background_image = background_image.convert("RGBA")

    # Crea un'immagine di dimensioni pari all'immagine di sfondo con un colore scuro
    overlay = Image.new("RGBA", background_image.size, (0, 0, 0, 150))

    # Sovrapponi l'immagine di sfondo con l'overlay scuro
    background_image = Image.alpha_composite(background_image, overlay)

    # Crea un oggetto draw per disegnare sull'immagine
    draw = ImageDraw.Draw(background_image)

    # Disegna un bordo attorno all'immagine.

    (bg_width, bg_height) = background_image.size;

    space_multiplier = 0.05

    border_horiz_margin = bg_width * space_multiplier
    border_vert_margin = bg_height * space_multiplier

    border_top_left_angle = (border_horiz_margin,border_vert_margin)
    border_bottom_left_angle = (border_horiz_margin, bg_height-border_vert_margin)
    border_bottom_right_angle = (bg_width-border_horiz_margin, bg_height-border_vert_margin)
    border_top_right_angle = (bg_width-border_horiz_margin,border_vert_margin)

    border_fill = (255,255,255)
    border_width = 5

    draw.line([border_top_left_angle,border_bottom_left_angle],border_fill,border_width)
    draw.line([border_bottom_left_angle,border_bottom_right_angle],border_fill,border_width)
    draw.line([border_bottom_right_angle,border_top_right_angle],border_fill,border_width)
    draw.line([border_top_right_angle,border_top_left_angle],border_fill,border_width)

    # Converti tutto in maiuscolo, e divide la frase motivazionale in due parti
    phrase, author = text_to_use.upper().split(" ~ ")

    ## Calculate font size

    draw = ImageDraw.Draw(background_image)
    fontsize = 1  # starting font size

    # La frase è troppo lunga? Dividiamola in parti accettabili
    phrase_lines = textwrap.wrap(phrase, width=24)
    longest_phrase_line = max(phrase_lines, key=len);

    # portion of background_image width you want text width to be
    img_fraction = 0.80

    font_path_for_phrase = os.path.abspath("image_generator" + os.sep + "fonts") + os.sep + "MerriweatherSans-SemiBold.ttf"
    font_path_for_author = os.path.abspath("image_generator" + os.sep + "fonts") + os.sep + "Caveat-Medium.ttf"

    font = ImageFont.truetype(font_path_for_phrase, fontsize)
    breakpoint = img_fraction * background_image.size[0]
    jumpsize = 75

    # Calcola la dimensione del font basandosi solo sulla frase
    while True:
        if font.getlength(longest_phrase_line) < breakpoint:
            fontsize += jumpsize
        else:
            jumpsize = jumpsize // 2
            fontsize -= jumpsize
        font = ImageFont.truetype(font_path_for_phrase, fontsize)
        if jumpsize <= 1:
            break

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1

    # Disegna la frase
    phrase_coordinates = draw.multiline_text((background_image.width/2,background_image.height/2), "\n".join(phrase_lines), spacing=40, align="center", anchor="mm", font=font, fill=(255, 255, 255))

    (left, top, right, bottom) = draw.multiline_textbbox((background_image.width/2,background_image.height/2), "\n".join(phrase_lines), spacing=40, align="center", anchor="mm", font=font)

    # Calcola le coordinate dell'autore in modo da posizionarlo sotto la frase
    draw.text((background_image.width/2, bottom+40),"\n\n~ "+author, align="center", anchor="mm", font=ImageFont.truetype(font_path_for_author, int(fontsize/2)), fill=(255, 255, 255))

    # Salva l'immagine
    saved_background_imagepath = generated_image_directory + os.sep + generated_image_filename_no_extension +".jpg"
    background_image.convert('RGB').save(saved_background_imagepath)

    return saved_background_imagepath
