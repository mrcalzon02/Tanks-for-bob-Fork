-- Finished authored 3D inventory artwork. No recipe, research or behavior changes.
local root="__tanks_for_bob_fork__/graphics/icons/material-icons-v01/"
local rows={
 {"item","clay","clay"},
 {"item","brick","brick"},
 {"item","charcoal","charcoal"},
 {"item","crude-paper","crude-paper"},
 {"item","ink","ink"},
 {"item","calcifier","calcifier"},
 {"item","crude-glass","crude-glass"},
 {"fluid","toxic-sludge","toxic-sludge"},
 {"item","stone-tools","stone-tools"},
 {"item","wood-pulp","wood-pulp"},
 {"item","staples","staples"},
 {"item","stamps","stamps"},
 {"item","folder","folder"},
 {"item","clipboard","clipboard"},
 {"item","corporate-waste","corporate-waste"},
 {"item","PhaseDetractor","phasedetractor"},
 {"item","Canister","canister"},
 {"item","Charged-Canister","charged-canister"},
 {"item","Canister-waste","canister-waste"},
 {"item","Canister-Radioactivewaste","canister-radioactivewaste"},
 {"item","Alumatedplate","alumatedplate"},
 {"item","trace-mineral-slurry","trace-mineral-slurry"},
 {"item","saline-particulate","saline-particulate"},
 {"item","ionic-scum","ionic-scum"},
 {"item","heavy-brine-fraction","heavy-brine-fraction"},
 {"item","microcrystal-sediment","microcrystal-sediment"},
 {"item","fish-oil-residue","fish-oil-residue"},
 {"item","fish-ash","fish-ash"},
 {"item","protein-slurry","protein-slurry"},
 {"item","calcified-bone-dust","calcified-bone-dust"},
 {"item","enzyme-paste","enzyme-paste"},
 {"item","rendered-organics","rendered-organics"},
 {"item","hydrolyzed-suspension","hydrolyzed-suspension"},
 {"item","phase-diluted-brine","phase-diluted-brine"},
 {"item","osmotic-residue","osmotic-residue"},
 {"item","gradient-saline-matrix","gradient-saline-matrix"},
 {"item","biphasic-brine-gel","biphasic-brine-gel"},
 {"item","salinity-locked-emulsion","salinity-locked-emulsion"},
 {"item","hydrocoptic-precursor","hydrocoptic-precursor"},
 {"item","denatured-organic-base","denatured-organic-base"},
 {"item","enzyme-saturated-mass","enzyme-saturated-mass"},
 {"item","lipid-carrier-gel","lipid-carrier-gel"},
 {"item","bio-reactive-slurry","bio-reactive-slurry"},
 {"item","catalytic-organic-medium","catalytic-organic-medium"},
 {"item","reactive-enzyme-binder","reactive-enzyme-binder"},
 {"item","bio-synthetic-precursor","bio-synthetic-precursor"},
 {"item","crystalline-agglomerate","crystalline-agglomerate"},
 {"item","fractured-lattice-mass","fractured-lattice-mass"},
 {"item","ceramic-seed-grain","ceramic-seed-grain"},
 {"item","mineral-phase-fragments","mineral-phase-fragments"},
 {"item","ceramic-lattice-core","ceramic-lattice-core"},
 {"item","compressed-crystal-bed","compressed-crystal-bed"},
 {"item","bioceramic-preform","bioceramic-preform"},
 {"item","charged-ionic-matrix","charged-ionic-matrix"},
 {"item","dielectric-suspension","dielectric-suspension"},
 {"item","conductive-residue","conductive-residue"},
 {"item","phase-unstable-granulate","phase-unstable-granulate"},
 {"item","balanced-reactive-medium","balanced-reactive-medium"},
 {"item","phase-primed-carrier","phase-primed-carrier"},
 {"item","electro-phase-precursor","electro-phase-precursor"},
 {"item","marseline-compound","marseline-compound"},
 {"item","bioceramic-grit","bioceramic-grit"},
 {"item","hydrocoptic-crystal","hydrocoptic-crystal"},
 {"item","amulite-flakes","amulite-flakes"},
 {"item","phase-reactive-granules","phase-reactive-granules"},
 {"item","oscillated-lubricant","oscillated-lubricant"},
 {"item","stabilized-brine-gel","stabilized-brine-gel"},
 {"item","dielectric-chowder","dielectric-chowder"},
 {"item","pre-turbulated-emulsion","pre-turbulated-emulsion"},
 {"item","viscoelastic-froth","viscoelastic-froth"},
 {"item","executive-marseline-resin","executive-marseline-resin"},
 {"item","encabuloy-alloy","encabuloy-alloy"},
 {"item","hyperphase-matrix","hyperphase-matrix"},
 {"item","retrograde-polymer-sheet","retrograde-polymer-sheet"},
 {"item","duplexed-substrate","duplexed-substrate"},
 {"item","tank-light-chasis-wlsk","tank-light-chasis-wlsk"},
 {"item","tank-ammo-casing","tank-ammo-casing"},
 {"item","tank-ammo-reinforced-casing","tank-ammo-reinforced-casing"},
 {"item","tank-ammo-Industrialwaste","tank-ammo-industrialwaste"},
 {"item","tank-ammo-Radioactivewaste","tank-ammo-radioactivewaste"},
 {"item","tank-ammo-universal-explosive","tank-ammo-universal-explosive"},
 {"item","compressed-biohazard-waste","compressed-biohazard-waste"},
 {"tool","Seared-fish","seared-fish"},
 {"tool","meal","meal"},
 {"tool","requisition-slip","requisition-slip"},
 {"tool","work-order-slip","work-order-slip"},
 {"tool","certified-work-order","certified-work-order"},
 {"tool","submitted-evaluation","submitted-evaluation"},
 {"tool","risk-assessment","risk-assessment"},
 {"tool","risk-assessed-work-order","risk-assessed-work-order"},
 {"tool","compliance-packet","compliance-packet"},
 {"tool","audit-ready-deliverable","audit-ready-deliverable"},
 {"tool","stakeholder-review-summary","stakeholder-review-summary"},
 {"tool","liability-contained-report","liability-contained-report"},
 {"tool","board-review-docket","board-review-docket"},
 {"tool","board-advisory-risk-assessment","board-advisory-risk-assessment"},
 {"module","Cradinal-grametter","cradinal-grametter"},
 {"module","Hydrocoptic-marselvanes","hydrocoptic-marselvanes"},
 {"module","Retro-Encabulator","retro-encabulator"},
 {"module","SpervingArm","spervingarm"},
 {"module","DuctedSpervingArm","ductedspervingarm"},
 {"module","DuplexedSpervingArm","duplexedspervingarm"},
 {"module","Encabulator","encabulator"},
 {"module","TurboEncabulator","turboencabulator"},
 {"module","HyperEncabulator","hyperencabulator"},
 {"module","FramulatedEncabulator","framulatedencabulator"},
 {"item","stone-water-wheel","stone-water-wheel"},
}
local function apply(p,path)
 p.icon=path;p.icon_size=64;p.icons=nil;p.icon_mipmaps=nil
end
local replacements={}
for _,row in ipairs(rows) do
 local p=assert(data.raw[row[1]] and data.raw[row[1]][row[2]],"Missing modeled inventory prototype "..row[2])
 local path=root..row[3]..".png"
 replacements[row[2]]={path=path,previous=p.icon}
 apply(p,path)
 if p.place_result then
  for kind,prototypes in pairs(data.raw) do
   local e=prototypes[p.place_result]
   if e and kind~="recipe" and kind~="technology" and (e.collision_box or e.minable) then apply(e,path) end
  end
 end
end
-- Single-output recipes normally inherit item icons. Replace explicit legacy
-- multi-output icons only when their real primary result matches the item.
for _,recipe in pairs(data.raw.recipe) do
 local main=recipe.main_product
 if not main then
  if replacements[recipe.name] then
   for _,result in ipairs(recipe.results or {}) do if result.name==recipe.name then main=recipe.name;break end end
  end
  if not main and recipe.results and #recipe.results==1 then main=recipe.results[1].name end
  if (not main or main=="") and recipe.results and #recipe.results>1 then
   local first=recipe.results[1].name;local r=replacements[first]
   if r and recipe.icon==r.previous then main=first end
  end
 end
 local replacement=main and replacements[main]
 if replacement and (recipe.icon or recipe.icons) then apply(recipe,replacement.path) end
end

-- Replace the ten generic-crate research images with their actual material subjects.
if data.raw.technology["mineral-fractionation"] then apply(data.raw.technology["mineral-fractionation"],root.."trace-mineral-slurry.png") end
if data.raw.technology["ceramic-lattice-conditioning"] then apply(data.raw.technology["ceramic-lattice-conditioning"],root.."ceramic-lattice-core.png") end
if data.raw.technology["bio-reactive-processing"] then apply(data.raw.technology["bio-reactive-processing"],root.."bio-reactive-slurry.png") end
if data.raw.technology["organic-substrate-conditioning"] then apply(data.raw.technology["organic-substrate-conditioning"],root.."denatured-organic-base.png") end
if data.raw.technology["brine-conditioning"] then apply(data.raw.technology["brine-conditioning"],root.."heavy-brine-fraction.png") end
if data.raw.technology["stabilized-emulsion-systems"] then apply(data.raw.technology["stabilized-emulsion-systems"],root.."pre-turbulated-emulsion.png") end
if data.raw.technology["ionic-phase-conditioning"] then apply(data.raw.technology["ionic-phase-conditioning"],root.."charged-ionic-matrix.png") end
if data.raw.technology["biomineral-synthesis"] then apply(data.raw.technology["biomineral-synthesis"],root.."bioceramic-preform.png") end
if data.raw.technology["pre-encabulation-materials"] then apply(data.raw.technology["pre-encabulation-materials"],root.."marseline-compound.png") end
if data.raw.technology["advanced-encabulation-substrates"] then apply(data.raw.technology["advanced-encabulation-substrates"],root.."duplexed-substrate.png") end
