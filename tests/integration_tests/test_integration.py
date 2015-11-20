import os
from subprocess import call


def test_init(isolated_filesystem, fg_fasta, bg_fasta, ex_fasta):
    with isolated_filesystem:
        command = "swga init -f {} -b {} -e {}".format(
            fg_fasta, bg_fasta, ex_fasta)
        retcode = call(command, shell=True)
        assert retcode == 0
        assert os.path.exists("parameters.cfg")


def test_count(isolated_filesystem):
    with isolated_filesystem:
        command = "swga count --min_size 7 --max_size 7 --max_bg_bind -1"
        retcode = call(command, shell=True)
        assert retcode == 0


def test_filter(isolated_filesystem):
    with isolated_filesystem:
        command = "swga filter --max_bg_bind 1000000 --min_tm 0 --max_tm 100"
        retcode = call(command, shell=True)
        assert retcode == 0


def test_find_sets(isolated_filesystem):
    with isolated_filesystem:
        command = "swga find_sets"
        retcode = call(command, shell=True)
        assert retcode == 0


def test_find_sets_randomized(isolated_filesystem):
    with isolated_filesystem:
        command = "swga find_sets --workers=2 --force"
        retcode = call(command, shell=True)
        assert retcode == 0


def test_export_sets(isolated_filesystem):
    with isolated_filesystem:
        command = "swga export sets --limit 1 --order_by score"
        retcode = call(command, shell=True)
        assert retcode == 0


def test_export_bedfile(isolated_filesystem):
    with isolated_filesystem:
        command = "swga export bedfile --id 3"
        retcode = call(command, shell=True)
        assert retcode == 0


def test_export_bedgraph(isolated_filesystem):
    with isolated_filesystem:
        command = "swga export bedgraph --id 3"
        retcode = call(command, shell=True)
        assert retcode == 0


def test_count_manual(isolated_filesystem):
    with isolated_filesystem:
        with open('primers.txt', 'w') as out:
            out.write("ATGCAT\nATTTAT\n")
        command = "swga count --input primers.txt"
        retcode = call(command, shell=True)
        assert retcode == 0


def test_activate(isolated_filesystem):
    with isolated_filesystem:
        command = "swga activate primers.txt"
        retcode = call(command, shell=True)
        assert retcode == 0


def test_summary(isolated_filesystem):
    with isolated_filesystem:
        command = "swga summary"
        retcode = call(command, shell=True)
        assert retcode == 0



