__author__ = 'dex'
from geo_pipeline.Gse import *
import glob, os

for filename in glob.glob('geo_mirror/DATA/SeriesMatrix/*'):
    gse_name = os.path.basename(filename)
    print gse_name
    gse = Gse(gse_name, doData=False)
    for gsm_name in gse.samples.index:
        gpl_name = gse.samples.ix[gsm_name].Sample_platform_id
        platform_rec = db(Platform.gpl_name == gpl_name).select().first() \
                       or Platform(Platform.insert(gpl_name=gpl_name))

        series_rec = db(Series.gse_name == gse_name).select().first() \
                     or Series(Series.insert(gse_name=gse_name))

        sample_rec = db((Sample.gsm_name == gsm_name) & \
                        (Sample.series_id == series_rec.id) & \
                        (Sample.platform_id == platform_rec.id)).select().first() \
                     or Sample(Sample.insert(gsm_name=gsm_name,
                                             series_id=series_rec.id,
                                             platform_id=platform_rec.id))
        attribute_name2value = gse.samples.ix[gsm_name].to_dict()
        for name in attribute_name2value:
            value = attribute_name2value[name]
            sample_attribute_rec = db((Sample_Attribute.sample_id == sample_rec.id) & \
                                      (Sample_Attribute.name == name)).select().first() \
                                   or Sample_Attribute(Sample_Attribute.insert(sample_id=sample_rec.id,
                                                                               name=name,
                                                                               value=value))
            # print sample_attribute_rec