import numpy
from PIL import Image as im

def preserve_color_YCC():	 
	contentIm = im.open('boston.jpg')
	contentIm = contentIm.convert("YCbCr")
	contentImYUV = numpy.array(contentIm)

	stylizedIm = im.open('monet-boston.jpg')
	stylizedIm = stylizedIm.convert("YCbCr")
	stylizedImYUV = numpy.array(stylizedIm)

	for i in range(len(contentImYUV)):
		for j in range(len(contentImYUV[0])):
			contentImYUV[i][j][0] = stylizedImYUV[i][j][0]

	out = im.fromarray(contentImYUV, 'YCbCr')

	out.save('boston_YCC.jpg')
	out.show()

def preserve_color_RGB():
	contentIm = im.open('boston.jpg')
	contentIm = contentIm.convert("RGB")
	contentArray = numpy.array(contentIm)

	stylizedIm = im.open('monet-boston.jpg')
	stylizedIm = stylizedIm.convert("RGB")
	stylizedArray = numpy.array(stylizedIm)

	CONTENT_WEIGHT = 0.5
	STYLIZED_WEIGHT = 0.5
	height = len(contentArray)
	width = len(contentArray[0])
	outArray = numpy.empty((height, width, 3))

	for i in range(height):
		for j in range(width):
			weightedContent = CONTENT_WEIGHT*contentArray[i][j]
			weightedStyle = STYLIZED_WEIGHT*stylizedArray[i][j]
			outArray[i][j] = weightedContent + weightedStyle

	out = im.fromarray(outArray.astype('uint8'), 'RGB')

	out.save('boston_RGB.jpg')
	out.show()

preserve_color_YCC()
preserve_color_RGB()