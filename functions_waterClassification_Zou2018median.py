def Ndvi(image):
    # calculate ndvi
    ndvi = image.normalizedDifference(['Nir_median', 'Red_median']).rename('ndvi')
    return ndvi

def Evi(image):
    # calculate the enhanced vegetation index
    evi = image.expression('2.5 * (Nir_median - Red_median) / (1 + Nir_median + 6 * Red_median - 7.5 * Blue_median)', {
    'Nir_median': image.select(['Nir_median']),
    'Red_median': image.select(['Red_median']),
    'Blue_median': image.select(['Blue_median'])
    })
    return evi.rename(['evi'])

def Mndwi(image):
    # calculate mndwi
    mndwi = image.normalizedDifference(['Green_median', 'Swir1_median']).rename('mndwi')
    return mndwi

def ClassifyWaterZou2018(image):
    mndwi = Mndwi(image)
    ndvi = Ndvi(image)
    evi = Evi(image)

    water = (mndwi.gt(ndvi).Or(mndwi.gt(evi))).And(evi.lt(0.1))
    return(water.rename(['waterMask']))