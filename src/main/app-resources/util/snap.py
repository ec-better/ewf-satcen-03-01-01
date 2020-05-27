from py_snap_helpers import *

def slice_assembly(input_prods): 
    HashMap = snappy.jpy.get_type('java.util.HashMap')
    
    slices = jpy.array('org.esa.snap.core.datamodel.Product', len(input_prods.index))
    for index, row in input_prods.iterrows(): 
        slices[index] = snappy.ProductIO.readProduct(row['local_path'])

    mosaic = snappy.GPF.createProduct('SliceAssembly', parameters, slices)
    #how to persist the output ... ciop-publish?
    return mosaic

