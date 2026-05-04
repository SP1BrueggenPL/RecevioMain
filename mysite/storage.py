import logging

from whitenoise.storage import CompressedManifestStaticFilesStorage

try:
    from whitenoise.storage import MissingFileError as WhiteNoiseMissingFileError
except ImportError:
    WhiteNoiseMissingFileError = None

logger = logging.getLogger(__name__)


class RelaxedManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False

    def post_process(self, *args, **kwargs):
        for result in super().post_process(*args, **kwargs):
            if (
                WhiteNoiseMissingFileError is not None
                and isinstance(result, tuple)
                and len(result) == 3
                and isinstance(result[2], WhiteNoiseMissingFileError)
            ):
                logger.warning("Static file reference could not be resolved: %s", result[2])
                yield result[0], result[1], True
            else:
                yield result
