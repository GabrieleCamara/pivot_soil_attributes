# Vector layer
vlayer = iface.activeLayer()

# -- Adding stats mean to vector layer -- #
# Adding a new column in attribute table
provider = vlayer.dataProvider()
raster_mean = QgsField("clay_mean", QVariant.Double)
provider.addAttributes([raster_mean])
vlayer.updateFields()

# Raster layer
fn = 'C:/Users/EHDGZ/outlier_detection/br_clay_content_0-5cm_pred_g_kg.tif'
rlayer = iface.addRasterLayer(fn, '')

#Variar pivot id para selecionar diferentes feições
count_pivot = 1
while count_pivot <= 21040:
    vlayer.selectByExpression('"PIVOTID"=\'%s\'' %count_pivot,QgsVectorLayer.SetSelection)
    selection = vlayer.selectedFeatures()
    print(count_pivot)
    uri = "Polygon?crs=epsg:4326&index=yes"
    vl = QgsVectorLayer(uri, "temp_vlayer_%s" %count_pivot,  "memory")
    pr = vl.dataProvider()
    pr.addFeatures(vlayer.selectedFeatures())
    vl.updateExtents()
#    QgsProject.instance().addMapLayer(vl)
    alg_params = {
        'ALPHA_BAND': False,
        'CROP_TO_CUTLINE': True,
        'DATA_TYPE': 0,
        'EXTRA': '',
        'INPUT': rlayer,
        'KEEP_RESOLUTION': True,
        'MASK': vl,
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
    new_rlayer = QgsRasterLayer(result['OUTPUT'], 'OutputFile_%s' %count_pivot)
    # Adding the new raster layer in QGIS
#    QgsProject.instance().addMapLayer(new_rlayer)
    
#    # -- Mean of a raster attributes -- #
    stats = new_rlayer.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
    stats_mean = stats.mean
    print(stats_mean)

    # Updating the new field for each feature
    idx = provider.fieldNameIndex('clay_mean')
    for feature in selection:
        attrs = {idx : float(stats_mean)}
        vlayer.dataProvider().changeAttributeValues({feature.id() : attrs})
    
    count_pivot += 1
    
vlayer.removeSelection()