#!/opt/anaconda/envs/env_ewf_satcen_03_01_01/bin/python

import cioppy
import subprocess
import gdal
import osr
import ogr
import subprocess
from shapely.geometry import box

ciop = cioppy.Cioppy()

def log_input(reference):
    """
    Just logs the input reference, using the ciop.log function
    """

    ciop.log('INFO', 'processing input: ' + reference)
    
def pass_next_node(input):
    """
    Pass the input reference to the next node as is, without storing it on HDFS
    """

    ciop.publish(input, mode='silent')

def group_analysis(df):
    df['ordinal_type'] = 'NaN'
    slave_date=df['startdate'].min()[:10]
    master_date=df['startdate'].max()[:10]
    for i in range(len(df)):
    
        if slave_date == df.iloc[i]['startdate'][:10]:
            df.loc[i,'ordinal_type']='Pre'
    
        elif master_date == df.iloc[i]['startdate'][:10]:
            df.loc[i,'ordinal_type']='Pst'

    return 



def cog(input_tif, output_tif, band=None):
    
    if band is not None:
        translate_options = gdal.TranslateOptions(gdal.ParseCommandLine('-co TILED=YES ' \
                                                                        '-co COPY_SRC_OVERVIEWS=YES ' \
                                                                        '-co BIGTIFF=YES ' \
                                                                        '-co COMPRESS=LZW ' \
                                                                        '-ot Float32 ' \
                                                                        '-b {}'.format(band)))
    else:
        translate_options = gdal.TranslateOptions(gdal.ParseCommandLine('-co TILED=YES ' \
                                                                        '-co COPY_SRC_OVERVIEWS=YES ' \
                                                                        '-co BIGTIFF=YES ' \
                                                                        '-co COMPRESS=LZW ' \
                                                                        '-ot Float32 ' \
                                                                        '-b 1 -b 2 -b 3'))

    ds = gdal.Open(input_tif, gdal.OF_READONLY)

    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
    ds.BuildOverviews('NEAREST', [2,4,8,16,32])
    
    ds = None

    ds = gdal.Open(input_tif)
    gdal.Translate(output_tif,
                   ds, 
                   options=translate_options)
    ds = None

    #os.remove('{}.ovr'.format(input_tif))
    #os.remove(input_tif)
                                                  


def COG_merge(first, second, third, out_file):

    ps = subprocess.Popen(
        ['gdal_merge.py', '-o', out_file,
         #'-of', 'GTiff',
         first, second, third],
        stdout=subprocess.PIPE
    )
    output = ps.communicate()[0]
    for line in output.splitlines():
        ciop.log('INFO',line)
                                                  
# Modified the function to accept the img either if does NOT have Projection
def get_image_wkt(product):
    
    src = gdal.Open(product)
    ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()

    max_x = ulx + (src.RasterXSize * xres)
    min_y = uly + (src.RasterYSize * yres)
    min_x = ulx 
    max_y = uly
    if src.GetProjection()=='':
        result_wkt = box(min_x, min_y, max_x, max_y).wkt
    else:
        source = osr.SpatialReference()
        source.ImportFromWkt(src.GetProjection())

        target = osr.SpatialReference()
        target.ImportFromEPSG(4326)

        transform = osr.CoordinateTransformation(source, target)

        result_wkt = box(transform.TransformPoint(min_x, min_y)[0],
                     transform.TransformPoint(min_x, min_y)[1],
                     transform.TransformPoint(max_x, max_y)[0],
                     transform.TransformPoint(max_x, max_y)[1]).wkt
    
    return result_wkt
