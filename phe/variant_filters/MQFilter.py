'''
Created on 24 Sep 2015

@author: alex
'''

import argparse

from phe.variant_filters import PHEFilterBase

class MQFilter(PHEFilterBase):
    '''Filter sites by Mapping Quality (MQ) score.'''

    name = "MinMQ"
    _default_threshold = 30
    _parameter = "mq_score"

    @classmethod
    def customize_parser(self, parser):
        arg_name = self._parameter.replace("_", "-")
        parser.add_argument("--%s" % arg_name, type=int, default=self._default_threshold,
                help="Filter sites below given MQ score (default: %s)" % self._default_threshold)

    def __init__(self, args):
        """Min Mapping Quality constructor."""
        # This needs to happen first, because threshold is initialised here.
        super(MQFilter, self).__init__(args)

        # Change the threshold to custom gq value.
        self.threshold = self._default_threshold
        if isinstance(args, argparse.Namespace):
            self.threshold = args.mq_score
        elif isinstance(args, dict):
            self.threshold = args.get(self._parameter)

    def __call__(self, record):
        """Filter a :py:class:`vcf.model._Record`."""

        record_mq = record.INFO.get("MQ")

        if record_mq is None or record_mq < self.threshold:
            # FIXME: when record_mq is None, i,e, error/missing, what do you do?
            return record_mq or ""
        else:
            return None

    def short_desc(self):
        short_desc = self.__doc__ or ''

        if short_desc:
            short_desc = "%s (MQ > %s)" % (short_desc, self.threshold)

        return short_desc
