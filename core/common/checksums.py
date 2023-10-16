import json
import hashlib
from uuid import UUID

from django.conf import settings
from django.db import models
from pydash import get

from core.common.utils import generic_sort
from core.toggles.models import Toggle


class ChecksumModel(models.Model):
    class Meta:
        abstract = True

    checksums = models.JSONField(null=True, blank=True, default=dict)

    CHECKSUM_EXCLUSIONS = []
    CHECKSUM_INCLUSIONS = []
    STANDARD_CHECKSUM_KEY = 'standard'
    SMART_CHECKSUM_KEY = 'smart'
    CHECKSUM_TYPES = {STANDARD_CHECKSUM_KEY}
    STANDARD_CHECKSUM_TYPES = {STANDARD_CHECKSUM_KEY}

    def get_checksums(self, standard=False, queue=False):
        if Toggle.get('CHECKSUMS_TOGGLE'):
            if self.checksums and self.has_checksums(standard):
                return self.checksums
            if queue:
                self.queue_checksum_calculation()
                return self.checksums or {}
            if standard:
                self.set_standard_checksums()
            else:
                self.set_checksums()

            return self.checksums
        return None

    def queue_checksum_calculation(self):
        from core.common.tasks import calculate_checksums
        if get(settings, 'TEST_MODE', False):
            calculate_checksums(self.__class__.__name__, self.id)
            self.refresh_from_db()
        else:
            calculate_checksums.delay(self.__class__.__name__, self.id)

    def set_specific_checksums(self, checksum_type, checksum):
        self.checksums = self.checksums or {}
        self.checksums[checksum_type] = checksum
        self.save(update_fields=['checksums'])

    def has_checksums(self, standard=False):
        return self.has_standard_checksums() if standard else self.has_all_checksums()

    def has_all_checksums(self):
        return set(self.checksums.keys()) - set(self.CHECKSUM_TYPES) == set()

    def has_standard_checksums(self):
        return set(self.checksums.keys()) - set(self.STANDARD_CHECKSUM_TYPES) == set()

    def set_checksums(self):
        if Toggle.get('CHECKSUMS_TOGGLE'):
            self.checksums = self._calculate_checksums()
            self.save(update_fields=['checksums'])

    def set_standard_checksums(self):
        if Toggle.get('CHECKSUMS_TOGGLE'):
            self.checksums = self.get_standard_checksums()
            self.save(update_fields=['checksums'])

    @property
    def checksum(self):
        """Returns the checksum of the model instance or standard only checksum."""
        if Toggle.get('CHECKSUMS_TOGGLE'):
            if get(self, f'checksums.{self.STANDARD_CHECKSUM_KEY}'):
                return self.checksums[self.STANDARD_CHECKSUM_KEY]
            self.get_checksums()

            return self.checksums.get(self.STANDARD_CHECKSUM_KEY)
        return None

    def get_checksum_fields(self):
        return {field: getattr(self, field) for field in self.CHECKSUM_INCLUSIONS}

    def get_standard_checksum_fields(self):
        return self.get_checksum_fields()

    def get_smart_checksum_fields(self):
        return {}

    def get_standard_checksums(self):
        if Toggle.get('CHECKSUMS_TOGGLE'):
            checksums = {}
            if self.STANDARD_CHECKSUM_KEY:
                checksums[self.STANDARD_CHECKSUM_KEY] = self._calculate_standard_checksum()
            return checksums
        return None

    def get_all_checksums(self):
        if Toggle.get('CHECKSUMS_TOGGLE'):
            checksums = {}
            if self.STANDARD_CHECKSUM_KEY:
                checksums[self.STANDARD_CHECKSUM_KEY] = self._calculate_standard_checksum()
            if self.SMART_CHECKSUM_KEY:
                checksums[self.SMART_CHECKSUM_KEY] = self._calculate_smart_checksum()
            return checksums
        return None

    @staticmethod
    def generate_checksum(data):
        return Checksum.generate(data)

    @staticmethod
    def generate_queryset_checksum(queryset, standard=False):
        _checksums = []
        for instance in queryset:
            instance.get_checksums(standard)
            _checksums.append(instance.checksum)
        if len(_checksums) == 1:
            return _checksums[0]
        return ChecksumModel.generate_checksum(_checksums)

    def _calculate_standard_checksum(self):
        fields = self.get_standard_checksum_fields()
        return None if fields is None else self.generate_checksum(fields)

    def _calculate_smart_checksum(self):
        fields = self.get_smart_checksum_fields()
        return self.generate_checksum(fields) if fields else None

    def _calculate_checksums(self):
        return self.get_all_checksums()


class Checksum:
    @classmethod
    def generate(cls, obj, hash_algorithm='MD5'):
        # hex encoding is used to make the hash more readable
        serialized_obj = cls._serialize(obj).encode('utf-8')
        hash_func = hashlib.new(hash_algorithm)
        hash_func.update(serialized_obj)

        return hash_func.hexdigest()

    @classmethod
    def _serialize(cls, obj):
        if isinstance(obj, list) and len(obj) == 1:
            obj = obj[0]
        if isinstance(obj, list):
            return f"[{','.join(map(cls._serialize, generic_sort(obj)))}]"

        if isinstance(obj, dict):
            keys = generic_sort(obj.keys())
            acc = f"{{{json.dumps(keys)}"
            for key in keys:
                acc += f"{cls._serialize(obj[key])},"
            return f"{acc}}}"
        if isinstance(obj, UUID):
            return json.dumps(str(obj))
        return json.dumps(obj)
