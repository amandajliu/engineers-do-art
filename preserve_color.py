import numpy
from PIL import Image as im

def preserve_color():	 
	contentIm = im.open('hongkong.jpg')
	contentIm = contentIm.convert("YCbCr")
	contentImYUV = numpy.array(contentIm)

	stylizedIm = im.open('hongkong-guernica.jpg')
	stylizedIm = stylizedIm.convert("YCbCr")
	stylizedImYUV = numpy.array(stylizedIm)

	for i in range(len(contentImYUV)):
		for j in range(len(contentImYUV[0])):
			contentImYUV[i][j][0] = stylizedImYUV[i][j][0]

	out = im.fromarray(contentImYUV, 'YCbCr')

	out.save('out_preserve_color.jpg')
	out.show()

preserve_color()
