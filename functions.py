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

def ErosDil(image):
    kernel = ee.Kernel.square(2)
    opened = image.focalMin(kernel=kernel, iterations=2).focalMax(kernel=kernel, iterations=2)
    return opened

def ClassifyWater(imgIn, method = 'Jones2019'):
    if method == 'Jones2019':
        from functions_waterClassification_Jones2019median import ClassifyWaterJones2019
        return(ClassifyWaterJones2019(imgIn))
    elif method == 'Zou2018':
        from functions_waterClassification_Zou2018median import ClassifyWaterZou2018
        return(ClassifyWaterZou2018(imgIn))
    
def histogram(image, scale_hist):
    # Compute the histogram of the NIR band.  The mean and variance are only FYI.
    polygon = ee.Geometry(image.geometry())
    histogram = image.reduceRegion(
        **{
            'reducer': ee.Reducer.histogram(255, 2),
            'geometry': polygon,
            'scale': scale_hist,
            'bestEffort': True,
        }
    )
    return histogram

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

def extract_ac(imagesat,imagemndwi, t_sat, t_mndwi):
    ac = imagesat.select('saturation_median').gte(t_sat).Or(imagemndwi.select('mndwi_median').gte(t_mndwi)).selfMask()
    return ee.Image(ac)

def stdLocal (image, roi, scale): 
    geom = roi.geometry()
    std_value = image.clip(geom).reduceRegion(**{
        'reducer': ee.Reducer.stdDev(),
        'geometry': geom,
        'scale': scale,
        'maxPixels': 1e12,
        'tileScale': 16
    })
    return std_value

def peronaMalikFilter(I, iter, K, method, l):
    '''
    PERONA MALIK FILTER
    Perona malik filter
    I(n+1, i, j) = I(n, i, j) + Lambda * (cN * dN(I) + cS * dS(I) + cE * dE(I), cW * dW(I))
    
    Perona-Malik (anisotropic diffusion) convolution
    by Gennadii Donchyts see https://groups.google.com/forum/#!topic/google-earth-engine-developers/a9W0Nlrhoq0
    I(n+1, i, j) = I(n, i, j) + lambda * (cN * dN(I) + cS * dS(I) + cE * dE(I), cW * dW(I))
    iter: Number of interations to apply filter
    K: kernel size
    method: choose method 1 (default) or 2
    Returns: image 
    '''
    dxW = ee.Kernel.fixed(3, 3, [[ 0,  0,  0], [ 1, -1,  0], [ 0,  0,  0]])
    dxE = ee.Kernel.fixed(3, 3, [[ 0,  0,  0], [ 0, -1,  1], [ 0,  0,  0]])
    dyN = ee.Kernel.fixed(3, 3, [[ 0,  1,  0], [ 0, -1,  0], [ 0,  0,  0]])
    dyS = ee.Kernel.fixed(3, 3, [[ 0,  0,  0], [ 0, -1,  0], [ 0,  1,  0]])
    
    Lambda = l 
    
    k1 = ee.Image(-1.0/K)
    k2 = ee.Image(K).multiply(ee.Image(K))
    
    for i in range(0, iter):
        dI_W = I.convolve(dxW)
        dI_E = I.convolve(dxE)
        dI_N = I.convolve(dyN)
        dI_S = I.convolve(dyS)
        
        if method == 1:
            cW = dI_W.multiply(dI_W).multiply(k1).exp()
            cE = dI_E.multiply(dI_E).multiply(k1).exp()
            cN = dI_N.multiply(dI_N).multiply(k1).exp()
            cS = dI_S.multiply(dI_S).multiply(k1).exp()
        elif method == 2:
            cW = ee.Image(1.0).divide(ee.Image(1.0).add(dI_W.multiply(dI_W).divide(k2)))
            cE = ee.Image(1.0).divide(ee.Image(1.0).add(dI_E.multiply(dI_E).divide(k2)))
            cN = ee.Image(1.0).divide(ee.Image(1.0).add(dI_N.multiply(dI_N).divide(k2)))
            cS = ee.Image(1.0).divide(ee.Image(1.0).add(dI_S.multiply(dI_S).divide(k2)))
        I = I.add(ee.Image(Lambda).multiply(cN.multiply(dI_N).add(cS.multiply(dI_S)).add(cE.multiply(dI_E)).add(cW.multiply(dI_W))))
    
    return I

def check_tasks_status(tasks_list):
    export_task  = [dict for dict in tasks_list  if dict['metadata']['type' ] == 'EXPORT_IMAGE']
    running_task = [dict for dict in export_task if dict['metadata']['state'] == 'RUNNING'     ]
    ready_task   = [dict for dict in export_task if dict['metadata']['state'] == 'READY'       ]
    unsub_task   = [dict for dict in export_task if dict['metadata']['state'] == 'UNSUBMITTED' ]

    run     = len(running_task)
    not_run = len(ready_task) + len(unsub_task)
    
    return run, not_run
