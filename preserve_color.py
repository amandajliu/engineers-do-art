import numpy
from PIL import Image as im
from skimage import io, color, novice
from skimage.viewer import ImageViewer

# color transfer using the YCbCr color space
def preserve_color_YCbCr(content, stylized, out_name):
    
    # read the content image and convert it to YCbCr
    contentIm = im.open(content)
    contentIm = contentIm.convert("YCbCr")
    contentImYUV = numpy.array(contentIm)

    # read the stylized image and convert it to YCbCr
    stylizedIm = im.open(stylized)
    stylizedIm = stylizedIm.convert("YCbCr")
    stylizedImYUV = numpy.array(stylizedIm)

    # replaces the Y channel of the content image with that of the stylized image
    for i in range(len(contentImYUV)):
        for j in range(len(contentImYUV[0])):
            contentImYUV[i][j][0] = stylizedImYUV[i][j][0]

    out = im.fromarray(contentImYUV, 'YCbCr')

    out.save(out_name)
    out.show()

# weighted RGB color transfer
def preserve_color_RGB(content, stylized, out_name, stylized_weight, content_weight):

    # read the content image and convert it to RGB 
    contentIm = im.open(content)
    contentIm = contentIm.convert("RGB")
    contentArray = numpy.array(contentIm)

    # read the stylized image and convert it to RGB
    stylizedIm = im.open(stylized)
    stylizedIm = stylizedIm.convert("RGB")
    stylizedArray = numpy.array(stylizedIm)
    
    height = len(contentArray)
    width = len(contentArray[0])
    
    # empty output numpy array
    outArray = numpy.empty((height, width, 3))

    # performs weighted RGB average on each pixel in the image
    for i in range(height):
        for j in range(width):
            weightedContent = content_weight*contentArray[i][j]
            weightedStyle = stylized_weight*stylizedArray[i][j]
            outArray[i][j] = weightedContent + weightedStyle

    out = im.fromarray(outArray.astype('uint8'), 'RGB')

    out.save(out_name)
    out.show()

# color preservation with CIE-LAB
def preserve_color_lab(content, stylized, image_name):
    
    # extract rgb values and then convert to CIELAB for content image and stylized image
    rgbContent = io.imread(content)
    labContent = color.rgb2lab(numpy.asarray(rgbContent)/255.0)
    labContentArray = numpy.array(labContent)
    
    rgbStyle = io.imread(stylized)
    labStyle = color.rgb2lab(numpy.asarray(rgbStyle)/255.0)
    labStyleArray = numpy.array(labStyle)

    # color transfer over L channel
    for i in range(len(labContentArray)):
        for j in range(len(labContentArray[0])):
            labContentArray[i][j][0] = labStyleArray[i][j][0]

    # convert back to RGB to save
    labContentArray = color.lab2rgb(labContentArray)*255.0

    # RGB unpacking
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
    
# CIE-LCh color preservation
def preserve_color_cielch(content, stylized, image_name):
    
    # extract info and convert to CIE-LCh for each image
    rgbContent = io.imread(content)
    labContent = color.lab2lch(color.xyz2lab(color.rgb2xyz(numpy.asarray(rgbContent))))
    labContentArray = numpy.array(labContent)
    rgbStyle = io.imread(stylized)
    labStyle = color.lab2lch(color.xyz2lab(color.rgb2xyz(numpy.asarray(rgbStyle))))
    labStyleArray = numpy.array(labStyle)

    # color transfer
    for i in range(len(labContentArray)):
        for j in range(len(labContentArray[0])):
            labContentArray[i][j][0] = labStyleArray[i][j][0]

    labContentArray = color.xyz2rgb(color.lab2xyz(color.lch2lab(labContentArray)))
    viewer = ImageViewer(labContentArray)
    viewer.show()

# running all four on yosemite and afremov test images
preserve_color_YCbCr('yosemite.jpg', 'afremov-yosemite.jpg', 'yosemite_YCC.jpg')
preserve_color_RGB('yosemite.jpg', 'afremov-yosemite.jpg', 'yosemite_RGB.jpg', 0.5, 0.5)
preserve_color_lab('yosemite.jpg', 'afremov-yosemite.jpg', 'yosemite_LAB.jpg')
preserve_color_cielch('yosemite.jpg', 'afremov-yosemite.jpg', 'yosemite_LCh.jpg')