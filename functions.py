import ee

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

def perc(image, perc, scale):
    p = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([perc]),
        'geometry': image.geometry(),
        'scale': scale,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p