import base64

from botocore.exceptions import NoCredentialsError, ClientError
from minio import Minio
from minio.deleteobjects import DeleteObject
from minio.error import S3Error
from minio.helpers import ObjectWriteResult
from django.conf import settings
from django.core.files.base import ContentFile
from core.services.storages.cloud.core import CloudStorageServiceInterface


class MinioExportService(CloudStorageServiceInterface):
    """
    Configured from settings.EXPORT_SERVICE
    """

    GET = "GET"
    PUT = "PUT"

    def upload_file(
        cls, key, file_path=None, headers=None, binary=False, metadata=None
    ):  # pylint: disable=too-many-arguments
        """Uploads file object"""
        read_directive = "rb" if binary else "r"
        file_path = file_path if file_path else key
        return cls._upload(key, open(file_path, read_directive), headers, metadata)

    def upload_base64(  # pylint: disable=too-many-arguments,inconsistent-return-statements
        cls,
        doc_base64,
        file_name,
        append_extension=True,
        public_read=False,
        headers=None,
    ):
        """Uploads via base64 content with file name"""
        _format = None
        _doc_string = None
        try:
            _format, _doc_string = doc_base64.split(";base64,")
        except:  # pylint: disable=bare-except # pragma: no cover
            pass

        if not _format or not _doc_string:  # pragma: no cover
            return

        if append_extension:
            file_name_with_ext = file_name + "." + _format.split("/")[-1]
        else:
            if file_name and file_name.split(".")[-1].lower() not in [
                "pdf",
                "jpg",
                "jpeg",
                "bmp",
                "gif",
                "png",
            ]:
                file_name += ".jpg"
            file_name_with_ext = file_name

        doc_data = ContentFile(base64.b64decode(_doc_string))
        if public_read:
            cls._upload_public(file_name_with_ext, doc_data)
        else:
            cls._upload(file_name_with_ext, doc_data, headers)

        return file_name_with_ext

    def url_for(cls, file_path):
        return cls._generate_signed_url(cls.GET, file_path) if file_path else None

    def public_url_for(cls, file_path):
        url = f"http://s3.health.go.ke/{settings.AWS_STORAGE_BUCKET_NAME}/{file_path}"
        if settings.ENV != "development":
            url = url.replace("http://", "https://")
        return url

    def exists(cls, key):
        try:
            resp = cls._conn().stat_object(settings.AWS_STORAGE_BUCKET_NAME, key)
            return True
        except S3Error:
            return False

    def has_path(self, prefix="/", delimiter="/"):
        return len(self.__fetch_keys(prefix, delimiter)) > 0

    def rename(cls, old_key, new_key, delete=False):  # pragma: no cover
        try:
            client = cls._conn()
            client.copy_object(settings.AWS_STORAGE_BUCKET_NAME, new_key, old_key)
            if delete:
                cls.delete_objects(old_key)
        except (ClientError, NoCredentialsError):
            return False

        return True

    def delete_objects(cls, path):  # pragma: no cover
        try:
            client = cls._conn()
            keys = cls.__fetch_keys(prefix=path)
            if keys:
                objects_to_delete = map(
                    lambda x: DeleteObject(x),
                    keys,
                )
                return client.remove_objects(
                    settings.AWS_STORAGE_BUCKET_NAME, objects_to_delete
                )
        except:  # pylint: disable=bare-except
            pass

    def remove(cls, key):
        try:
            client = cls._conn()
            return client.remove_object(settings.AWS_STORAGE_BUCKET_NAME, key)
        except S3Error:  # pragma: no cover
            pass

        return None

    @staticmethod
    def _conn(cls):
        return MinioExportService._session()

    def __get_connection(self):
        session = self.__session()
        return session

    @staticmethod
    def _session():
        return Minio(
            "s3.health.go.ke",
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY,
            secure=True if settings.ENV != "development" else False,
        )

    def _generate_signed_url(cls, accessor, key, metadata=None):
        try:
            _conn = cls._conn()
            return _conn.get_presigned_url(
                accessor,
                settings.AWS_STORAGE_BUCKET_NAME,
                key,
                extra_query_params=metadata,
            )
        except S3Error:  # pragma: no cover
            pass

        return None

    def _upload(cls, file_path, file, headers=None, metadata=None):
        """Uploads via file content with file_path as path + name"""
        client = cls._conn()
        file_size = len(file.read())
        file.seek(0)
        result: ObjectWriteResult = client.put_object(
            settings.AWS_STORAGE_BUCKET_NAME,
            file_path,
            file,
            file_size,
            headers.get("content-type", "application/octet-stream"),
            metadata=metadata,
        )
        return result.location

    def _upload_public(cls, file_path, file_content: ContentFile):
        try:
            client = cls._conn()
            return client.put_object(
                settings.AWS_STORAGE_BUCKET_NAME,
                file_path,
                file_content,
                length=file_content.size,
                metadata={"ACL": "public-read"},
            )
        except S3Error as e:  # pragma: no cover
            print(e)
            pass

        return None

    def __fetch_keys(cls, prefix="/", delimiter="/"):  # pragma: no cover
        prefix = prefix[1:] if prefix.startswith(delimiter) else prefix
        client = cls._conn()
        objects = client.list_objects(settings.AWS_STORAGE_BUCKET_NAME, prefix=prefix)
        return [obj.object_name for obj in objects]
