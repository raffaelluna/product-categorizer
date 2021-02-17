SEED = 10

TARGET = "category"

ALL_FEATURES = [
    "product_id",
    "seller_id",
    "query",
    "search_page",
    "position",
    "title",
    "concatenated_tags",
    "creation_date",
    "price",
    "weight",
    "express_delivery",
    "minimum_quantity",
    "view_counts",
    "order_counts",
    "category"
]

FEATURES_TO_DROP = [
    "product_id",
    "seller_id",
    "creation_date",
    "search_page",
    "position",
    "view_counts",
    "order_counts"
]

FEATURES_TO_SCALE = [
    "price",
    "weight",
    "minimum_quantity"
]

FEATURES_TO_NORMALIZE = [
    "query",
    "title",
    "concatenated_tags"
]