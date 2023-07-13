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

def areaImg(image):
    areaImage = image.multiply(ee.Image.pixelArea())
    area = areaImage.reduceRegion(**{
        'reducer': ee.Reducer.sum(),
        'geometry': ee.Geometry(image.geometry()),
        'scale': 30,
        'maxPixels': 1e15,
        'tileScale': 16
    })
    return area

#### STATS: 
# get highest value
def maxValue(img, scale=30):
    max_value = img.reduceRegion(**{
        'reducer': ee.Reducer.max(),
        'geometry': img.geometry(),
        'scale': scale,
        'maxPixels': 1e9
    })
    return max_value

# get lowest value
def minValue(img, scale=30):
    min_value = img.reduceRegion(**{
        'reducer': ee.Reducer.min(),
        'geometry': img.geometry(),
        'scale': scale,
        'maxPixels': 1e10
    })
    return min_value

# get mean value
def meanValue(img, scale=30):
    mean_value = img.reduceRegion(**{
        'reducer': ee.Reducer.mean(),
        'geometry': img.geometry(),
        'scale': scale,
        'maxPixels': 1e9
    })
    return mean_value

# get standard deviation
def stdValue(img, scale=30):
    std_value = img.reduceRegion(**{
        'reducer': ee.Reducer.stdDev(),
        'geometry': img.geometry(),
        'scale': scale,
        'maxPixels': 1e9
    })
    return std_value

scale = 30

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

#this function add selected index to the image as additional band
def addindex(index):
    return index.addBands


bnp5 = ['uBlue', 'Blue', 'Green', 'Red', 'Swir1', 'BQA', 'Nir', 'Swir2']
bnp95 = ['uBlue', 'Blue', 'Green', 'Red', 'Swir1', 'BQA', 'Nir', 'Swir2']

def p_5(image):
    p5 = image.reduceRegion(**{
        'reducer': ee.Reducer.percentile([5]),
        'geometry': image.geometry(),
        'scale': 30,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p5
def p_10(image):
    p10 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([10]),
        'geometry': image.geometry(),
        'scale': 30,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p10
def p_40(image):
    p40 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([40]),
        'geometry': image.geometry(),
        'scale': 30,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p40
def p_50(image):
    p50 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([50]),
        'geometry': image.geometry(),
        'scale': 30,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p50
def p_60(image):
    p60 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([60]),
        'geometry': image.geometry(),
        'scale': 30,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p60
def p_75(image):
    p_75 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([75]),
        'geometry': image.geometry(),
        'scale': 30,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p_75
def p_80(image):
    p80 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([80]),
        'geometry': image.geometry(),
        'scale': 30,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p80
def p_90(image):
    p90 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([90]),
        'geometry': image.geometry(),
        'scale': 30,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p90
def p_95(image):
    p95 = image.reduceRegion(**{
         'reducer': ee.Reducer.percentile([95]),
        'geometry': image.geometry(),
        'scale': 30,
        'maxPixels': 1e12,
        'tileScale':16
    })
    return p95

def histogram(image, band):
    # Compute the histogram of the NIR band.  The mean and variance are only FYI.
    polygon = ee.Geometry(image.geometry())
    histogram = image.select('band').reduceRegion(
        **{
            'reducer': ee.Reducer.histogram(255, 2),
            'geometry': polygon,
            'scale': 30,
            'bestEffort': True,
        }
    )
    hist_dict = histogram.getInfo()
    return hist_dict

# Return the DN that maximizes interclass variance in B5 (in the region).
def otsu(histogram):
    counts = ee.Array(ee.Dictionary(histogram).get('histogram'))
    means = ee.Array(ee.Dictionary(histogram).get('bucketMeans'))
    size = means.length().get([0])
    total = counts.reduce(ee.Reducer.sum(), [0]).get([0])
    sum = means.multiply(counts).reduce(ee.Reducer.sum(), [0]).get([0])
    mean = sum.divide(total)

    indices = ee.List.sequence(1, size)

    # Compute between sum of squares, where each mean partitions the data.

    def func_xxx(i):
        aCounts = counts.slice(0, 0, i)
        aCount = aCounts.reduce(ee.Reducer.sum(), [0]).get([0])
        aMeans = means.slice(0, 0, i)
        aMean = (
            aMeans.multiply(aCounts)
            .reduce(ee.Reducer.sum(), [0])
            .get([0])
            .divide(aCount)
        )
        bCount = total.subtract(aCount)
        bMean = sum.subtract(aCount.multiply(aMean)).divide(bCount)
        return aCount.multiply(aMean.subtract(mean).pow(2)).add(
            bCount.multiply(bMean.subtract(mean).pow(2))
        )

    bss = indices.map(func_xxx)

    # Return the mean value corresponding to the maximum BSS.
    return means.sort(bss).get([-1])
