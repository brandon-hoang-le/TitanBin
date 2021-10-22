# -*- coding: utf-8 -*- #
# Copyright 2015 Google LLC. All Rights Reserved.
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
"""Displays log entries produced by Google Cloud Functions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.functions.v1 import util
from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.functions import flags
from googlecloudsdk.command_lib.functions.v1.logs.read import command as command_v1
from googlecloudsdk.command_lib.functions.v2.logs.read import command as command_v2

_DEFAULT_TABLE_FORMAT = 'table(level,name,execution_id,time_utc,log)'


@base.ReleaseTracks(base.ReleaseTrack.GA)
class GetLogs(base.ListCommand):
  """Display log entries produced by Google Cloud Functions."""

  @staticmethod
  def Args(parser, track=base.ReleaseTrack.GA):
    """Register flags for this command."""
    flags.AddRegionFlag(
        parser,
        help_text='Only show logs generated by functions in the region.',
    )
    base.LIMIT_FLAG.RemoveFromParser(parser)
    parser.add_argument(
        'name',
        nargs='?',
        help=('Name of the function which logs are to be displayed. If no name '
              'is specified, logs from all functions are displayed.'))
    parser.add_argument(
        '--execution-id',
        help=('Execution ID for which logs are to be displayed.'))
    parser.add_argument(
        '--start-time',
        required=False,
        type=arg_parsers.Datetime.Parse,
        help=('Return only log entries in which timestamps are not earlier '
              'than the specified time. If *--start-time* is not specified, a '
              'default start time of 1 week ago is assumed. See $ gcloud '
              'topic datetimes for information on time formats.'))
    parser.add_argument(
        '--end-time',
        required=False,
        type=arg_parsers.Datetime.Parse,
        help=('Return only log entries which timestamps are not later than '
              'the specified time. If *--end-time* is specified but '
              '*--start-time* is not, the command returns *--limit* latest '
              'log entries which appeared before --end-time. See '
              '*$ gcloud topic datetimes* for information on time formats.'))
    parser.add_argument(
        '--limit',
        required=False,
        type=arg_parsers.BoundedInt(1, 1000),
        default=20,
        help=('Number of log entries to be fetched; must not be greater than '
              '1000. Note that the most recent entries in the specified time '
              'range are returned, rather than the earliest.'))
    flags.AddMinLogLevelFlag(parser)
    parser.display_info.AddCacheUpdater(None)

  @util.CatchHTTPErrorRaiseHTTPException
  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      A generator of objects representing log entries.
    """
    return command_v1.Run(args)


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class GetLogsBeta(GetLogs):
  """Display log entries produced by Google Cloud Functions."""

  @staticmethod
  def Args(parser, track=base.ReleaseTrack.BETA):
    """Register flags for this command."""
    GetLogs.Args(parser)

    # Add additional flags for GCFv2
    flags.AddGen2Flag(parser, track)

  @util.CatchHTTPErrorRaiseHTTPException
  def Run(self, args):
    if flags.ShouldUseGen2():
      return command_v2.Run(args, self.ReleaseTrack())
    else:
      return command_v1.Run(args)


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class GetLogsAlpha(GetLogsBeta):
  """Display log entries produced by Google Cloud Functions."""

  @staticmethod
  def Args(parser, track=base.ReleaseTrack.ALPHA):
    """Register flags for this command."""
    GetLogsBeta.Args(parser, track)
