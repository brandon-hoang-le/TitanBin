# Copyright 2020 The Abseil Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines type annotations for _flagvalues."""


from absl.flags import _flag
import six

from typing import Any, Dict, Generic, Iterable, Iterator, List, Optional, Sequence, Text, Type, TypeVar


class FlagValues:

  def __getitem__(self, name: Text) -> _flag.Flag:  ...

  def __setitem__(self, name: Text, flag: _flag.Flag) -> None:  ...

  def __getattr__(self, name: Text) -> Any:  ...

  def __setattr__(self, name: Text, value: Any) -> Any:  ...

  def __call__(
      self,
      argv: Sequence[Text],
      known_only: bool = ...,
  ) -> List[Text]: ...

  def __contains__(self, name: Text) -> bool: ...

  def __copy__(self) -> Any: ...

  def __deepcopy__(self, memo) -> Any: ...

  def __delattr__(self, flag_name: Text) -> None: ...

  def __dir__(self) -> List[Text]: ...

  def __getstate__(self) -> Any: ...

  def __iter__(self) -> Iterator[Text]: ...

  def __len__(self) -> int: ...

  def get_help(self,
               prefix: Text = ...,
               include_special_flags: bool = ...) -> Text:
    ...


  def set_gnu_getopt(self, gnu_getopt: bool = ...) -> None: ...

  def is_gnu_getopt(self) -> bool: ...

  def flags_by_module_dict(self) -> Dict[Text, List[_flag.Flag]]: ...

  def flags_by_module_id_dict(self) -> Dict[Text, List[_flag.Flag]]: ...

  def key_flags_by_module_dict(self) -> Dict[Text, List[_flag.Flag]]: ...

  def register_flag_by_module(
    self, module_name: Text, flag: _flag.Flag) -> None: ...

  def register_flag_by_module_id(
    self, module_id: Text, flag: _flag.Flag) -> None: ...

  def register_key_flag_for_module(
    self, module_name: Text, flag: _flag.Flag) -> None: ...

  def get_key_flags_for_module(self, module: Any) -> List[_flag.Flag]: ...

  def find_module_defining_flag(
    self, flagname: Text, default: Any = ...) -> Any:
    ...

  def find_module_id_defining_flag(
    self, flagname: Text, default: Any = ...) -> Any:
    ...

  def append_flag_values(self, flag_values: Any) -> None: ...

  def remove_flag_values(self, flag_values: Any) -> None: ...

  def validate_all_flags(self) -> None: ...

  def set_default(self, name: Text, value: Any) -> None: ...

  def is_parsed(self) -> bool: ...

  def mark_as_parsed(self) -> None: ...

  def unparse_flags(self) -> None: ...

  def flag_values_dict(self) -> Dict[Text, Any]: ...

  def module_help(self, module: Any) -> Text: ...

  def main_module_help(self) -> Text: ...

  def get_flag_value(self, name: Text, default: Any) -> Any: ...

  def read_flags_from_files(
    self, argv: List[Text], force_gnu: bool = ...) -> List[Text]: ...

  def flags_into_string(self) -> Text: ...

  def append_flags_into_file(self, filename: Text) -> None:...

  # outfile is Optional[fileobject]
  def write_help_in_xml_format(self, outfile: Any = ...) -> None: ...


FLAGS = ...  # type: FlagValues


_T = TypeVar('_T')  # The type of parsed default value of the flag.

# We assume that default and value are guaranteed to have the same type.
class FlagHolder(Generic[_T]):
  def __init__(
    self,
    flag_values: FlagValues,
    # NOTE: Use Flag instead of Flag[T] is used to work around some superficial
    # differences between Flag and FlagHolder typing.
    flag: _flag.Flag,
    ensure_non_none_value: bool=False) -> None: ...

  @property
  def name(self) -> Text: ...

  @property
  def value(self) -> _T: ...

  @property
  def default(self) -> _T: ...

