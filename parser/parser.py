from typing import Dict, List, Tuple

from parser.exceptions import (NotListOfDictsException,
                               NotDictException,
                               DuplicatedKeysException,
                               KeysNotFoundException)


class JsonParser(object):
    def __init__(self):
        self.output = {}

    def parse(self, input_dict: List[Dict], keys: List[str]) -> Dict:
        self.output = {}  # if we want re-use parser again
        self.__validate_input(input_dict, keys)

        for flat_dict in input_dict:
            leaf = list(set(flat_dict.keys()) - set(keys))
            all_leafs = [{l: flat_dict.get(l) for l in leaf}]

            ind, dict_to_update = self._get_nested(flat_dict, keys)
            stored_leaf = dict_to_update.get(flat_dict.get(keys[ind]), [])
            stored_leaf.append(all_leafs[0])
            current = stored_leaf

            for nest in reversed(keys):
                if nest == keys[ind]:
                    dict_to_update.update({flat_dict.get(nest): current})
                    break
                previous = current
                current = {flat_dict.get(nest): previous}
        return self.output

    def _get_nested(self, flat_dict: Dict,
                    keys: List[str]) -> Tuple[int, Dict]:
        value = self.output
        index = 0
        previous = value

        for index, nest in enumerate(keys):
            previous = value
            if not value.get(flat_dict.get(nest)):
                break

        return index, previous

    def __validate_input(self, input_dict: List[Dict], keys: List[str]):
        """
        Private method for validating input data
        """
        if not isinstance(input_dict, list):
            raise NotListOfDictsException

        for d in input_dict:
            if not isinstance(d, dict):
                raise NotDictException

        if len(keys) > len(set(keys)):
            raise DuplicatedKeysException

        allowed_keys = {v for d in input_dict for v in d.keys()}
        not_found = list(set(keys) - allowed_keys)
        if not_found:
            raise KeysNotFoundException(f'Key(s) not found: {not_found}')
