#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pathlib import Path
from glob import glob

#for filename in glob('/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments/*_k80_n*.tif'):

"""
filenames = [
    #'/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments/Tappan32_WV03_20191105_M1BS_10400100551A5F00_data-sheperd_k80_n5000.tif',
    #'/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments/Tappan29_WV03_20211108_M1BS_1040010071B9E300_data-sheperd_k80_n5000.tif',
    #'/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments/Tappan19_WV02_20211006_M1BS_10300100C7242A00_data-sheperd_k80_n2000.tif',
    #'/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments/Tappan32_WV03_20191105_M1BS_10400100551A5F00_data-sheperd_k80_n2000.tif',
    #'/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments/Tappan29_WV03_20211108_M1BS_1040010071B9E300_data-sheperd_k80_n2000.tif',
    '/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments_v6/Tappan01_WV02_20231029_M1BS_10300100EDC20C00_data-sheperd_k60_n500.tif',
    '/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments_v6/Tappan05_WV03_20231031_M1BS_104001008C41A200_data-sheperd_k60_n1000.tif',
    '/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments_v6/Tappan06_WV03_20231024_M1BS_104001008CD42800_data-sheperd_k60_n1000.tif',
    '/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments_v6/Tappan19_WV02_20211006_M1BS_10300100C7242A00_data_sheperd_k60_n1000.tif',
    '/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments_v6/Tappan24_WV02_20231029_M1BS_10300100F0319100_data-sheperd_k60_n1000.tif',
    '/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments_v6/Tappan19_WV02_20210914_M1BS_10300100C645A500_data-sheperd_k60_n500.tif'
]
"""

filenames = glob('/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments_v6/Tappan19*.tif')


for filename in filenames:

    output_filename = '/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments_v6/'+ \
        f'{Path(filename).stem}.gpkg'
    if not os.path.exists(output_filename):
        os.system(f'python gdal_polygonize.py -f GPKG {filename} {output_filename}')

filenames = glob('/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments_v6/Tappan05*.tif')


for filename in filenames:

    output_filename = '/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments_v6/'+ \
        f'{Path(filename).stem}.gpkg'
    if not os.path.exists(output_filename):
        os.system(f'python gdal_polygonize.py -f GPKG {filename} {output_filename}')

filenames = glob('/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments_v6/Tappan06*.tif')


for filename in filenames:

    output_filename = '/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments_v6/'+ \
        f'{Path(filename).stem}.gpkg'
    if not os.path.exists(output_filename):
        os.system(f'python gdal_polygonize.py -f GPKG {filename} {output_filename}')

"""
from osgeo import ogr
from osgeo import gdal

#  get raster data source
open_image = gdal.Open( "/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments/Tappan22_WV02_20101108_M1BS_1030010007046300_data-sheperd_k80_n8000.tif" )
input_band = open_image.GetRasterBand(1)

#  create output data source
output_shp = "Tappan22_WV02_20101108_M1BS_1030010007046300_data-sheperd_k80_n8000"
shp_driver = ogr.GetDriverByName("GPKG")

# create output file name
output_shapefile = shp_driver.CreateDataSource( output_shp + ".gpkg" )
new_shapefile = output_shapefile.CreateLayer(output_shp, srs = None )

gdal.Polygonize(input_band, None, new_shapefile, -1, [], callback=None)
new_shapefile.SyncToDisk()
"""