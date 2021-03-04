from rest_framework import serializers

from pulp_container.app import models as container_models
from pulpcore.plugin import models as core_models

from galaxy_ng.app import models
from galaxy_ng.app.access_control.fields import GroupPermissionField


class ContainerRepositorySerializer(serializers.ModelSerializer):
    pulp = serializers.SerializerMethodField()
    groups = GroupPermissionField()
    namespace = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    # This serializer is purposfully refraining from using pulp fields directly
    # in the top level response body. This is because future versions of hub will have to
    # support indexing other registries and the API responses for a container
    # repository should make sense for containers hosted by pulp and containers
    # hosted by other registries.
    class Meta:
        model = models.ContainerDistribution
        fields = (
            'id',
            'name',
            'groups',

            # this field will return null on instances where hub is indexing a
            # different repo
            'pulp',
            'namespace',
            'description',
            'created',
            'updated'
        )

    def get_id(self, distro):
        return distro.pulp_id

    def get_created(self, distro):
        return distro.repository.pulp_created

    def get_updated(self, distro):
        return distro.repository.pulp_last_updated

    def get_namespace(self, distro):
        return distro.namespace.name

    def get_pulp(self, distro):
        repo = distro.repository

        return {
            'repository':
            {
                'pulp_id': repo.pulp_id,
                'pulp_type': repo.pulp_type,
                'version': repo.latest_version().number,
                'name': repo.name,
                'description': repo.description,
                'pulp_created': repo.pulp_created,
            },
            'distribution':
            {
                'pulp_id': distro.pulp_id,
                'name': distro.name,
                'pulp_created': distro.pulp_created,
                'base_path': distro.base_path,
            }
        }


class ContainerRepositoryImageSerializer(serializers.ModelSerializer):
    config_blob = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    layers = serializers.SerializerMethodField()

    class Meta:
        model = container_models.Manifest
        fields = (
            'pulp_id',
            'digest',
            'schema_version',
            'media_type',
            'config_blob',
            'tags',
            'pulp_created',
            'layers'
        )

    def get_layers(self, obj):
        layers = []
        # use the prefetched blob_list and artifact_list instead of obj.blobs and
        # blob._artifacts to cut down on queries made.
        for blob in obj.blob_list:
            layers.append({
                'digest': blob.digest,
                'size': blob.artifact_list[0].size
            })

        return layers

    def get_config_blob(self, obj):
        return {
            'digest': obj.config_blob.digest,
            'media_type': obj.config_blob.media_type
        }

    def get_tags(self, obj):
        tags = []
        # tagget_manifests returns all tags on the manifest, not just the ones
        # that are in the latest version of the repo.
        for tag in obj.tagged_manifests.all():
            tags.append(tag.name)

        return tags


class ContainerRepositoryHistorySerializer(serializers.ModelSerializer):
    added = serializers.SerializerMethodField()
    removed = serializers.SerializerMethodField()

    class Meta:
        model = core_models.RepositoryVersion
        fields = (
            'pulp_id',
            'added',
            'removed',
            'pulp_created',
            'number'
        )

    def get_added(self, obj):
        added = []
        for content in obj.added_memberships.all():
            added.append(self._content_info(content.content))

        return added

    def get_removed(self, obj):
        removed = []
        for content in obj.removed_memberships.all():
            removed.append(self._content_info(content.content))

        return removed

    def _content_info(self, content):
        return_data = {
            "pulp_id": content.pulp_id,
            "pulp_type": content.pulp_type,
            "manifest_digest": None,
            "tag_name": None,
        }

        # TODO: Figure out if there is a way to prefetch Manifest and Tag objects
        if content.pulp_type == 'container.manifest':
            manifest = container_models.Manifest.objects.get(pk=content.pulp_id)
            return_data['manifest_digest'] = manifest.digest
        elif content.pulp_type == 'container.tag':
            tag = container_models.Tag.objects.select_related('tagged_manifest')\
                .get(pk=content.pulp_id)
            return_data['manifest_digest'] = tag.tagged_manifest.digest
            return_data['tag_name'] = tag.name

        return return_data
