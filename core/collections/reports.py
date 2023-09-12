from core.collections.models import Collection, Expansion, CollectionReference
from core.common.constants import HEAD
from core.reports.models import AbstractReport


class CollectionReport(AbstractReport):
    queryset = Collection.objects.filter(version=HEAD)
    name = 'Collections'
    select_related = ['created_by', 'organization', 'user']
    verbose_fields = [
        'mnemonic',
        'name',
        'collection_type',
        'public_access',
        'created_by.username',
        'created_at',
        'parent_resource_type',
        'parent_resource',
        'canonical_url',
        'custom_validation_schema'
    ]
    VERBOSE_HEADERS = [
        "ID",
        "Name",
        "Collection Type",
        "Public Access",
        "Created By",
        "Created At",
        "Owner Type",
        "Owner",
        "Canonical URL",
        "Validation Schema"
    ]


class CollectionVersionReport(AbstractReport):
    queryset = Collection.objects.exclude(version=HEAD)
    name = 'Collection Versions'
    select_related = ['created_by']
    verbose_fields = [
        'version',
        'versioned_object_url',
        'created_by.username',
        'created_at',
        'released'
    ]
    VERBOSE_HEADERS = [
        "Version",
        "Collection URL",
        "Created By",
        "Created At",
        "Released"
    ]


class ExpansionReport(AbstractReport):
    queryset = Expansion.objects.filter()
    name = 'Expansions'
    verbose = False


class ReferenceReport(AbstractReport):
    queryset = CollectionReference.objects.filter()
    name = 'References'
    grouped_label = "New References"
    verbose = False
    grouped = True
    GROUPED_HEADERS = [
        "Resource Type",
        "Static during Period",
        "Dynamic during Period",
        "Subtotal during Period",
        "Total as of Report Date"
    ]

    @property
    def grouped_queryset(self):
        if not self.queryset.exists():
            return []
        concepts_queryset = self.queryset.filter(reference_type='concepts')
        mappings_queryset = self.queryset.filter(reference_type='mappings')
        total_concepts = concepts_queryset.count()
        total_mappings = mappings_queryset.count()
        static_criteria = CollectionReference.get_static_references_criteria()
        total_static_concepts = concepts_queryset.filter(static_criteria).count()
        total_static_mappings = mappings_queryset.filter(static_criteria).count()
        overall_report = self.get_overall_report_instance()
        overall_concepts = overall_report.queryset.filter(reference_type='concepts')
        overall_mappings = overall_report.queryset.filter(reference_type='mappings')
        return [
            [
                'Concepts',
                total_static_concepts,
                total_concepts - total_static_concepts,
                total_concepts,
                overall_concepts.count()
            ],
            [
                'Mappings',
                total_static_mappings,
                total_mappings - total_static_mappings,
                total_mappings,
                overall_mappings.count()
            ]
        ]

    @staticmethod
    def to_grouped_stat_csv_row(obj):
        return [*obj]

    @property
    def retired(self):
        return 0

    @property
    def active(self):
        return self.count