from __future__ import absolute_import

import ConfigParser
from celery.schedules import crontab

class MirrorConfParser(ConfigParser.ConfigParser):

    def as_dict(self):
        d = dict(self._sections)
        for section in d:
            for opt in d[section]:
                if opt != '__name__':
                    d[section][opt] = self.get(section, opt)
            d[section] = dict(self._defaults, **d[section])
            d[section].pop('__name__', None)
        return d

def config_to_schedule(raw_config):
    schedule = {}
    for section, config in raw_config.as_dict().iteritems():
        # schedule_args = extract_schedule(config)
        cmd = config.get('cmd', None)
        # schedule.update({
        #     section: {
        #         'task': 'mirror.tasks.ShellTask',
        #         'schedule': crontab(**schedule_args),
        #         'args': (cmd,)
        #     }
        # })

    return schedule

def extract_schedule(config):
    crontab_fields = ['minute', 'hour', 'day_of_week',
                      'day_of_month', 'month_of_year']
    schedule_args = {}
    for field in crontab_fields:
        val = config.get(field, None)
        if val:
            arg = {field:val}
            schedule_args.update(arg)
    return schedule_args
