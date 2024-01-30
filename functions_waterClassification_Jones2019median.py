
  # /* water test functions for determing DSWE
# see https://github.com/USGS-EROS/espa-surface-water-extent/blob/master/dswe/algorithm-description.md
# */
def Mndwi(image):
    return(image.normalizedDifference(['Green_median', 'Swir1_median']).rename('mndwi'))

def Mbsrv(image):
    return(image.select(['Green_median']).add(image.select(['Red_median'])).rename('mbsrv'))

def Mbsrn(image):
    return(image.select(['Nir_median']).add(image.select(['Swir1_median'])).rename('mbsrn'))

def Ndvi(image):
    return(image.normalizedDifference(['Nir_median', 'Red_median']).rename('ndvi'))

def Awesh(image):
    return(image.expression('Blue_median + 2.5 * Green_median + (-1.5) * mbsrn + (-0.25) * Swir2_median', {
    'Blue_median': image.select(['Blue_median']),
    'Green_median': image.select(['Green_median']),
    'mbsrn': Mbsrn(image).select(['mbsrn']),
    'Swir2_median': image.select(['Swir2_median'])}))

def Dswe(i):
    mndwi = Mndwi(i)
    mbsrv = Mbsrv(i)
    mbsrn = Mbsrn(i)
    awesh = Awesh(i)
    swir1_median = i.select(['Swir1_median'])
    nir = i.select(['Nir_median'])
    ndvi = Ndvi(i)
    blue = i.select(['Blue_median'])
    swir2_median = i.select(['Swir2_median'])

    t1 = mndwi.gt(0.124)
    t2 = mbsrv.gt(mbsrn)
    t3 = awesh.gt(0)
    t4 = (mndwi.gt(-0.44)
    .And(swir1_median.lt(900))
    .And(nir.lt(1500))
    .And(ndvi.lt(0.7)))
    t5 = (mndwi.gt(-0.5)
    .And(blue.lt(1000))
    .And(swir1_median.lt(3000))
    .And(swir2_median.lt(1000))
    .And(nir.lt(2500)))

    t = t1.add(t2.multiply(10)).add(t3.multiply(100)).add(t4.multiply(1000)).add(t5.multiply(10000))

    noWater = (t.eq(0)
    .Or(t.eq(1))
    .Or(t.eq(10))
    .Or(t.eq(100))
    .Or(t.eq(1000)))
    hWater = (t.eq(1111)
    .Or(t.eq(10111))
    .Or(t.eq(11011))
    .Or(t.eq(11101))
    .Or(t.eq(11110))
    .Or(t.eq(11111)))
    mWater = (t.eq(111)
    .Or(t.eq(1011))
    .Or(t.eq(1101))
    .Or(t.eq(1110))
    .Or(t.eq(10011))
    .Or(t.eq(10101))
    .Or(t.eq(10110))
    .Or(t.eq(11001))
    .Or(t.eq(11010))
    .Or(t.eq(11100)))
    pWetland = t.eq(11000)
    lWater = (t.eq(11)
    .Or(t.eq(101))
    .Or(t.eq(110))
    .Or(t.eq(1001))
    .Or(t.eq(1010))
    .Or(t.eq(1100))
    .Or(t.eq(10000))
    .Or(t.eq(10001))
    .Or(t.eq(10010))
    .Or(t.eq(10100)))

    iDswe = (noWater.multiply(0)
    .add(hWater.multiply(1))
    .add(mWater.multiply(2))
    .add(pWetland.multiply(3))
    .add(lWater.multiply(4)))

    return(iDswe.rename(['dswe']))

def ClassifyWaterJones2019(img):
    dswe = Dswe(img)
    waterMask = dswe.eq(1).Or(dswe.eq(2)).rename(['waterMask'])
    return(waterMask)