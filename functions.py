import ee

#calculate normalized difference vegetation index
def ndvi(image):
    return image.normalizedDifference(['Nir_median', 'Red_median']).rename('ndvi')

#calculate land surface water index
def lswi(image):
    return image.normalizedDifference(['Nir_median', 'Swir1_median']).rename('lswi')

#calculate modified normalized difference water index
def mndwi(image):
    return image.normalizedDifference(['Green_median', 'Swir1_median']).rename('mndwi')

def Evi(image):
    # calculate the enhanced vegetation index
    evi = image.expression('2.5 * (Nir - Red) / (1 + Nir + 6 * Red - 7.5 * Blue)', {
    'Nir': image.select(['Nir']),
    'Red': image.select(['Red']),
    'Blue': image.select(['Blue'])
    })
    return evi.rename(['evi'])

#this function add selected index to the image as additional band
def addindex(index):
    return index.addBands

def areaImg(image, scale):
    areaImage = image.multiply(ee.Image.pixelArea())
    area = areaImage.reduceRegion(**{
        'reducer': ee.Reducer.sum(),
        'geometry': ee.Geometry(image.geometry()),
        'scale': scale,
        'maxPixels': 1e15,
        'tileScale': 16
    })
    return area

#### STATS: 
# get highest value
def maxValue(img, scale):
    max_value = img.reduceRegion(**{
        'reducer': ee.Reducer.max(),
        'geometry': img.geometry(),
        'scale': scale,
        'maxPixels': 1e9
    })
    return max_value

# get lowest value
def minValue(img, scale):
    min_value = img.reduceRegion(**{
        'reducer': ee.Reducer.min(),
        'geometry': img.geometry(),
        'scale': scale,
        'maxPixels': 1e10
    })
    return min_value

# get mean value
def meanValue(img, scale):
    mean_value = img.reduceRegion(**{
        'reducer': ee.Reducer.mean(),
        'geometry': img.geometry(),
        'scale': scale,
        'maxPixels': 1e9
    })
    return mean_value

# get standard deviation
def stdValue(img, scale):
    std_value = img.reduceRegion(**{
        'reducer': ee.Reducer.stdDev(),
        'geometry': img.geometry(),
        'scale': scale,
        'maxPixels': 1e9
    })
    return std_value

#calculate normalized difference vegetation index
def ndviMap(image):
    ndvi= image.normalizedDifference(['Nir', 'Red']).rename('ndvi')
    return image.addBands(ndvi)

#calculate land surface water index
def lswiMap(image):
    lswi= image.normalizedDifference(['Nir', 'Swir1']).rename('lswi')
    return image.addBands(lswi)

#calculate modified normalized difference water index
def mndwiMap(image):
    mndwi= image.normalizedDifference(['Green', 'Swir1']).rename('mndwi')
    return image.addBands(mndwi)

def EviMap(image):
    # calculate the enhanced vegetation index
    evi = image.expression('2.5 * (Nir - Red) / (1 + Nir + 6 * Red - 7.5 * Blue)', {
    'Nir': image.select(['Nir']),
    'Red': image.select(['Red']),
    'Blue': image.select(['Blue'])
    }).rename(['evi'])
    return image.addBands(evi)

# this function add selected index to the image as additional band
def addindex(index):
    return index.addBands

def p_5(image, scale):
    p5 = image.reduceRegion(**{
        'reducer': ee.Reducer.percentile([5]),
        'geometry': image.geometry(),
        'scale': scale,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p5
def p_10(image, scale):
    p10 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([10]),
        'geometry': image.geometry(),
        'scale': scale,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p10
def p_40(image, scale):
    p40 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([40]),
        'geometry': image.geometry(),
        'scale': scale,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p40

def p_50(image, scale):
    p50 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([50]),
        'geometry': image.geometry(),
        'scale': scale,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p50

def p_60(image, scale):
    p60 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([60]),
        'geometry': image.geometry(),
        'scale': scale,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p60

def p_75(image, scale):
    p_75 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([75]),
        'geometry': image.geometry(),
        'scale': scale,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p_75

def p_80(image, scale):
    p80 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([80]),
        'geometry': image.geometry(),
        'scale': scale,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p80

def p_90(image, scale):
    p90 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([90]),
        'geometry': image.geometry(),
        'scale': scale,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p90

def p_95(image, scale):
    p95 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([95]),
        'geometry': image.geometry(),
        'scale': scale,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p95