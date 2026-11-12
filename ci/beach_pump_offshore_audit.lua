-- CI-only native data-stage contract for slow shoreline water extraction.
-- The beachpump is an OFFSHORE PUMP, not an intermediate fluid transfer pump.
-- Called by the existing disposable single-profile Factorio 2.1 suite.
local offshore = data.raw["offshore-pump"] or {}
local vanilla = assert(offshore["offshore-pump"],
  "[TANKS-CI] BEACH_PUMP_OFFSHORE_FAIL vanilla offshore pump unavailable")
local beach = assert(offshore["beachpump"],
  "[TANKS-CI] BEACH_PUMP_OFFSHORE_FAIL beachpump must be offshore-pump")

local function expect(condition, message)
  if not condition then
    error("[TANKS-CI] BEACH_PUMP_OFFSHORE_FAIL " .. message)
  end
end
-- Fluid is CREATED by the shoreline source, not siphoned from an upstream pipe.
expect(beach.fluid == "water", "source water must be native offshore fluid")
expect(beach.fluid_source_offset and beach.fluid_source_offset[1] == 0 and
       beach.fluid_source_offset[2] == -1,
       "intake must point into shoreline water tile")
expect(beach.energy_source and beach.energy_source.type == "void",
       "slow starter pump must operate without electricity or burner fuel")
expect(beach.energy_usage == "1W", "retain original void power usage")
expect(beach.pumping_speed == 0.01, "starter production must remain 0.01 fluid/tick")
expect(type(vanilla.pumping_speed) == "number" and
       vanilla.pumping_speed > beach.pumping_speed * 1000,
       "starter pump must be over one thousand times slower than vanilla")

local fluid = beach.fluid_box
expect(type(fluid) == "table" and fluid.filter == "water",
       "fluid box must be filtered to water")
expect(fluid.volume == 200, "retain native beach water fluid volume")
expect(fluid.production_flow_direction == "output",
       "fluid must be produced into a pipe network, never imported")
expect(type(fluid.pipe_connections) == "table" and
       #fluid.pipe_connections == 1,
       "exactly one pipe output must exist; no upstream fluid pipe")
local port = fluid.pipe_connections[1]
expect(port.flow_direction == "output" and
       port.direction == defines.direction.south,
       "pipe socket must output to shoreward south")
expect(port.position and port.position[1] == 0 and port.position[2] == 0.25,
       "the true offshore output position must remain (0,+0.25)")

expect(beach.tile_width == 1 and beach.tile_height == 1,
       "preserve offshore-pump native placement dimensions")
expect(beach.selection_box[1][1] == -0.6 and
       beach.selection_box[1][2] == -1.49 and
       beach.selection_box[2][1] == 0.6 and
       beach.selection_box[2][2] == 0.49,
       "retain shoreline-offset selection geometry")
expect(beach.pumping_speed > 0,
       "water source must never be disabled or replaced by a passive dummy")
log(string.format(
  "[TANKS-CI] BEACH_PUMP_OFFSHORE_PASS source=shoreline-water output=south " ..
  "speed=%.4f/tick effective=%.2f/s vanilla=%.2f/s slow_factor=%.0fx " ..
  "energy=void connections=1",
  beach.pumping_speed, beach.pumping_speed * 60,
  vanilla.pumping_speed * 60, vanilla.pumping_speed / beach.pumping_speed))
