#!/usr/bin/env python3
"""Map the fork's progression from a real Factorio --dump-data snapshot.

This is a diagnostic, not a full playthrough or a balance/release gate. It
checks explicit research ancestry and machine capacity instead of treating
every ingredient and every enabled machine recipe as immediately available.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import re

RECIPE_FILES = ('prototypes/recipe/recipe.lua', 'prototypes/recipe/ammo.lua',
                'prototypes/recipe/vehicles.lua')
TECH_FILES = ('prototypes/technology/technology.lua',)
ITEM_FILES = ('prototypes/item/item.lua', 'prototypes/item/ammo.lua',
              'prototypes/item/gun.lua', 'prototypes/item/vehicles.lua',
              'prototypes/item/capsule.lua', 'prototypes/item/equipment.lua')


def declarations(source, kind, files):
    pattern = re.compile(r'\btype\s*=\s*"' + re.escape(kind)
                         + r'"\s*,\s*name\s*=\s*"([^"]+)"')
    result = set()
    for relative in files:
        text = (source / relative).read_text(encoding='utf-8-sig')
        text = re.sub(r'--\[\[.*?\]\]', '', text, flags=re.S)
        text = '\n'.join(line.split('--', 1)[0] for line in text.splitlines())
        result.update(pattern.findall(text))
    return result


def entries(value):
    if isinstance(value, list):
        return value
    return [v for v in value.values() if isinstance(v, dict)] if isinstance(value, dict) else []


def field(record):
    if isinstance(record, list):
        return 'item', record[0]
    return record.get('type', 'item'), record.get('name')


def categories(recipe):
    return recipe.get('categories') or [recipe.get('category', 'crafting')]


def machine_fits(machine, recipe):
    if not set(categories(recipe)) & set(machine.get('crafting_categories', [])):
        return False
    ingredients = recipe.get('ingredients', [])
    products = recipe.get('results', [])
    items = {field(x) for x in ingredients if field(x)[0] == 'item'}
    outputs = {field(x) for x in products if field(x)[0] == 'item'
               and x.get('probability', x.get('independent_probability', 1)) > 0}
    if machine['type'] == 'furnace':
        if len(items) > machine.get('source_inventory_size', 1):
            return False
        if len(outputs) > machine.get('result_inventory_size', 1):
            return False
    elif len(items) > machine.get('ingredient_count', 65535):
        return False
    fluids = [('input', field(x)[1]) for x in ingredients if field(x)[0] == 'fluid']
    fluids += [('output', field(x)[1]) for x in products if field(x)[0] == 'fluid']
    boxes = entries(machine.get('fluid_boxes', []))

    def assign(index, used):
        if index == len(fluids):
            return True
        direction, name = fluids[index]
        for slot, box in enumerate(boxes):
            flow = box.get('production_type', box.get('production_flow_direction', 'input-output'))
            if slot not in used and flow in (direction, 'input-output') and box.get('filter', name) == name:
                if assign(index + 1, used | {slot}):
                    return True
        return False
    return assign(0, set())


def analyze(raw, source, label):
    recipes = raw.get('recipe', {})
    techs = raw.get('technology', {})
    declared_r = declarations(source, 'recipe', RECIPE_FILES)
    declared_t = declarations(source, 'technology', TECH_FILES)
    ammo = declarations(source, 'ammo', ITEM_FILES)
    custom = set()
    for kind in ('item', 'ammo', 'gun', 'module', 'tool', 'capsule'):
        custom.update(('item', n) for n in declarations(source, kind, ITEM_FILES))
    custom.update(('fluid', n) for n in declarations(source, 'fluid', ('prototypes/fluid/fluid.lua',)))
    unlocked_by = defaultdict(set)
    invalid_unlocks = []
    for name, tech in techs.items():
        for effect in tech.get('effects', []):
            if effect['type'] == 'unlock-recipe':
                unlocked_by[effect['recipe']].add(name)
                if effect['recipe'] not in recipes and name in declared_t:
                    invalid_unlocks.append([name, effect['recipe']])
    cycles = []
    missing_prerequisites = []
    ancestors_cache = {}

    def ancestors(name, trail=()):
        if name in trail:
            cycles.append(list(trail[trail.index(name):]) + [name])
            return set()
        if name in ancestors_cache:
            return ancestors_cache[name]
        result = set()
        for parent in techs.get(name, {}).get('prerequisites', []):
            if parent not in techs:
                missing_prerequisites.append([name, parent])
            result.add(parent)
            result.update(ancestors(parent, trail + (name,)))
        ancestors_cache[name] = result
        return result

    for name in sorted(declared_t):
        ancestors(name)
    machines = {name: m for kind in ('assembling-machine', 'furnace')
                for name, m in raw.get(kind, {}).items()}
    hand_categories = set()
    for character in raw.get('character', {}).values():
        hand_categories.update(character.get('crafting_categories', ['crafting']))
    rows = []
    for name in sorted(declared_r):
        recipe = recipes.get(name)
        if recipe is None:
            rows.append({'name': name, 'missing': True})
            continue
        compatible = [n for n, m in machines.items() if machine_fits(m, recipe)]
        hand = (bool(set(categories(recipe)) & hand_categories)
                and not any(field(x)[0] == 'fluid' for x in entries(recipe.get('ingredients', []))
                            + entries(recipe.get('results', []))))
        if hand:
            compatible.append('character')
        rows.append({'name': name, 'initially_enabled': recipe.get('enabled', True),
                     'categories': categories(recipe), 'unlocked_by': sorted(unlocked_by[name]),
                     'compatible_crafters': sorted(compatible),
                     'ingredients': recipe.get('ingredients', []), 'products': recipe.get('results', [])})

    # This deliberately asks the narrower custom-material ancestry question.
    # Vanilla resources/processing and machine construction are NOT assumed to
    # be proved by it; those dependencies stay visible in the full inventory.
    research_material_gaps = []
    for name in sorted(declared_t):
        allowed = ancestors(name)
        candidates = {n: recipes[n] for n in declared_r if n in recipes and
                      (recipes[n].get('enabled', True) or unlocked_by[n] & allowed)}
        available = set()
        made = set()
        changed = True
        while changed:
            changed = False
            for rn, recipe in candidates.items():
                if rn not in made and all(field(x) not in custom or field(x) in available
                                          for x in recipe.get('ingredients', [])):
                    made.add(rn)
                    available.update(field(x) for x in recipe.get('results', []))
                    changed = True
        for ingredient in techs.get(name, {}).get('unit', {}).get('ingredients', []):
            if field(ingredient) in custom and field(ingredient) not in available:
                research_material_gaps.append({'technology': name, 'material': field(ingredient)[1]})
    tech_rows = []
    for name in sorted(declared_t):
        t = techs.get(name, {})
        tech_rows.append({'name': name, 'prerequisites': t.get('prerequisites', []),
                          'research_trigger': t.get('research_trigger'), 'unit': t.get('unit'),
                          'unlocks': sorted(e['recipe'] for e in t.get('effects', [])
                                            if e['type'] == 'unlock-recipe'),
                          'other_effects': [e for e in t.get('effects', []) if e['type'] != 'unlock-recipe']})
    diagnostics = {
        'missing_recipes': sorted(declared_r - set(recipes)),
        'missing_technologies': sorted(declared_t - set(techs)),
        'disabled_without_unlock': [r['name'] for r in rows if not r.get('missing')
                                   and not r['initially_enabled'] and not r['unlocked_by']],
        'redundant_starting_unlocks': [r['name'] for r in rows if r.get('initially_enabled') and r.get('unlocked_by')],
        'no_compatible_crafter': [r['name'] for r in rows if not r.get('missing') and not r['compatible_crafters']],
        'invalid_unlocks': invalid_unlocks, 'missing_prerequisites': missing_prerequisites,
        'cycles': cycles, 'custom_research_material_ancestry_gaps': research_material_gaps,
    }
    return {'baseline': label, 'source_manifest': source.name,
            'scope': {'custom_recipes': len(declared_r), 'custom_technologies': len(declared_t),
                      'custom_ammunition': len(ammo), 'live_recipes': len(recipes), 'live_technologies': len(techs)},
            'limits': ['Machine compatibility does not prove construction, power, terrain or routing.',
                       'Custom-material ancestry excludes vanilla manufacturing feasibility.',
                       'A complete unlocked registry is not a fresh-game playthrough.'],
            'diagnostics': diagnostics, 'recipes': rows, 'technologies': tech_rows}


def markdown(report):
    lines = ['# Complete progression inventory', '', f"Baseline: **{report['baseline']}**.", '',
             'This is the observed baseline inventory. Findings and repair decisions are in',
             '[the progression order audit](PROGRESSION_ORDER_AUDIT_2026-11-08.md).', '',
             '## Recipes', '', '| Recipe | Initially available | Unlocks | Categories | Compatible crafters |',
             '| --- | --- | --- | --- | --- |']
    for row in report['recipes']:
        lines.append('| `' + row['name'] + '` | ' + ('Yes' if row.get('initially_enabled') else 'No')
                     + ' | ' + ', '.join(row.get('unlocked_by', [])) + ' | '
                     + ', '.join(row.get('categories', [])) + ' | '
                     + ', '.join(row.get('compatible_crafters', [])) + ' |')
    lines += ['', '## Technologies', '', '| Technology | Prerequisites | Research inputs / trigger | Unlocks |',
              '| --- | --- | --- | --- |']
    for row in report['technologies']:
        inputs = ', '.join(field(x)[1] for x in (row.get('unit') or {}).get('ingredients', []))
        if row.get('research_trigger'):
            inputs = json.dumps(row['research_trigger'], sort_keys=True)
        lines.append('| `' + row['name'] + '` | ' + ', '.join(row['prerequisites']) + ' | '
                     + inputs + ' | ' + ', '.join(row['unlocks']) + ' |')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-raw', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--markdown', type=Path)
    args = parser.parse_args()
    report = analyze(json.loads(args.data_raw.read_text()), args.source, args.label)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    if args.markdown:
        args.markdown.write_text(markdown(report))
    print(json.dumps({'scope': report['scope'], 'diagnostics': report['diagnostics']}, indent=2))


if __name__ == '__main__':
    main()
