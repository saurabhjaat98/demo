import asyncio

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ccp_server.util.utils import Utils
from ccp_syncer.constants import Scheduler
from ccp_syncer.os_heat_syncer import heatsyncer
from ccp_syncer.syncer import SyncResources

scheduler = AsyncIOScheduler()
executor = ThreadPoolExecutor()

sync = SyncResources()
all_clouds = Utils.load_supported_cloud_details()
for cloud in all_clouds:
    for collection_name in sync.__func_map__:
        scheduler.add_job(sync.sync_resources,
                          trigger='interval',
                          seconds=sync.__func_map__[collection_name][2],
                          args=[collection_name, sync.__func_map__[collection_name][0],
                                sync.__func_map__[collection_name][1], cloud],
                          max_instances=1,
                          executors={'default': executor})

scheduler.add_job(heatsyncer,
                  trigger='interval',
                  seconds=Scheduler.Heat,
                  max_instances=1,
                  executors={'default': executor})
scheduler.start()
asyncio.get_event_loop().run_forever()
