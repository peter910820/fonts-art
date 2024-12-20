import click
import PIL.Image

from math import floor

class FontsArt(object):
    def __init__(self, img_path, zoom):
        self.img_path = img_path
        self.zoom = zoom
        self.img = PIL.Image.open(self.img_path)
        self.chars = ['%', '$', '*', '^', '-', '+', '<', '!', ':', '.', ' ']
        
        width, height = self.img.size
        self.new_width, self.new_height = floor(width * zoom), floor(height * zoom)*0.5
        # self.new_width, self.new_height = 50, height / (width / 50) * zoom
        self.result = ''

    def resize(self):
        self.img = self.img.resize((self.new_width, int(self.new_height)))
        self.img = self.img.convert('L') # translate to Grayscale

    def translate(self, reverse):
        pixels = self.img.getdata()
        if reverse:
            self.chars.reverse()
        new_pixels = [self.chars[pixel//25] for pixel in pixels]
        new_pixels = ''.join(new_pixels)
        ascii_image = [new_pixels[index: index + self.new_width] 
                       for index in range(0, len(new_pixels), self.new_width)]
        self.result = ascii_image = '\n'.join(ascii_image)
        
    def save(self):
        with open(f"{self.img_path[0: -4]}.txt", "w") as f:
            f.write(self.result)

@click.command()
@click.option('-P', '--path', 'path', required=True, help='Your png file path')
@click.option('-Z', '--zoom', 'zoom', default=1.0, required=False, help='zoom feature')
@click.option('-R', '--reverse', 'reverse', default=False, required=False, help='reverse feature')
def main(path: str, zoom: str | float | None, reverse: bool): # zoom should be translate to float
    try:
        if not zoom: zoom = 1.0
        zoom = float(zoom)
    except:
        print('[ERROR:] --zoom options should be float type')
        return
    
    image = FontsArt(path, zoom)
    image.resize()
    image.translate(reverse)
    image.save()

if __name__== '__main__':
    main()