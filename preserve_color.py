import numpy
from PIL import Image as im
from skimage import io, color, novice
from skimage.viewer import ImageViewer

def preserve_color_YCbCr(content, stylized, out_name):
	contentIm = im.open(content)
	contentIm = contentIm.convert("YCbCr")
	contentImYUV = numpy.array(contentIm)

	stylizedIm = im.open(stylized)
	stylizedIm = stylizedIm.convert("YCbCr")
	stylizedImYUV = numpy.array(stylizedIm)

	for i in range(len(contentImYUV)):
		for j in range(len(contentImYUV[0])):
			contentImYUV[i][j][0] = stylizedImYUV[i][j][0]

	out = im.fromarray(contentImYUV, 'YCbCr')

	out.save(out_name)
	out.show()

def preserve_color_RGB(content, stylized, out_name):
	contentIm = im.open(content)
	contentIm = contentIm.convert("RGB")
	contentArray = numpy.array(contentIm)

	stylizedIm = im.open(stylized)
	stylizedIm = stylizedIm.convert("RGB")
	stylizedArray = numpy.array(stylizedIm)

	CONTENT_WEIGHT = 0.7
	STYLIZED_WEIGHT = 0.3
	height = len(contentArray)
	width = len(contentArray[0])
	outArray = numpy.empty((height, width, 3))

	for i in range(height):
		for j in range(width):
			weightedContent = CONTENT_WEIGHT*contentArray[i][j]
			weightedStyle = STYLIZED_WEIGHT*stylizedArray[i][j]
			outArray[i][j] = weightedContent + weightedStyle

	out = im.fromarray(outArray.astype('uint8'), 'RGB')

	out.save(out_name)
	out.show()

def preserve_color_lab(image_name, content, stylized):

	rgbContent = io.imread(content)
	labContent = color.rgb2lab(numpy.asarray(rgbContent)/255.0)
	labContentArray = numpy.array(labContent)
	rgbStyle = io.imread(stylized)

	labStyle = color.rgb2lab(numpy.asarray(rgbStyle)/255.0)
	labStyleArray = numpy.array(labStyle)

	for i in range(len(labContentArray)):
		for j in range(len(labContentArray[0])):
			labContentArray[i][j][0] = labStyleArray[i][j][0]

	labContentArray = color.lab2rgb(labContentArray)*255.0

	H = len(labContentArray)
	W = len(labContentArray[0])
	img = labContentArray.reshape(( H,W,3 ))
	print "img.shape:", img.shape
	r,g,b = img.transpose( 2,0,1 )  # 3 10 5
	print "r.shape:", r.shape

	# pack 10 x 5 r g b -> 10 x 5 x 3 again --
	rgb = numpy.array(( r, g, b )).transpose( 1,2,0 )  # 10 5 3 again
	print "rgb.shape:", rgb.shape
	assert (rgb == img).all()

	# rgb 0 .. 255 <-> float 0 .. 1 --
	imgfloat = img.astype(numpy.float32) / 255.
	img8 = (imgfloat * 255.).round().astype(numpy.uint8)

	out1 = im.fromarray(img8, 'RGB')
	out1.show()
	out1.save(image_name)

def preserve_color_cielab(content, stylized, image_name):
	rgbContent = io.imread('hongkong.jpg')
	labContent = color.xyz2lab(color.rgb2xyz(numpy.asarray(rgbContent)/255.))
	labContentArray = numpy.array(labContent)
	rgbStyle = io.imread('hongkong-guernica.jpg')
	labStyle = color.xyz2lab(color.rgb2xyz(numpy.asarray(rgbStyle)/255.))
	labStyleArray = numpy.array(labStyle)

	for i in range(len(labContentArray)):
		for j in range(len(labContentArray[0])):
			labContentArray[i][j][0] = labStyleArray[i][j][0]

	labContentArray = color.xyz2rgb(color.lab2xyz(labContentArray))
	viewer = ImageViewer(labContentArray)
	viewer.show()

def preserve_color_cielch(content, stylized, image_name):
	rgbContent = io.imread(content)
	labContent = color.lab2lch(color.xyz2lab(color.rgb2xyz(numpy.asarray(rgbContent)/255.)))
	labContentArray = numpy.array(labContent)
	rgbStyle = io.imread(stylized)
	labStyle = color.lab2lch(color.xyz2lab(color.rgb2xyz(numpy.asarray(rgbStyle)/255.)))
	labStyleArray = numpy.array(labStyle)

	for i in range(len(labContentArray)):
		for j in range(len(labContentArray[0])):
			labContentArray[i][j][0] = labStyleArray[i][j][0]

	labContentArray = color.xyz2rgb(color.lab2xyz(color.lch2lab(labContentArray)))*255.
	# viewer = ImageViewer(labContentArray)
	# viewer.show()

	H = len(labContentArray)
	W = len(labContentArray[0])
	img = labContentArray.reshape(( H,W,3 ))
	print "img.shape:", img.shape
	r,g,b = img.transpose( 2,0,1 )  # 3 10 5
	print "r.shape:", r.shape

	# pack 10 x 5 r g b -> 10 x 5 x 3 again --
	rgb = numpy.array(( r, g, b )).transpose( 1,2,0 )  # 10 5 3 again
	print "rgb.shape:", rgb.shape
	assert (rgb == img).all()

	# rgb 0 .. 255 <-> float 0 .. 1 --
	imgfloat = img.astype(numpy.float32) / 255.
	img8 = (imgfloat * 255.).round().astype(numpy.uint8)

	out1 = im.fromarray(img8, 'RGB')
	out1.show()
	out1.save(image_name)



#preserve_color_YCbCr('stata.jpg', 'chinese-stata.jpg', 'stata_YCC.jpg')
#preserve_color_RGB('yosemite.jpg', 'afremov-yosemite.jpg', 'yosemite_RGB_73.jpg')
#preserve_color_lab('gatys_lab.png', 'content_gatys.jpg', 'stylized_gatys.jpg')
preserve_color_cielch('content_gatys.jpg', 'stylized_gatys.jpg', 'gatys_lch.jpg')
