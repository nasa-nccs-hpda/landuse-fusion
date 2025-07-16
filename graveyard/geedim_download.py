import ee
import os
import geedim as gd
from glob import glob
from pathlib import Path
import rioxarray as rxr
from shapely.geometry import box

# input to download data for
gee_account = 'id-sl-senegal-service-account@ee-3sl-senegal.iam.gserviceaccount.com'
gee_key = '/home/jacaraba/gee/ee-3sl-senegal-8fa70fe1c565.json'
#filename = '/explore/nobackup/projects/3sl/data/Tappan/Tappan21_WV02_20190119_M1BS_103001008B4CF000_data.tif'
#output_dir = '/explore/nobackup/projects/3sl/labels/landuse/ethiopia_segmentation_experiments_v2'
output_dir = '/explore/nobackup/projects/3sl/data/SAR/S1_Monthly'

# get credentials
credentials = ee.ServiceAccountCredentials(gee_account, gee_key)
ee.Initialize(credentials)  # gd initialize does not take service account
print("Initialized")

# filenames = glob('/panfs/ccds02/nobackup/people/walemu/NRO/WV02_20210322_M1BS_*.tif')
#filenames = glob('/panfs/ccds02/nobackup/people/walemu/NRO/WV03_20211209_M1BS_1040010072958B00-toa-sharpened_RayaKobo.tif')
#filenames = [
#    '/explore/nobackup/projects/3sl/data/Tappan/Tappan01_WV03_20230917_M1BS_104001008A0E6500_data.tif',
#    '/explore/nobackup/projects/3sl/data/Tappan/Tappan02_WV02_20110430_M1BS_103001000A27E100_data.tif',
#    '/explore/nobackup/projects/3sl/data/Tappan/Tappan03_WV02_20110320_M1BS_10300100095E3100_data.tif',
#    ''
#    '/explore/nobackup/projects/3sl/data/Tappan/Tappan05_WV03_20231031_M1BS_104001008C41A200_data.tif',
#    '/explore/nobackup/projects/3sl/data/Tappan/Tappan06_WV03_20231024_M1BS_104001008CD42800_data.tif',
#    '/explore/nobackup/projects/3sl/data/Tappan/Tappan19_WV03_20231024_M1BS_104001008C3E9000_data.tif',
#    '/explore/nobackup/projects/3sl/data/Tappan/Tappan50_WV03_20230620_M1BS_1040010087D26800_data.tif',
#    '/explore/nobackup/projects/3sl/data/Tappan/Tappan24_WV03_20230607_M1BS_10400100860D4600_data.tif',
#    '/explore/nobackup/projects/3sl/data/Tappan/Tappan30_WV03_20211108_M1BS_1040010070C71D00_data.tif',
#    '/explore/nobackup/projects/3sl/data/Tappan/Tappan32_WV03_20191105_M1BS_10400100554AC400_data.tif'
#]

filenames = []
#for n in range(1, 34):
#    regex = glob(f'/explore/nobackup/projects/3sl/data/Tappan/Tappan{str(n).zfill(2)}*_data.tif')
#    filenames.append(regex[-1])

#filenames.append(glob(f'/explore/nobackup/projects/3sl/data/Tappan/Tappan{50}*_data.tif')[-1])
filenames.append(glob(f'/explore/nobackup/projects/3sl/data/Tappan/Tappan{30}*_data.tif')[-1])



for filename in filenames:

    print(filename)

    #tmp_output_dir = os.path.join(output_dir, Path(filename).stem)#.split('_')[0])
    tmp_output_dir = os.path.join(output_dir, (Path(filename).stem).split('_')[0])

    #if os.path.exists(tmp_output_dir):
    #    print(tmp_output_dir)
    #    print("skipping")
    #    continue

    os.makedirs(tmp_output_dir, exist_ok=True)

    # get boundary
    raster = rxr.open_rasterio(filename).rio.reproject("EPSG:4326")
    xx, yy = box(*raster.rio.bounds()).exterior.coords.xy
    image_bounds = [[x, y] for x, y in zip(xx, yy)]
    region = ee.Geometry.Polygon(image_bounds)

    # iterate over the years we need
    for year in range(2017, 2025, 1):

        for polarization in ['VV', 'VH']:

            try:
                output_filename = os.path.join(tmp_output_dir, f"{Path(filename).stem.split('_')[0]}-{polarization}-{year}.tif")
                if os.path.isfile(output_filename):
                    continue

                def compute_gee_power(image: ee.image.Image) -> ee.element.Element:
                    return ee.Image(10).pow(image.divide(10)).rename(polarization).copyProperties(image, ['system:time_start'])

                # get collection
                gee_image_collection = ee.ImageCollection('COPERNICUS/S1_GRD') \
                .filter(ee.Filter.eq('instrumentMode', 'IW')) \
                .filterBounds(region) \
                .select(polarization) \
                .filterDate(f'{year}-01-01', f'{year}-12-31')
                print('S1 ImageCollection: ' +f'{len(gee_image_collection.toBands().bandNames().getInfo())}')

                # compute power to normalize
                gee_image_collection = gee_image_collection.map(compute_gee_power)
                print('Processed logarithmic power for ' + f'{len(gee_image_collection.toBands().bandNames().getInfo())} bands')

                # get the median month sequence
                months = ee.List.sequence(1, 12)
                gee_image_collection = ee.ImageCollection.fromImages(
                months.map(
                    lambda month: gee_image_collection.filter(
                        ee.Filter.calendarRange(month, month, 'month')
                    ).median().set('month', month)
                    )
                )

                # clip the imagery again
                gee_image = gee_image_collection.toBands().clip(region)
                print('Processed monthly mean, resulted in ' + f'{len(gee_image.bandNames().getInfo())} bands')

                im = gd.mask.MaskedImage(gee_image)
                im.download(output_filename, region=region, crs='EPSG:32628', scale=10) # seengal 32628, ethiopia EPSG:32637
            except:
                continue
