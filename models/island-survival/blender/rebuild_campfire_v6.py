#!/usr/bin/env python3
"""Reconstruct the exact V6 campfire mesh from the committed V4 generator.
No third-party assets, no network, no hidden geometry: reconstruct visible shapes only.
"""
from pathlib import Path
import argparse
import subprocess
import sys

PATCHES = [
    ("n=9; group=f'stone_{i:02d}'", "n=18; group=f'stone_{i:02d}'"),
    ("levels=[(.02,.82),(.25,1.0),(.70,.92),(1.0,.35)]", "levels=[(.02,.78),(.15,.89),(.33,.97),(.52,1.0),(.72,.86),(.89,.63),(1.0,.30)]"),
    ("wave=[rng.uniform(.79,1.14) for _ in range(n)]", "wave=[rng.uniform(.90,1.10) for _ in range(n)]"),
    ("heights=[rng.uniform(-.08,.08) for _ in range(n)]", "heights=[rng.uniform(-.046,.046) for _ in range(n)]"),
    ("heights[j] if k in (1,2) else heights[j]*.15", "heights[j] if k in (1,2,3,4,5) else heights[j]*.12"),
    ("m=color if rng.random()>.25 else rng.choice(['stone_light','stone_pale','stone_dark','stone_warm'])", "m=color"),
    ("n=13;steps=17", "n=22;steps=25"),
    ("barknoise=[rng.uniform(.91,1.09) for _ in range(n)]", "barknoise=[rng.uniform(.96,1.04) for _ in range(n)]"),
    ("lengthwise=[rng.uniform(-.055,.055) for _ in range(steps)]", "lengthwise=[(.024*math.sin((k+phase)*.4)+.012*math.cos((k+phase)*.9)) for k in range(steps)]"),
    ("knot_a=rng.choice([2,4,7,9,11])", "knot_a=rng.choice([3,6,11,15,19])"),
    ("rough=(.96+.043*math.cos(t*20+3*theta)+.038*math.sin(5*theta+13*t))", "rough=(.98+.022*math.cos(t*20+3*theta)+.019*math.sin(5*theta+13*t))"),
    ("j in (1,2,9)", "j in (1,2,16)"),
    ("j in (5,11)", "j in (8,20)"),
    ("j in (2,3) and radius>.06", "j in (3,4,5) and radius>.06"),
    ("j==8:m='wood_weathered'", "j==14:m='wood_weathered'"),
    ("start=rng.randint(2,5);finish=rng.randint(10,15)", "start=rng.randint(3,7);finish=rng.randint(19,24)"),
    ("campfire-refined-v4.mtl", "campfire-smoothed-v6.mtl"),
    ("campfire-refined-v4.obj", "campfire-smoothed-v6.obj"),
]

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--v4', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    script = args.v4.read_text()
    for old, new in PATCHES:
        matches=script.count(old)
        expected = 2 if old == 'campfire-refined-v4.mtl' else 1
        if matches != expected:
            raise RuntimeError(f'V4 generator changed: expected {expected} occurrences for {old!r}, got {matches}')
        script=script.replace(old,new)
    args.out.mkdir(parents=True,exist_ok=True)
    gen=args.out/'_reconstructed_v6_generator.py'
    gen.write_text(script)
    subprocess.run([sys.executable,str(gen),str(args.out)],check=True)
    obj=args.out/'campfire-smoothed-v6.obj'
    f=obj.read_text().splitlines()
    v=sum(s.startswith('v ') for s in f)
    faces=sum(s.startswith('f ') for s in f)
    print(f'Verified procedural V6 reconstruction: {v} vertices, {faces} triangles')
    if (v,faces)!=(6763,12152):
        raise AssertionError('V6 topology regression, not using as final input')

if __name__=='__main__':
    main()
