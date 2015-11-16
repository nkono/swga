# -*- coding: utf-8 -*-
'''
Selects valid primers from a database according to various criteria.

This code could be a lot more succinct, but it's largely broken apart
to provide useful messages during operation (like how many primers satisfy
each criteria) and for performance reasons (i.e. we only calculate melt
temps on primers that pass the binding rate thresholds, and only calculate
binding locations on primers that pass all filters.)

Since all the results of the calculations are stored in the primer db,
the user can run this command multiple times to tune parameters and
subsequent runs will be much faster.
'''

from swga.primers import Primers
from swga.commands._command import Command
import swga.database


class Filter(Command):

    def __init__(self, argv):
        super(Filter, self).__init__('filter')
        self.parse_args(argv)

    def run(self):
        # If we have an input file, use that. Otherwise pull from db
        if self.input:
            with open(self.input, 'rb') as infile:
                primers = Primers(infile)
        else:
            self.skip_filtering = False
            primers = Primers()

        assert isinstance(primers, Primers)

        # Undo all active marks, if any
        swga.database.Primer.update(active=False).execute()

        if not self.skip_filtering:
            (
                primers
                .filter_min_fg_rate(self.min_fg_bind)
                .filter_max_bg_rate(self.max_bg_bind)
                .summarize()
                .filter_tm_range(self.min_tm, self.max_tm)
                .limit_to(self.max_primers)
                .filter_max_gini(self.max_gini, self.fg_genome_fp)
            )

        primers.activate(self.max_primers)
