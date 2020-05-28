from py_snap_helpers import *

def slice_assembly(input_prods): 
    snappy.GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    HashMap = snappy.jpy.get_type('java.util.HashMap')
    parameters = HashMap()
    slices = jpy.array('org.esa.snap.core.datamodel.Product', len(input_prods.index))
    for index, row in input_prods.iterrows(): 
        slices[index] = snappy.ProductIO.readProduct(row['local_path'])

    mosaic = snappy.GPF.createProduct('SliceAssembly', parameters, slices)

    return mosaic


def split_subswath_write_product(input_id, subswath, polarisation, output):
    snappy.GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    HashMap = snappy.jpy.get_type('java.util.HashMap')
    parameters = HashMap()
    parameters.put('subswath', subswath)
    parameters.put('selectedPolarisations', polarisation)
    #parameters.put('wktAoi', '----')
    product = snappy.GPF.createProduct('TOPSAR-Split', parameters, product)
    ProductIO.writeProduct(product, output, 'GeoTIFF-BigTIFF')
    return 
    