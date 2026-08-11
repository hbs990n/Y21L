#!/usr/bin/env python3
"""Guard the HMP fast path in select_task_rq_fair() with CONFIG_SCHED_HMP.

kernel/sched/fair.c:4870 calls select_best_cpu(p, prev_cpu, 0, sync) with four
arguments.  That prototype (fair.c:1952) only exists inside #ifdef
CONFIG_SCHED_HMP; when HMP is disabled the 3-argument inline stub (fair.c:2531)
is used and the call fails to compile with 'too many arguments'.

The Y23L config has CONFIG_SCHED_HMP off, which trips this.  The runtime
switch sched_enable_hmp is always 0 in that build, so wrapping the call in
#ifdef CONFIG_SCHED_HMP preserves behaviour exactly.
"""
p = 'kernel/sched/fair.c'
src = open(p, encoding='utf-8').read()

old = ('\tif (sched_enable_hmp)\n'
       '\t\treturn select_best_cpu(p, prev_cpu, 0, sync);')
new = ('#ifdef CONFIG_SCHED_HMP\n'
       '\tif (sched_enable_hmp)\n'
       '\t\treturn select_best_cpu(p, prev_cpu, 0, sync);\n'
       '#endif\t/* CONFIG_SCHED_HMP */')

assert src.count(old) == 1, 'pattern not found exactly once'
src = src.replace(old, new)
open(p, 'w', encoding='utf-8').write(src)
print('fair.c patched: HMP fast path guarded by #ifdef CONFIG_SCHED_HMP')
