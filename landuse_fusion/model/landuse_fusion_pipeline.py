import os
import sys
import socket
import shapely
import rasterio
import geopandas as gpd

from glob import glob
from pathlib import Path
from itertools import repeat
from multiprocessing import Pool, cpu_count

try:
    import rsgislib
    from rsgislib.segmentation import shepherdseg
    from rsgislib.segmentation import tiledsegsingle
except ImportError:
    RGISLIB_AVAILABLE = False

# singularity exec --nv -B $NOBACKUP,/explore/nobackup/people,/explore/nobackup/projects \
#    /explore/nobackup/projects/ilab/containers/senegal-rsgislib python test_segmentation.py


class LandUseFusionPipeline():

    def __init__(self) -> None:
        pass

    def get_filenames(self, data_regex: str) -> list:
        """
        Get filename from list of regexes
        """
        # get the paths/filenames of the regex
        filenames = []
        if isinstance(data_regex, list):
            for regex in data_regex:
                filenames.extend(glob(regex))
        else:
            filenames = glob(data_regex)
        assert len(filenames) > 0, f'No files under {data_regex}'
        return sorted(filenames)

    def get_segmentation(self, segmentation_algorithm: str = 'sheperd'):

        # sheperd segmentation
        if segmentation_algorithm == 'sheperd':
            self.compute_sheperd_segmentation()

        return

    def get_segmentation_objects():
        return

    def get_sar_data():
        return

    def get_data_fusion():
        return

    def compute_sheperd_segmentation(
                self,
                filename: str,
                output_filename: str,
                num_clusters: int,
                min_n_pxls: int
            ):

        if not os.path.isfile(output_filename):
            shepherdseg.run_shepherd_segmentation(
            #tiledsegsingle.perform_tiled_segmentation(
                filename,
                output_filename,
                num_clusters=num_clusters,
                min_n_pxls=min_n_pxls,
                #minPxls=1000,
                #tile_width=1000,
                #tile_height=1000,
                #calc_stats=True,
                dist_thres=1000,
                gdalformat='GTiff',
                process_in_mem=True,
                tmp_dir='/explore/nobackup/projects/ilab/tmp'
            )
            #raster_to_vector(output_filename, output_filename.with_suffix('.gpkg'))
        return
    
    def compute_polygons(               
                self,
                filename: str,
                output_filename: str
            ):
        if not os.path.exists(output_filename):
            os.system(f'python gdal_polygonize.py -f GPKG {filename} {output_filename}')

def main():

    # This whole main will be removed at a later time and be
    # replaced with the CLI script.

    # define the landuse object
    landuse_fusion_pipeline = LandUseFusionPipeline()

    # TEMPORARY
    output_dir = '/explore/nobackup/projects/3sl/labels/landuse/agroforestry_segmentation_experiments_v1'
    os.makedirs(output_dir, exist_ok=True)

    num_clusters = 60 #80
    min_n_pxls = 500

    for filename in [
        #'/explore/nobackup/people/walemu/NRO/WV02_20210322_M1BS_10300100BB4AF500-toa_RayaAlamata.tif',
        #'/explore/nobackup/people/walemu/NRO/WV02_20210322_M1BS_10300100BB4AF500-toa_RayaKorem.tif',
        #'/explore/nobackup/people/walemu/NRO/WV03_20211209_M1BS_1040010072958B00-toa-sharpened_RayaKobo.tif'
        '/explore/nobackup/projects/3sl/data/Tappan/new_dates/Tappan50_WV02_20230217_M1BS_10300100E2591000.data.tif',
        '/explore/nobackup/projects/3sl/data/Tappan/new_dates/Tappan50_WV02_20230402_M1BS_10300100E49C3E00.data.tif',
        '/explore/nobackup/projects/3sl/data/Tappan/new_dates/Tappan50_WV02_20230709_M1BS_10300100EA3D0400.data.tif',
        '/explore/nobackup/projects/3sl/data/Tappan/new_dates/Tappan50_WV03_20221016_M1BS_104001007C8D5200.data.tif',
        '/explore/nobackup/projects/3sl/data/Tappan/new_dates/Tappan50_WV03_20230424_M1BS_1040010085159D00.data.tif',
        '/explore/nobackup/projects/3sl/data/Tappan/new_dates/Tappan50_WV03_20230424_M1BS_1040010085918900.data.tif',
        '/explore/nobackup/projects/3sl/data/Tappan/new_dates/Tappan50_WV03_20230620_M1BS_10400100864D0600.data.tif',
        '/explore/nobackup/projects/3sl/data/Tappan/new_dates/Tappan50_WV03_20230620_M1BS_1040010087D26800.data.tif'
    ]:

        # compute sheperd segmentation
        # TODO: add the arguments to the function
        output_filename_segmentation = os.path.join(
            output_dir,
            f'{Path(filename).stem}-sheperd_k{num_clusters}_n{min_n_pxls}.tif')
        landuse_fusion_pipeline.compute_sheperd_segmentation(
            filename,
            output_filename_segmentation,
            100,
            500
        )

        # polygonize
        output_filename_polygon = os.path.join(output_dir, f'{Path(filename).stem}.gpkg')
        landuse_fusion_pipeline.compute_polygons(
            output_filename_segmentation, output_filename_polygon)

    return

if __name__ == "__main__":
    sys.exit(main())