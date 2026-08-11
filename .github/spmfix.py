#!/usr/bin/env python3
"""Add missing 'static inline' to the !CONFIG_MSM_SPM stubs in
include/soc/qcom/spm.h.

The four functions in the #else branch are defined (not just declared) in the
header, but without 'static'.  Every .c file that includes this header and has
CONFIG_MSM_SPM off therefore emits its own global copy, and the kernel link
fails with 'multiple definition' (board-8916.o, hotplug.o, lpm-levels-of.o,
pm-stats.o, ...).

The Y23L config has CONFIG_MSM_SPM disabled, which trips this.  The fix is
scoped to the #else branch only, so the CONFIG_MSM_SPM=y path (declarations
only, implemented in spm_devices.c) is left untouched.
"""
p = 'include/soc/qcom/spm.h'
src = open(p, encoding='utf-8').read()

marker_start = '#else /* defined(CONFIG_MSM_SPM) */'
marker_end = '#endif  /* defined (CONFIG_MSM_SPM) */'

i = src.index(marker_start)
j = src.index(marker_end, i)
block = src[i:j]

repl = [
    ('int msm_spm_config_low_power_mode(struct msm_spm_device *dev,',
     'static inline int msm_spm_config_low_power_mode(struct msm_spm_device *dev,'),
    ('int msm_spm_config_low_power_mode_addr(struct msm_spm_device *dev,',
     'static inline int msm_spm_config_low_power_mode_addr(struct msm_spm_device *dev,'),
    ('struct msm_spm_device *msm_spm_get_device_by_name(const char *name)',
     'static inline struct msm_spm_device *msm_spm_get_device_by_name(const char *name)'),
    ('bool msm_spm_is_mode_avail(unsigned int mode)',
     'static inline bool msm_spm_is_mode_avail(unsigned int mode)'),
]
for old, new in repl:
    assert block.count(old) == 1, 'pattern not found exactly once: ' + old
    block = block.replace(old, new)

src = src[:i] + block + src[j:]
open(p, 'w', encoding='utf-8').write(src)
print('spm.h patched: static inline added to 4 stubs')
