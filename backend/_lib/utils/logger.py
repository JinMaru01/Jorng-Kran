import logging, os, json
from datetime import datetime

LOG_DIR = "log"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("traffic_logger")
logger.setLevel(logging.INFO)

date_str = datetime.now().strftime("%Y-%m-%d")
log_filename = f"mlflow_traffic_{date_str}.log"
log_filepath = os.path.join(LOG_DIR, log_filename)

class FlatLogFormatter(logging.Formatter):
    def format(self, record):
        dt = datetime.fromtimestamp(record.created)
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S") + f":{int(record.msecs):03d}"
        pid = record.process
        level = record.levelname

        try:
            message_obj = json.loads(record.getMessage())
        except Exception:
            message_obj = {"message": str(record.getMessage())}

        msg_parts = [f"[ {timestamp} ] [ {pid} ] [{level}]"]

        msg_data = message_obj.get("message", {})
        user = msg_data.get("user", "unknown")
        request = msg_data.get("request", {})
        response = msg_data.get("response", {})

        # Flatten request
        msg_parts.append(f"User: {user}")
        msg_parts.append(f"Method: {request.get('method')}")
        msg_parts.append(f"URL: {request.get('url')}")
        msg_parts.append(f"QueryParams: {request.get('query_params')}")
        msg_parts.append(f"RequestHeaders: {request.get('headers')}")
        msg_parts.append(f"RequestBody: {request.get('body')}")

        # Flatten response
        msg_parts.append(f"StatusCode: {response.get('status_code')}")
        msg_parts.append(f"ResponseHeaders: {response.get('headers')}")
        msg_parts.append(f"ResponseBody: {response.get('body')}")

        return " | ".join(msg_parts)

handler = logging.FileHandler(log_filepath, encoding="utf-8")
handler.setFormatter(FlatLogFormatter())
logger.addHandler(handler)