import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrameCollection
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

def remove_unnecessary_text(team):
        return team.split(sep="(")[0]

# Script generated for node Custom Transform
def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
    
    df = dfc.select(list(dfc.keys())[0]).toDF()
    remove_unnecessary_text_udf = udf(remove_unnecessary_text, StringType())
    df_transformed = df.withColumn("time", remove_unnecessary_text_udf("time"))
    
    dyf_filtered = DynamicFrame.fromDF(df_transformed, glueContext, "remove_unnecessary_text")
    return DynamicFrameCollection({"CustomTransform0": dyf_filtered}, glueContext)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1711576375740 = glueContext.create_dynamic_frame.from_catalog(
    database="brasileirao-raw-database",
    table_name="rankings_csv",
    transformation_ctx="AWSGlueDataCatalog_node1711576375740",
)

# Script generated for node Custom Transform
CustomTransform_node1711576504392 = MyTransform(
    glueContext,
    DynamicFrameCollection(
        {"AWSGlueDataCatalog_node1711576375740": AWSGlueDataCatalog_node1711576375740},
        glueContext,
    ),
)

# Script generated for node Select From Collection
SelectFromCollection_node1711578354677 = SelectFromCollection.apply(
    dfc=CustomTransform_node1711576504392,
    key=list(CustomTransform_node1711576504392.keys())[0],
    transformation_ctx="SelectFromCollection_node1711578354677",
)

# Script generated for node Amazon S3
AmazonS3_node1711578395416 = glueContext.write_dynamic_frame.from_options(
    frame=SelectFromCollection_node1711578354677,
    connection_type="s3",
    format="csv",
    connection_options={
        "path": "s3://brasileirao-output",
        "compression": "gzip",
        "partitionKeys": [],
    },
    transformation_ctx="AmazonS3_node1711578395416",
)

job.commit()
