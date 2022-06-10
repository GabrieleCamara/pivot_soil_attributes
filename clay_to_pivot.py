# Vector layer
vlayer = iface.activeLayer()
# Raster layer
fn = 'C:/Users/EHDGZ/outlier_detection/br_clay_content_0-5cm_pred_g_kg.tif'
rlayer = iface.addRasterLayer(fn, '')

# -- Clip raster -- #
# Parameter algoritms of processing run
# EPSG must to be equal to raster layer 5880
alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': rlayer,
            'KEEP_RESOLUTION': True,
            'MASK': vlayer,
            'MULTITHREADING': False,
            'NODATA': 0,
            'OPTIONS': '',
            'SET_RESOLUTION': False,
            'SOURCE_CRS': 'ProjectCrs',
            'TARGET_CRS': 'ProjectCrs',
            'X_RESOLUTION': None,
            'Y_RESOLUTION': None,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
# Processing Clip raster by mask
result = processing.run('gdal:cliprasterbymasklayer', alg_params)
# Creating new raster layer
new_rlayer = QgsRasterLayer(result['OUTPUT'], 'OutputFile')
# Adding the new raster layer in QGIS
QgsProject.instance().addMapLayer(new_rlayer)

# -- Mean of a raster attributes -- #
stats = new_rlayer.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
stats_mean = stats.mean
print(stats_mean)
# -- Adding stats mean to vector layer -- #
# Adding a new column in attribute table
provider = vlayer.dataProvider()
raster_mean = QgsField("clay_mean", QVariant.Int)
provider.addAttributes([raster_mean])
vlayer.updateFields()

# Updating the new field for each feature
idx = provider.fieldNameIndex('clay_mean')
for feature in vlayer.getFeatures():
    attrs = {idx : int(stats_mean)}
    vlayer.dataProvider().changeAttributeValues({feature.id() : attrs})

