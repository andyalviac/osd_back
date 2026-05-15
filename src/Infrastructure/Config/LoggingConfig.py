import logging
import colorlog

def setup_logging(level=logging.INFO):
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s:%(name)s:%(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    ))

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    logging.getLogger("ariadne").setLevel(logging.CRITICAL)
    
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("azure.monitor.opentelemetry").setLevel(logging.WARNING)
    logging.getLogger("azure.monitor.opentelemetry.exporter").setLevel(logging.WARNING)
    logging.getLogger(
        "azure.monitor.opentelemetry.exporter.export._base"
    ).setLevel(logging.CRITICAL)