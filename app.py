import click
import PIL.Image

class FontsArt(object):
    def __init__(self, img_path, zoom):
        self.img_path = img_path
        self.zoom = zoom
        self.img = PIL.Image.open(self.img_path)
        self.chars = ['%', '*', '^', '^', '-', '+', '<', '!', ':', '.', ' ']
        
        width, height = self.img.size
        self.new_width, self.new_height = 50, height / (width / 50) * zoom
        self.result = ''

    def resize(self):
        self.img = self.img.resize((self.new_width, int(self.new_height)))
        self.img = self.img.convert('L') # translate to Grayscale

    def translate(self):
        pixels = self.img.getdata()
        new_pixels = [self.chars[pixel//25] for pixel in pixels]
        new_pixels = ''.join(new_pixels)
        ascii_image = [new_pixels[index: index + self.new_width] 
                       for index in range(0, len(new_pixels), self.new_width)]
        self.result = ascii_image = '\n'.join(ascii_image)
        
    def save(self):
        with open(f"{self.img_path}.txt", "w") as f:
            f.write(self.result)

@click.command()
@click.option('-P', '--path', 'path', required=True)
@click.option('--zoom', 'zoom', required=False)
def main(path: str, zoom: str = 1.0): # zoom should be translate to float
    try:
        zoom = float(zoom)
    except:
        print('[ERROR:] --zoom options should be float type')
        return
    image = FontsArt(path, zoom)
    image.resize()
    image.translate()
    image.save()

if __name__== '__main__':
    main()