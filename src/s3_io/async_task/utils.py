import logging


async def read_stream(stream, logger: logging.Logger, is_error=False):
    while True:
        line = await stream.readline()
        if not line:
            break
        decoded = line.decode().strip()
        if is_error:
            logger.error(f"{decoded}")
        else:
            logger.info(f"{decoded}")
