import logging
import time

import requests


logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self, base_url):
        self.url = base_url.rstrip("/")

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.url}/{endpoint.lstrip('/')}"
        timeout = kwargs.pop("timeout", 10)

        logger.info("%s %s", method.upper(), url)

        start_time = time.perf_counter()

        try:
            response = requests.request(
                method=method,
                url=url,
                timeout=timeout,
                **kwargs,
            )

            duration = (time.perf_counter() - start_time) * 1000

            logger.info(
                "Response: status=%s, duration=%.2fms",
                response.status_code,
                duration,
            )

            return response

        except requests.RequestException:
            duration = (time.perf_counter() - start_time) * 1000

            logger.exception(
                "Request failed: method=%s, url=%s, duration=%.2fms",
                method.upper(),
                url,
                duration,
            )

            raise

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)