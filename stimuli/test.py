import Image
import ImageChops

im1 = Image.open("dresser00.png")
im2 = Image.open("bowl00.png")

diff = ImageChops.difference(im2, im1)
