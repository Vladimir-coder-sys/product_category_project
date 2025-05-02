from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("ProductCategoryMatcher").getOrCreate()

products = spark.read.option("header", True).csv("data/products.csv")
categories = spark.read.option("header", True).csv("data/categories.csv")
product_category = spark.read.option("header", True).csv("data/product_category.csv")

# Join all together: Products -> ProductCategory -> Categories
joined = products.join(product_category, "product_id", "left") \
    .join(categories, "category_id", "left")

# Select required fields
result = joined.select("product_name", "category_name")

# Show results
result.show()

# Find products without category
no_category = result.filter(col("category_name").isNull()).select("product_name").distinct()
print("Products without categories:")
no_category.show()
