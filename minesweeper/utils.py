stats_pb_conditions = {
    "tbv": lambda x, y: x > y,
    "tbv_per_second": lambda x, y: x > y,
    "ios": lambda x, y: x > y,
    "rqp": lambda x, y: x < y,
}
