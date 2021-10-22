# -*- coding: utf-8 -*- #
# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Database Migration Service connection profiles API."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from apitools.base.py import list_pager

from googlecloudsdk.api_lib.database_migration import api_util
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions as calliope_exceptions
from googlecloudsdk.command_lib.util.args import labels_util
from googlecloudsdk.core import exceptions as core_exceptions


class UnsupportedConnectionProfileDBTypeError(core_exceptions.Error):
  """Error raised when the connection profile database type is unsupported."""


class ConnectionProfilesClient(object):
  """Client for connection profiles service in the API."""

  def __init__(self, release_track):
    self._api_version = api_util.GetApiVersion(release_track)
    self.client = api_util.GetClientInstance(release_track)
    self.messages = api_util.GetMessagesModule(release_track)
    self._service = self.client.projects_locations_connectionProfiles
    self.resource_parser = api_util.GetResourceParser(release_track)
    self._release_track = release_track

  def _GetEngineFromCloudSql(self, cloudsql):
    """Gets the SQL engine from the Cloud SQL version.

    Args:
      cloudsql: Cloud SQL connection profile

    Returns:
      A string representing the SQL engine
    """
    if cloudsql.settings.databaseVersion:
      # Taking the DB engine from the version enum which is of the format:
      # <SQL_ENGINE>_<VERSION_NUMBER> e.g. MYSQL_5_6
      return '{}'.format(cloudsql.settings.databaseVersion).split('_')[0]
    else:
      return ''

  def GetEngineName(self, profile):
    """Gets the SQL engine name from the connection profile.

    Args:
      profile: the connection profile

    Returns:
      A string representing the SQL engine
    """
    try:
      if profile.mysql:
        return 'MYSQL'
      if profile.cloudsql:
        return self._GetEngineFromCloudSql(profile.cloudsql)
      # Make sure to add new engines at the end of the list to avoid the except
      # clause catching and skipping relevant cases for older/alpha versions
      if profile.postgresql:
        return 'POSTGRES'
      # TODO(b/178304949): Add SQL Server case once supported.
      return ''
    except AttributeError as _:
      # This exception is for Alpha/GA support since not all fields
      # exists in alpha class version - it causes an exception to access them.
      # This is the alternative for having a different impl. for each version.
      return ''

  def _ClientCertificateArgName(self):
    if self._api_version == 'v1alpha2':
      return 'certificate'
    return 'client_certificate'

  def _InstanceArgName(self):
    if self._api_version == 'v1alpha2':
      return 'instance'
    return 'cloudsql_instance'

  def _SupportsPostgresql(self):
    return self._release_track == base.ReleaseTrack.GA

  def _ValidateArgs(self, args):
    self._ValidateSslConfigArgs(args)

  def _ValidateSslConfigArgs(self, args):
    self._ValidateCertificateFormat(args, 'ca_certificate')
    self._ValidateCertificateFormat(args, self._ClientCertificateArgName())
    self._ValidateCertificateFormat(args, 'private_key')

  def _ValidateCertificateFormat(self, args, field):
    if not hasattr(args, field) or not args.IsSpecified(field):
      return True
    certificate = getattr(args, field)
    cert = certificate.strip()
    cert_lines = cert.split('\n')
    if (not cert_lines[0].startswith('-----')
        or not cert_lines[-1].startswith('-----')):
      raise calliope_exceptions.InvalidArgumentException(
          field,
          'The certificate does not appear to be in PEM format:\n{0}'
          .format(cert))

  def _GetSslConfig(self, args):
    return self.messages.SslConfig(
        clientKey=args.private_key,
        clientCertificate=args.GetValue(self._ClientCertificateArgName()),
        caCertificate=args.ca_certificate)

  def _UpdateMySqlSslConfig(self, connection_profile, args, update_fields):
    """Fills connection_profile and update_fields with MySQL SSL data from args."""
    if args.IsSpecified('ca_certificate'):
      connection_profile.mysql.ssl.caCertificate = args.ca_certificate
      update_fields.append('mysql.ssl.caCertificate')
    if args.IsSpecified('private_key'):
      connection_profile.mysql.ssl.clientKey = args.private_key
      update_fields.append('mysql.ssl.clientKey')
    if args.IsSpecified(self._ClientCertificateArgName()):
      connection_profile.mysql.ssl.clientCertificate = args.GetValue(
          self._ClientCertificateArgName())
      update_fields.append('mysql.ssl.clientCertificate')

  def _GetMySqlConnectionProfile(self, args):
    ssl_config = self._GetSslConfig(args)
    return self.messages.MySqlConnectionProfile(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        ssl=ssl_config,
        cloudSqlId=args.GetValue(self._InstanceArgName()))

  def _UpdateMySqlConnectionProfile(
      self, connection_profile, args, update_fields):
    """Updates MySQL connection profile."""
    if args.IsSpecified('host'):
      connection_profile.mysql.host = args.host
      update_fields.append('mysql.host')
    if args.IsSpecified('port'):
      connection_profile.mysql.port = args.port
      update_fields.append('mysql.port')
    if args.IsSpecified('username'):
      connection_profile.mysql.username = args.username
      update_fields.append('mysql.username')
    if args.IsSpecified('password'):
      connection_profile.mysql.password = args.password
      update_fields.append('mysql.password')
    if args.IsSpecified(self._InstanceArgName()):
      connection_profile.mysql.cloudSqlId = args.GetValue(
          self._InstanceArgName())
      update_fields.append('mysql.instance')
    self._UpdateMySqlSslConfig(connection_profile, args, update_fields)

  def _UpdatePostgreSqlSslConfig(self, connection_profile, args, update_fields):
    """Fills connection_profile and update_fields with PostgreSQL SSL data from args."""
    if args.IsSpecified('ca_certificate'):
      connection_profile.postgresql.ssl.caCertificate = args.ca_certificate
      update_fields.append('postgresql.ssl.caCertificate')
    if args.IsSpecified('private_key'):
      connection_profile.postgresql.ssl.clientKey = args.private_key
      update_fields.append('postgresql.ssl.clientKey')
    if args.IsSpecified(self._ClientCertificateArgName()):
      connection_profile.postgresql.ssl.clientCertificate = args.GetValue(
          self._ClientCertificateArgName())
      update_fields.append('postgresql.ssl.clientCertificate')

  def _GetPostgreSqlConnectionProfile(self, args):
    ssl_config = self._GetSslConfig(args)
    return self.messages.PostgreSqlConnectionProfile(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        ssl=ssl_config,
        cloudSqlId=args.GetValue(self._InstanceArgName()))

  def _UpdatePostgreSqlConnectionProfile(self, connection_profile, args,
                                         update_fields):
    """Updates PostgreSQL connection profile."""
    if args.IsSpecified('host'):
      connection_profile.postgresql.host = args.host
      update_fields.append('postgresql.host')
    if args.IsSpecified('port'):
      connection_profile.postgresql.port = args.port
      update_fields.append('postgresql.port')
    if args.IsSpecified('username'):
      connection_profile.postgresql.username = args.username
      update_fields.append('postgresql.username')
    if args.IsSpecified('password'):
      connection_profile.postgresql.password = args.password
      update_fields.append('postgresql.password')
    if args.IsSpecified(self._InstanceArgName()):
      connection_profile.postgresql.cloudSqlId = args.GetValue(
          self._InstanceArgName())
      update_fields.append('postgresql.instance')
    self._UpdatePostgreSqlSslConfig(connection_profile, args, update_fields)

  def _GetProvider(self, cp_type, provider):
    if provider is None:
      return cp_type.ProviderValueValuesEnum.DATABASE_PROVIDER_UNSPECIFIED
    return cp_type.ProviderValueValuesEnum.lookup_by_name(provider)

  def _GetActivationPolicy(self, cp_type, policy):
    if policy is None:
      return cp_type.ActivationPolicyValueValuesEnum.SQL_ACTIVATION_POLICY_UNSPECIFIED
    return cp_type.ActivationPolicyValueValuesEnum.lookup_by_name(policy)

  def _GetDatabaseVersion(self, cp_type, version):
    return cp_type.DatabaseVersionValueValuesEnum.lookup_by_name(version)

  def _GetAuthorizedNetworks(self, networks):
    acl_entry = self.messages.SqlAclEntry
    return [
        acl_entry(value=network)
        for network in networks
    ]

  def _GetIpConfig(self, args):
    return self.messages.SqlIpConfig(
        enableIpv4=args.enable_ip_v4,
        privateNetwork=args.private_network,
        requireSsl=args.require_ssl,
        authorizedNetworks=self._GetAuthorizedNetworks(args.authorized_networks)
    )

  def _GetDataDiskType(self, cp_type, data_disk_type):
    if data_disk_type is None:
      return  cp_type.DataDiskTypeValueValuesEnum.SQL_DATA_DISK_TYPE_UNSPECIFIED
    return cp_type.DataDiskTypeValueValuesEnum.lookup_by_name(data_disk_type)

  def _GetCloudSqlSettings(self, args):
    cp_type = self.messages.CloudSqlSettings
    source_id = args.CONCEPTS.source_id.Parse().RelativeName()
    user_labels_value = labels_util.ParseCreateArgs(
        args, cp_type.UserLabelsValue, 'user_labels')
    database_flags = labels_util.ParseCreateArgs(
        args, cp_type.DatabaseFlagsValue, 'database_flags')
    return self.messages.CloudSqlSettings(
        databaseVersion=self._GetDatabaseVersion(
            cp_type, args.database_version),
        userLabels=user_labels_value,
        tier=args.tier,
        storageAutoResizeLimit=args.storage_auto_resize_limit,
        activationPolicy=self._GetActivationPolicy(
            cp_type, args.activation_policy),
        ipConfig=self._GetIpConfig(args),
        autoStorageIncrease=args.auto_storage_increase,
        databaseFlags=database_flags,
        dataDiskType=self._GetDataDiskType(cp_type, args.data_disk_type),
        dataDiskSizeGb=args.data_disk_size,
        zone=args.zone,
        sourceId=source_id
    )

  def _GetCloudSqlConnectionProfile(self, args):
    settings = self._GetCloudSqlSettings(args)
    return self.messages.CloudSqlConnectionProfile(settings=settings)

  def _GetConnectionProfile(self, cp_type, connection_profile_id, args):
    """Returns a connection profile according to type."""
    connection_profile_type = self.messages.ConnectionProfile
    labels = labels_util.ParseCreateArgs(
        args, connection_profile_type.LabelsValue)
    params = {}
    if cp_type == 'MYSQL':
      mysql_connection_profile = self._GetMySqlConnectionProfile(args)
      params['mysql'] = mysql_connection_profile
      params['provider'] = self._GetProvider(connection_profile_type,
                                             args.provider)
    elif cp_type == 'CLOUDSQL':
      cloudsql_connection_profile = self._GetCloudSqlConnectionProfile(args)
      params['cloudsql'] = cloudsql_connection_profile
      params['provider'] = self._GetProvider(connection_profile_type,
                                             args.provider)
    elif cp_type == 'POSTGRESQL':
      postgresql_connection_profile = self._GetPostgreSqlConnectionProfile(args)
      params['postgresql'] = postgresql_connection_profile
    return connection_profile_type(
        name=connection_profile_id,
        labels=labels,
        state=connection_profile_type.StateValueValuesEnum.CREATING,
        displayName=args.display_name,
        **params)

  def _GetExistingConnectionProfile(self, name):
    get_req = self.messages.DatamigrationProjectsLocationsConnectionProfilesGetRequest(
        name=name
    )
    return self._service.Get(get_req)

  def _UpdateLabels(self, connection_profile, args):
    """Updates labels of the connection profile."""
    add_labels = labels_util.GetUpdateLabelsDictFromArgs(args)
    remove_labels = labels_util.GetRemoveLabelsListFromArgs(args)
    value_type = self.messages.ConnectionProfile.LabelsValue
    update_result = labels_util.Diff(
        additions=add_labels,
        subtractions=remove_labels,
        clear=args.clear_labels
    ).Apply(value_type, connection_profile.labels)
    if update_result.needs_update:
      connection_profile.labels = update_result.labels

  def _GetUpdatedConnectionProfile(self, connection_profile, args):
    """Returns updated connection profile and list of updated fields."""
    update_fields = []
    if args.IsSpecified('display_name'):
      connection_profile.displayName = args.display_name
      update_fields.append('displayName')
    if connection_profile.mysql is not None:
      self._UpdateMySqlConnectionProfile(connection_profile,
                                         args,
                                         update_fields)
    elif (self._SupportsPostgresql() and
          connection_profile.postgresql is not None):
      self._UpdatePostgreSqlConnectionProfile(connection_profile, args,
                                              update_fields)
    else:
      raise UnsupportedConnectionProfileDBTypeError(
          'The requested connection profile does not contain a MySQL or PostgreSQL object. '
          'Currently only MySQL and PostgreSQL connection profiles are supported.'
      )

    self._UpdateLabels(connection_profile, args)
    return connection_profile, update_fields

  def Create(self, parent_ref, connection_profile_id, cp_type, args=None):
    """Creates a connection profile.

    Args:
      parent_ref: a Resource reference to a parent
        datamigration.projects.locations resource for this connection profile.
      connection_profile_id: str, the name of the resource to create.
      cp_type: str, the type of the connection profile ('MYSQL', 'POSTGRESQL',
        ''
      args: argparse.Namespace, The arguments that this command was invoked
        with.

    Returns:
      Operation: the operation for creating the connection profile.
    """
    self._ValidateArgs(args)

    connection_profile = self._GetConnectionProfile(cp_type,
                                                    connection_profile_id, args)

    request_id = api_util.GenerateRequestId()
    create_req_type = self.messages.DatamigrationProjectsLocationsConnectionProfilesCreateRequest
    create_req = create_req_type(
        connectionProfile=connection_profile,
        connectionProfileId=connection_profile.name,
        parent=parent_ref,
        requestId=request_id
        )

    return self._service.Create(create_req)

  def Update(self, name, args=None):
    """Updates a connection profile.

    Args:
      name: str, the reference of the connection profile to
          update.
      args: argparse.Namespace, The arguments that this command was
          invoked with.

    Returns:
      Operation: the operation for updating the connection profile.
    """
    self._ValidateArgs(args)

    current_cp = self._GetExistingConnectionProfile(name)

    updated_cp, update_fields = self._GetUpdatedConnectionProfile(
        current_cp, args)

    request_id = api_util.GenerateRequestId()
    update_req_type = self.messages.DatamigrationProjectsLocationsConnectionProfilesPatchRequest
    update_req = update_req_type(
        connectionProfile=updated_cp,
        name=updated_cp.name,
        updateMask=','.join(update_fields),
        requestId=request_id
    )

    return self._service.Patch(update_req)

  def List(self, project_id, args):
    """Get the list of connection profiles in a project.

    Args:
      project_id: The project ID to retrieve
      args: parsed command line arguments

    Returns:
      An iterator over all the matching connection profiles.
    """
    location_ref = self.resource_parser.Create(
        'datamigration.projects.locations',
        projectsId=project_id,
        locationsId=args.region)

    list_req_type = self.messages.DatamigrationProjectsLocationsConnectionProfilesListRequest
    list_req = list_req_type(
        parent=location_ref.RelativeName(),
        filter=args.filter,
        orderBy=','.join(args.sort_by) if args.sort_by else None)

    return list_pager.YieldFromList(
        service=self.client.projects_locations_connectionProfiles,
        request=list_req,
        limit=args.limit,
        batch_size=args.page_size,
        field='connectionProfiles',
        batch_size_attribute='pageSize')

  def GetUri(self, name):
    """Get the URL string for a connnection profile.

    Args:
      name: connection profile's full name.

    Returns:
      URL of the connection profile resource
    """

    uri = self.resource_parser.ParseRelativeName(
        name,
        collection='datamigration.projects.locations.connectionProfiles')
    return uri.SelfLink()
