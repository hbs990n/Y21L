#!/usr/bin/env python3
"""Add the missing MSM8916 zreladdr to arch/arm/mach-msm/Makefile.boot.

ZRELADDR is read from zreladdr-y in this file (arch/arm/boot/Makefile:29).
The Y21L source forgot CONFIG_ARCH_MSM8916, so zreladdr-y is empty, ZRELADDR
is empty and the zImage link fails with:

    arm-eabi-ld: error: command line:1:10: syntax error, unexpected $end
    arch/arm/boot/compressed/head.S:183: undefined reference to 'zreladdr'

For MSM8916 DDR starts at 0x80000000 and TEXT_OFFSET is 0x00008000
(arch/arm/Makefile:134), so zreladdr = 0x80008000.
"""
p = 'arch/arm/mach-msm/Makefile.boot'
src = open(p, encoding='utf-8').read()
line = '\n# MSM8916\n   zreladdr-$(CONFIG_ARCH_MSM8916)\t:= 0x80008000\n'
assert 'CONFIG_ARCH_MSM8916' not in src, 'already patched'
src += line
open(p, 'w', encoding='utf-8').write(src)
print('Makefile.boot patched: MSM8916 zreladdr=0x80008000')
