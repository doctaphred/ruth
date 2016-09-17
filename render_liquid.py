#!/usr/bin/env python
import json
import subprocess


def render_liquid(template, context):
    # TODO: timeout, better error handling
    # TODO: reuse processes via pipes, Sinatra, or xml-rpc
    try:
        result = subprocess.run(
            ['./render_liquid.rb', template, json.dumps(context)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except:
        import pdb; pdb.set_trace()
    return result.stdout.decode('utf-8')


if __name__ == '__main__':
    import sys
    print(render_liquid(sys.argv[1], sys.argv[2]), end='')
