from invoke import Collection

from tasks import env, test, style, secure
from tasks.build import build_ns


ns = Collection()
ns.add_collection(env)
ns.add_collection(test)
ns.add_collection(style)
ns.add_collection(build_ns)
ns.add_collection(secure)
