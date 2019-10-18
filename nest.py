import json
import sys
import argparse

from parser.parser import JsonParser

if __name__ == "__main__":
    convert = JsonParser()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('keys', type=str, nargs='+')
    parser.add_argument('--input_json', default=sys.stdin)

    args = parser.parse_args(sys.argv[1:])
    stream = args.input_json.detach()

    loaded_json = json.loads(stream.read())

    dumped_output = json.dumps(convert.parse(loaded_json, keys=args.keys),
                               indent=4)
    print(dumped_output)
