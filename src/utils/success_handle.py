from src.utils.logging_handle import get_logger


def success_return(result: bool, message: str, client: str, **kwargs):
    logger = get_logger(__name__)
    # logger.info(client.host+":"+str(client.port) + ": " + message)
    # logger.info("{}:{}: {}".format(client.host, client.port, message))
    res = {
        "result": result,
        "message": message,
    }
    for key, value in kwargs.items():
        res[key] = value
    # print(res)
    return res
