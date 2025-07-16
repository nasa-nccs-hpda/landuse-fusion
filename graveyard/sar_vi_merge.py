import os
import rsgislib
from rsgislib import zonalstats
from glob import glob
import numpy as np
from pathlib import Path
from rsgislib import vectorutils

import os
os.environ['USE_PYGEOS'] = '0'

import geopandas as gpd


def read_vec_obj(vec_file):
    print("Reading vector into memory...")
    vec_lyr = rsgislib.vectorutils.get_vec_lyrs_lst(vec_file)[0]
    ogr_dataset, ogr_layer = rsgislib.vectorutils.read_vec_lyr_to_mem(vec_file, vec_lyr)

    return ogr_layer, ogr_dataset, vec_lyr

def populate_vec_segs(vec_mem_obj, sar_img, months, polarization):
    for i in range(len(months)):

        pol = polarization.lower()
        year = Path(sar_img).stem.split('-')[-1]

        print(pol, year)

        median_field_name = "_".join([pol, months[i], year, "med"])
        min_field_name = "_".join([pol, months[i], year, "min"])
        max_field_name = "_".join([pol, months[i], year, "max"])
        mean_field_name = "_".join([pol, months[i], year, "mean"])
        stddev_field_name = "_".join([pol, months[i], year, "stddev"])
        perc90_field_name = "_".join([pol, months[i], year, "perc90"])
        print("populating:", median_field_name, "band: ", i + 1, polarization)

        ogr_obj = vec_mem_obj
        sar_img = sar_img
        img_band = i + 1
        min_thresh = 0.00001
        max_thresh = 0.5
        out_no_data_val = 0.0

        zonalstats.calc_zonal_band_stats_test_poly_pts(
            vec_lyr_obj=ogr_obj,
            input_img=sar_img,
            img_band=img_band,
            min_thres=min_thresh,
            max_thres=max_thresh,
            out_no_data_val=out_no_data_val,
            median_field=median_field_name,
            percentile=90,
            percentile_field=perc90_field_name,
            min_field=min_field_name,
            max_field=max_field_name,
            mean_field=mean_field_name,
            stddev_field=stddev_field_name,
            sum_field=None,
            count_field=None,
            mode_field=None,
            vec_def_epsg=None,
        )

    return pol #ogr_obj


def write_vec_obj(vec_mem_obj, vec_file, vec_lyr, pol):
    # write vec_mem_obj to file
    print("writing mem obj to file...")
    vec_lyr_obj = vec_mem_obj
    print(vec_lyr_obj)
    out_vec_file = vec_file.replace('.gpkg','_pop4' + pol + '.gpkg')
    print(out_vec_file)
    out_vec_lyr = vec_lyr
    print(out_vec_lyr)
    out_format = "GPKG"
    rsgislib.vectorutils.write_vec_lyr_to_file(
        vec_lyr_obj, out_vec_file, out_vec_lyr, out_format
    )


months = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
]

"""
#sar_path = '/explore/nobackup/projects/3sl/labels/landuse/ethiopia_segmentation_experiments_v2'#Tappan21_WV02_20190119_M1BS_103001008B4CF000_data'
#vector_path = '/explore/nobackup/projects/3sl/labels/landuse/ethiopia_segmentation_experiments_v1'
sar_path = '/explore/nobackup/projects/3sl/data/SAR/S1_Monthly'
vector_path = '/explore/nobackup/projects/3sl/labels/landuse/v2_labels'

#for sar_dir in ['WV02_20210322_M1BS_10300100BB4AF500-toa_RayaAlamata', 'WV02_20210322_M1BS_10300100BB4AF500-toa_RayaKorem']:#os.listdir(sar_path):
for sar_dir in ['Tappan01', 'Tappan05', 'Tappan06', 'Tappan19', 'Tappan24']:

    print(sar_dir)

    vec_files = glob(os.path.join(vector_path, f'{sar_dir}*.gpkg'))
    print(vec_files)

    if len(vec_files) == 0:
        print("NO files")
        continue

    # taking one of the files in the list
    #vec_file = vec_file[5]

    for vec_file in vec_files:

        for polarization in ['VH', 'VV']:

            # get sar filenames
            sar_files = glob(os.path.join(sar_path, sar_dir, f'*-{polarization}-*.tif'))
            print(len(sar_files))

            # get vector filename
            output_vector = f'{Path(vec_file).with_suffix("")}-epsg.gpkg'
            if not os.path.isfile(output_vector):

                print(vec_file, f'{Path(vec_file).with_suffix("")}-epsg.gpkg')
                gdf = gpd.read_file(vec_file).to_crs('EPSG:32637')
                # print(gdf.shape, gdf.crs)
                gdf.to_file(output_vector, driver='GPKG')

            vec_mem_obj, ogr_layer, vec_lyr = read_vec_obj(output_vector)

            for sar_img in sar_files:
                #print(sar_img)
                #print(vec_file.replace('.gpkg','_pop' + polarization + '.gpkg'))
                pol = populate_vec_segs(vec_mem_obj, sar_img, months, polarization)

            write_vec_obj(vec_mem_obj, vec_file, vec_lyr, pol)
"""

"""
vec_file = '/explore/nobackup/projects/3sl/labels/landuse/segmentation_experiments/Tappan21_WV02_20190119_M1BS_103001008B4CF000_data-sheperd_k80_n8000-epsg.gpkg'


    for polarization in ['VH', 'VV']:

        sar_files = glob(os.path.join(output_dir, f'*-{polarization}-*.tif'))
        print(len(sar_files))

        #print(vec_file, f'{Path(vec_file).with_suffix("")}-epsg.gpkg')
        #gdf = gpd.read_file(vec_file).to_crs('EPSG:32628')
        #print(gdf.shape, gdf.crs)
        #gdf.to_file(f'{Path(vec_file).with_suffix("")}-epsg.gpkg', driver='GPKG')

        vec_mem_obj, ogr_layer, vec_lyr = read_vec_obj(vec_file)

        for sar_img in sar_files:
            #print(sar_img)
            #print(vec_file.replace('.gpkg','_pop' + polarization + '.gpkg'))
            pol = populate_vec_segs(vec_mem_obj, sar_img, months, polarization)

        write_vec_obj(vec_mem_obj, vec_file, vec_lyr, pol)
"""


#sar_path = '/explore/nobackup/projects/3sl/labels/landuse/ethiopia_segmentation_experiments_v2'#Tappan21_WV02_20190119_M1BS_103001008B4CF000_data'
#vector_path = '/explore/nobackup/projects/3sl/labels/landuse/ethiopia_segmentation_experiments_v1'
sar_path = '/explore/nobackup/projects/3sl/data/SAR/S1_Monthly_VIs'
vector_path = '/explore/nobackup/projects/3sl/labels/landuse/v3_objects'

#for sar_dir in ['WV02_20210322_M1BS_10300100BB4AF500-toa_RayaAlamata', 'WV02_20210322_M1BS_10300100BB4AF500-toa_RayaKorem']:#os.listdir(sar_path):
#for sar_dir in ['Tappan19', 'Tappan50', 'Tappan15', 'Tappan05', 'Tappan01', 'Tappan06', 'Tappan24', 'Tappan30', 'Tappan32']:
for sar_dir in ['Tappan05']: # running: Tappan01, Tappan06, Tappan24, Tappan05, Tappan50, Tappan19

    print(sar_dir)

    vec_files = glob(os.path.join(vector_path, sar_dir, f'{sar_dir}*-epsg.gpkg'))
    print(vec_files)

    if len(vec_files) == 0:
        print("NO files")
        continue

    # taking one of the files in the list
    #vec_file = vec_file[5]

    for vec_file in vec_files:

        for polarization in ['CPR', 'FDI', 'RFDI', 'RPI', 'RVI']:

            # get sar filenames
            sar_files = glob(os.path.join(sar_path, sar_dir, f'*-{polarization}-*.vrt'))
            print(len(sar_files))

            # get vector filename
            output_vector = f'{Path(vec_file).with_suffix("")}-sarvi-epsg-2.gpkg'
            if not os.path.isfile(output_vector):

                print(vec_file, f'{Path(vec_file).with_suffix("")}-sarvi-epsg-2.gpkg')
                gdf = gpd.read_file(vec_file).to_crs('EPSG:32628')
                # print(gdf.shape, gdf.crs)
                gdf.to_file(output_vector, driver='GPKG')

            vec_mem_obj, ogr_layer, vec_lyr = read_vec_obj(output_vector)

            for sar_img in sar_files:

                if sar_img.endswith('2024.vrt'):
                    print("LESS MONTHHHSHSHSHHSHS")
                    temp_months = months[:7]
                else:
                    temp_months = months
                #print(sar_img)
                #print(vec_file.replace('.gpkg','_pop' + polarization + '.gpkg'))
                pol = populate_vec_segs(vec_mem_obj, sar_img, temp_months, polarization)

            write_vec_obj(vec_mem_obj, vec_file, vec_lyr, pol)
